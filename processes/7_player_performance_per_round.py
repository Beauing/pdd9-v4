import pandas as pd
import os

input_path = 'final-data/no_blanks.csv'
output_dir = 'final-data/player_performance_per_round.csv'

# Read the CSV file
df = pd.read_csv(input_path)

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Group by game_round and player_ip and save each group to a separate CSV file
for (game_round, player_ip), group in df.groupby(['game_round', 'player_ip']):
    output_path = os.path.join(output_dir, f'round_{game_round}_player_{player_ip}.csv')
    group.to_csv(output_path, index=False)
    # print(f'Saved round {game_round} for player {player_ip} to {output_path}')

print("DataFrames for each round and player_ip have been saved.")
