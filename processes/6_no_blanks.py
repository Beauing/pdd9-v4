import pandas as pd

input_path = 'final-data/remove_break_rounds.csv'
output_path = 'final-data/no_blanks.csv'

df = pd.read_csv(input_path)

# Ensure the columns are not blank
for index, row in df.iterrows():
    if pd.isna(row['player_id']):
        if index > 0:
            previous_rows = df.iloc[:index]
            previous_kills = previous_rows[(previous_rows['killer_ip'] == row['killer_ip']) & (previous_rows['killer_id'] == row['killer_id'])]
            if not previous_kills.empty:
                previous_kill = previous_kills.iloc[-1]
                df.at[index, 'player_id'] = previous_kill['player_id']
                df.at[index, 'score'] = previous_kill['score'] + 1
                df.at[index, 'player_ip'] = previous_kill['player_ip']
                df.at[index, 'points'] = previous_kill['points'] + 1
            else:
                df.at[index, 'player_id'] = row['killer_id']
                df.at[index, 'score'] = 1
                df.at[index, 'player_ip'] = row['killer_ip']
                df.at[index, 'points'] = 1
        else:
            df.at[index, 'player_id'] = row['killer_id']
            df.at[index, 'score'] = 1
            df.at[index, 'player_ip'] = row['killer_ip']
            df.at[index, 'points'] = 1

# Fill remaining NaN values with defaults if any remain
df['player_id'].fillna(method='ffill', inplace=True)
df['score'].fillna(0, inplace=True)
df['player_ip'].fillna(method='ffill', inplace=True)
df['points'].fillna(0, inplace=True)

# Save the filled DataFrame to a new CSV file
df.to_csv(output_path, index=False)

# Print the filled DataFrame to the terminal
print(df)

print(f"Filled round score summary saved to {output_path}")
