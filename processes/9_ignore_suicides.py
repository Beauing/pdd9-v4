# Keeps track of the last valid points before any suicides.
# If a suicide occurs, it increments the points and score by 1 from the last valid points.
# For non-suicide events, it increments points and score normally and updates the last valid points.

import pandas as pd

# Create summary dataframes for each round

input_path = 'final-data/no_blanks.csv'
output_path = 'final-data/sus-6.csv'

# Load the CSV file
df = pd.read_csv(input_path)

# Preserve the original points in a new column
df['log_score'] = df['points']

# Function to adjust the score for each player exclusively in each game round
def adjust_scores(df):
    # Initialize dictionaries to keep track of the last valid points for each player in each game round
    last_valid_points = {}
    player_scores = {}
    
    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        round_id = row['game_round']
        player_id = row['player_id']
        
        if player_id not in player_scores:
            player_scores[player_id] = {round_id: 0}
        
        if round_id not in player_scores[player_id]:
            player_scores[player_id][round_id] = 0
        
        # Check if it's a suicide (killer_id == victim_id)
        if row['killer_id'] == row['victim_id']:
            if player_id in last_valid_points:
                df.at[index, 'score'] = last_valid_points[player_id]
                df.at[index, 'points'] = last_valid_points[player_id]
            else:
                df.at[index, 'score'] += 1
                df.at[index, 'points'] += 1
        else:
            player_scores[player_id][round_id] += 1
            df.at[index, 'score'] = player_scores[player_id][round_id]
            df.at[index, 'points'] = player_scores[player_id][round_id]
            last_valid_points[player_id] = player_scores[player_id][round_id]
    
    return df

# Apply the function to adjust the scores
adjusted_data = adjust_scores(df)

# Save the adjusted data to the specified output path
adjusted_data.to_csv(output_path, index=False)

print(f"Adjusted round score summary for suicides saved to {output_path}")
