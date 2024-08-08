import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('final-data/round_summary_adjusted.csv')

st.set_option('deprecation.showPyplotGlobalUse', False)

# Function to generate statistical summary and graphs
def generate_statistics(df):
    # Group by latency
    grouped = df.groupby('latency')
    
    # Dictionary to store results
    result_dfs = {}

    for latency, group in grouped:
        # Initialize dataframe with unique player_ips as index
        unique_player_ips = group['player_ip'].unique()
        latency_df = pd.DataFrame(index=unique_player_ips)
        
        # Filter group to include only rows with the current latency value
        group = group[group['latency'] == latency]
        
        for game_round in group['game_round'].unique():
            # Filter group for the current game_round and player_ip
            round_scores = group[group['game_round'] == game_round].set_index('player_ip')['score'].rename(f'Round_{game_round}')
            latency_df = latency_df.join(round_scores, how='left')
        
        # Calculate mean and standard deviation for each player_ip
        latency_df['Mean'] = latency_df.mean(axis=1)
        latency_df['StdDev'] = latency_df.std(axis=1)
        
        # Calculate mean difference relative to latency 0 (assuming latency 0 exists in the original data)
        if 0 in result_dfs:
            latency_df['mean_difference'] = latency_df['Mean'] - result_dfs[0]['Mean']
        else:
            latency_df['mean_difference'] = 0  # or handle appropriately if latency 0 doesn't exist
        
        # Store latency_df in result_dfs
        result_dfs[latency] = latency_df
    
    return result_dfs

# Generate statistics
result_dfs = generate_statistics(df)

# Streamlit app
def main():
    st.title('Players\' Mean Scores vs Latency Statistical Analysis')

    # Select latency value
    latency_values = list(result_dfs.keys())
    selected_latency = st.selectbox('Select Latency Value (ms)', latency_values, index=1)

    # Display selected dataframe
    st.subheader(f'Statistics for Latency {selected_latency}')
    st.write(result_dfs[selected_latency])

    # Line graph to show mean scores vs latency for each player_ip
    plt.figure(figsize=(12, 8))
    for player_ip in df['player_ip'].unique():
        means = [result_dfs[latency].loc[player_ip, 'Mean'] for latency in result_dfs.keys() if player_ip in result_dfs[latency].index]
        plt.plot(list(result_dfs.keys()), means, marker='o', label=f'Player {player_ip}')
    plt.xticks(list(result_dfs.keys()))
    plt.xlabel('Latency')
    plt.ylabel('Mean Score')
    plt.title('Players\' Mean Scores vs Latency')
    plt.legend()
    st.pyplot()

main()