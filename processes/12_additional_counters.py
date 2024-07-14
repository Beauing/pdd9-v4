import pandas as pd
import subprocess

# Create summary dataframes for each round

input_path = 'final-data/ignore_suicides.csv'
output_path = 'final-data/player_performance.csv'

# Load the input CSV file
df = pd.read_csv(input_path)

# Drop the 'log_line' column
df.drop(columns=['log_line'], inplace=True)

# Adding the new columns with initial values set to 0
df['suicide_count'] = 0
df['deaths_total'] = 0
# df['killed_by_Player_172.19.137.208'] = 0
# df['killed_by_Player_172.19.114.48'] = 0
# df['killed_by_Player_172.19.119.51'] = 0
# df['killed_by_Player_172.19.116.18'] = 0
# df['killed_by_Player_172.19.120.104'] = 0
# df['killed_by_Player_172.19.117.18'] = 0

# Function to calculate the counts for each round
def calculate_counts(group):
    suicide_count = 0
    # deaths_by_ip = {ip: 0 for ip in [
    #     'Player_172.19.137.208', 'Player_172.19.114.48', 'Player_172.19.119.51',
    #     'Player_172.19.116.18', 'Player_172.19.120.104', 'Player_172.19.117.18'
    # ]}
    
    # Mark suicides
    group['is_suicide'] = group['killer_ip'] == group['victim_ip']
    
    # Calculate cumulative suicides
    group['suicide_count'] = group.groupby('victim_ip')['is_suicide'].cumsum()
        
        
    # Calculate deaths total
    group['deaths_total'] = group.groupby('victim_ip').cumcount() + 1
    
    return group

# Applying the function to each game round
df = df.groupby('game_round', group_keys=False).apply(calculate_counts)

# Drop the 'is_suicide' column as it's no longer needed
df.drop(columns=['is_suicide'], inplace=True)

# Saving the updated and filtered dataframe to the output CSV file
df.to_csv(output_path, index=False)

print(f"Suicide counts, total deaths and deaths from each player_ip by round have been recorded in {output_path}")

# subprocess.call(['open', output_path])
