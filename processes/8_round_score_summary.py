import pandas as pd

# Create summary dataframes for each round

input_path = 'final-data/remove_break_rounds.csv'
output_path = 'final-data/round_summary.csv'

# Read the CSV file
df = pd.read_csv(input_path)

# Get unique player IPs and create a mapping
unique_player_ips = df['player_ip'].unique()
player_ip_map = {i+1: ip for i, ip in enumerate(unique_player_ips)}

# Reverse mapping for easy lookup
ip_player_map = {v: k for k, v in player_ip_map.items()}

# Initialize a list to store the summary data
summary_data = []

# Group by game_round and iterate over each group
for game_round, group in df.groupby('game_round'):
    current_map = group['map'].iloc[0] if pd.notna(group['map'].iloc[0]) else ''
    current_latency = group['latency'].iloc[0] if pd.notna(group['latency'].iloc[0]) else ''
    
    for player_ip in unique_player_ips:
        player_id = ip_player_map[player_ip]
        player_data = group[group['player_ip'] == player_ip]
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

print(f"Round score summary saved to {output_path}")

# Print out the player ID to IP mapping for reference
print("\nPlayer ID to IP mapping:")
for player_id, ip in player_ip_map.items():
    print(f"Player {player_id}: {ip}")