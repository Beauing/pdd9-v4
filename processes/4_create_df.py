import pandas as pd
import re

input_path = 'processes/processed_logs/start_again.log'
output_path = 'final-data/full.csv'

# Read the log file
with open(input_path, 'r') as file:
    log_contents = file.readlines()

# Initialize the data list
data = []
current_game_round = 1
current_map = None
current_latency = None

# Define the event parsing functions
def parse_kill(event):
    match = re.match(r'\\x08 \\x08Kill: (\d+) (\d+) (\d+): (.+) killed (.+) by (.+)', event)
    if match:
        return {
            'killer_id': match.group(1),
            'victim_id': match.group(2),
            'weapon_id': match.group(3),
            'killer_ip': match.group(4),
            'victim_ip': match.group(5),
            'weapon': match.group(6),
        }
    return {}

def parse_playerscore(event):
    match = re.match(r'\\x08 \\x08PlayerScore: (\d+) (\d+): (.+) now has (\d+) points', event)
    if match:
        return {
            'player_id': match.group(1),
            'score': match.group(2),
            'player_ip': match.group(3),
            'points': match.group(4),
        }
    return {}

# Process each log line
for line in log_contents:
    if 'loaded maps/' in line:
        # Extract the map name
        current_map = re.search(r'loaded maps/(.*)\.aas', line).group(1)
        current_game_round += 1  # Increment game round when a new map is loaded
    elif 'Network egress latency:' in line:
        # Extract the latency value
        current_latency = re.search(r'Network egress latency: (\d+) ms', line).group(1)
    else:
        timestamp, events = line.split(': ', 1)
        # Split the events by the known event prefixes
        event_list = re.split(r'(\\x08 \\x08Kill:|\\x08 \\x08PlayerScore:|\\x08 \\x08Challenge:|\\x08 \\x08Award:)', events)
        event_list = event_list[1:]  # Remove any leading empty entry
        
        merged_event = {
            'timestamp': timestamp,
            'game_round': current_game_round,
            'map': current_map,
            'latency': current_latency,
            'event': '',
            'killer_id': '',
            'victim_id': '',
            'weapon_id': '',
            'killer_ip': '',
            'victim_ip': '',
            'weapon': '',
            'player_id': '',
            'score': '',
            'player_ip': '',
            'points': '',
            'log_line': line.strip()
        }
        
        for i in range(0, len(event_list), 2):
            prefix = event_list[i]
            event_details = prefix + event_list[i + 1]
            parsed_event = {}
            if 'Kill:' in prefix:
                event_type = 'Kill'
                parsed_event = parse_kill(event_details)
            elif 'PlayerScore:' in prefix:
                event_type = 'PlayerScore'
                parsed_event = parse_playerscore(event_details)
            else:
                event_type = 'Award'
                parsed_event = {}  # Just to include the timestamp and event_type

            for key, value in parsed_event.items():
                if value:
                    merged_event[key] = value

            if 'event' not in merged_event or not merged_event['event']:
                merged_event['event'] = event_type

        data.append(merged_event)

# Create the DataFrame with all possible columns
df = pd.DataFrame(data)

# Save the DataFrame to the specified CSV file path
df.to_csv(output_path, index=False)

output_path
