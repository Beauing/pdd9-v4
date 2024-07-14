import pandas as pd
import subprocess

# Create summary dataframes for each round

input_path = 'final-data/ignore_suicides.csv'
output_path = 'final-data/player_performance.csv'

# Load the input CSV file
df = pd.read_csv(input_path)

# Drop the 'log_line' column
drop = {
    'log_line',
    'killer_id',
    'victim_id',
    'weapon_id',
    'weapon',
    'player_id',
    'log_score'
}
df.drop(columns=['{drop}'], inplace=True)

# Adding the new columns with initial values set to 0
df['suicide_count'] = 0
df['deaths_total'] = 0

players = [
    '172.19.137.208', '172.19.114.48', '172.19.119.51', 
    '172.19.116.18', '172.19.120.104', '172.19.117.18'
]

for player in players:
    df[f'killed_by_Player_{player}'] = 0
    df[f'killed_Player_{player}'] = 0

# Function to calculate the counts for each round
def calculate_counts(group):
    suicide_count = 0

    # Mark suicides
    group['is_suicide'] = group['killer_ip'] == group['victim_ip']
    
    # Calculate cumulative suicides
    group['suicide_count'] = group.groupby('player_ip')['is_suicide'].cumsum()
        
    # Calculate deaths total
    group['deaths_total'] = group.groupby('victim_ip').cumcount() + 1
    
    # Update killed_by_Player and killed_Player counters
    for player in players:
        player_ip = f'Player_{player}'
        group[f'killed_by_Player_{player}'] = (group['killer_ip'] == player_ip).cumsum()
        group[f'killed_Player_{player}'] = (group['victim_ip'] == player_ip).cumsum()
    
    return group

# Applying the function to each game round
df = df.groupby('game_round', group_keys=False).apply(calculate_counts)

# Drop the 'is_suicide' column as it's no longer needed
df.drop(columns=['is_suicide'], inplace=True)

# Saving the updated and filtered dataframe to the output CSV file
df.to_csv(output_path, index=False)

print(f"Suicide counts, total deaths and deaths from each player_ip by round have been recorded in {output_path}")

# subprocess.call(['open', output_path])