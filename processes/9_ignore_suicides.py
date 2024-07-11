import pandas as pd

# Create summary dataframes for each round

input_path = 'final-data/no_blanks.csv'
output_path = 'final-data/ignore_suicides.csv'

# Read the CSV file
df = pd.read_csv(input_path)

# Preserve the original points in a new column
df['log_score'] = df['points']

# Adjust scores and points for suicides and subsequent kills
for index, row in df.iterrows():
    if row['killer_ip'] == row['victim_ip']:
        if index > 0:
            previous_row = df.iloc[index - 1]
            df.at[index, 'score'] = previous_row['score']
            df.at[index, 'points'] = previous_row['points']
        else:
            df.at[index, 'score'] = 0
            df.at[index, 'points'] = 0
    elif index > 0:
        previous_row = df.iloc[index - 1]
        df.at[index, 'score'] = previous_row['score'] + 1
        df.at[index, 'points'] = previous_row['points'] + 1

# Save the adjusted DataFrame to a new CSV file
df.to_csv(output_path, index=False)

print(f"Adjusted round score summary for suicides saved to {output_path}")
