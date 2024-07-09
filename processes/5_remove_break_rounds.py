import pandas as pd

# Remove rows related to kaos maps
# Adjusts game round counter

input_path = 'final-data/full.csv'
output_path = 'final-data/remove_break_rounds.csv'

# Read the CSV file
df = pd.read_csv(input_path)

# Initialize the game round counter
game_round_counter = 0

def update_game_round(row, current_map, game_round_counter):
    if pd.notna(row['map']) and row['map'] != current_map:
        game_round_counter += 1
        current_map = row['map']
    row['game_round'] = game_round_counter
    return row, current_map, game_round_counter

# Filter out rows where the map is 'kaos' or NaN and update the game round
current_map = None
filtered_rows = []

for index, row in df.iterrows():
    if row['map'] != 'kaos' and pd.notna(row['map']):
        row, current_map, game_round_counter = update_game_round(row, current_map, game_round_counter)
        filtered_rows.append(row)

# Create a filtered DataFrame
df_filtered = pd.DataFrame(filtered_rows)

# Save the filtered DataFrame to a new CSV file
df_filtered.to_csv(output_path, index=False)

print(f"Filtered data saved to {output_path}")