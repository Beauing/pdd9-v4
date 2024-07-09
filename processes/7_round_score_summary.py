import pandas as pd

# Create summary dataframes for each round

input_path = 'final-data/remove_break_rounds.csv'
output_path = 'final-data/round_summary.csv'

# Mapping of player IDs to IP addresses
player_ip_map = {
    1: 'Player_172.19.137.208',
    2: 'Player_172.19.114.48',
    3: 'Player_172.19.119.51',
    4: 'Player_172.19.116.18',
    5: 'Player_172.19.120.104',
    6: 'Player_172.19.117.18'
}

# Read the CSV file
df = pd.read_csv(input_path)

# Unique player IDs to include in the summary
player_ids = list(range(1, 7))

# Initialize a list to store the summary data
summary_data = []

# Group by game_round and iterate over each group
for game_round, group in df.groupby('game_round'):
    current_map = group['map'].iloc[0] if pd.notna(group['map'].iloc[0]) else ''
    current_latency = group['latency'].iloc[0] if pd.notna(group['latency'].iloc[0]) else ''
    
    for player_id in player_ids:
        player_ip = player_ip_map[player_id]
        player_data = group[group['player_id'] == player_id]
        if not player_data.empty:
            last_record = player_data.iloc[-1]
            score = last_record['score'] if pd.notna(last_record['score']) else 0
        else:
            score = 0
        
        summary_data.append({
            'game_round': game_round,
            'map': current_map,
            'latency': current_latency,
            'player_id': player_id,
            'player_ip': player_ip,
            'score': score
        })

# Create a summary DataFrame
summary_df = pd.DataFrame(summary_data)

# Save the summary DataFrame to a new CSV file
summary_df.to_csv(output_path, index=False)

# Print the summary DataFrame to the terminal
print(summary_df)

print(f"Round score summary saved to {output_path}")