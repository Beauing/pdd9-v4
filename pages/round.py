import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
    st.title("Round Scoreboard")
    
    source = "final-data/player_performance.csv"
    sb_summary = "final-data/round_summary_adjusted.csv"
    df = pd.read_csv(source)
    sb = pd.read_csv(sb_summary)
    
    select_latency = df['latency'].unique()
    select_latency.sort()
    select_round = df['game_round'].unique()
    
    option_round = st.selectbox("Select a Round", [""] + list(select_round), key='round_select')
    
    round_scoreboard = sb[sb['game_round'] == int(option_round)]
    map_name = round_scoreboard['map'].iloc[0] if not round_scoreboard.empty else "N/A"
    latency = round_scoreboard['latency'].iloc[0] if not round_scoreboard.empty else "N/A"

    st.subheader(f"Round {option_round} Scoreboard")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"Map: {map_name}")
    with col2:
        st.write(f"Latency: {latency} ms")
    
    round_scoreboard = round_scoreboard.drop(columns=['game_round', 'map', 'latency'])

    # Create a bar chart for the round scoreboard
    fig, ax = plt.subplots()
    round_scoreboard.plot(kind='bar', x='player_id', y='score', ax=ax, legend=False)
    ax.set_xlabel('Player IP')
    ax.set_ylabel('Score')
    ax.set_title(f'Score by Player IP for Round {option_round}')
    st.pyplot(fig)
    
    # Sort the table by score in descending order and display it
    round_scoreboard_sorted = round_scoreboard.sort_values(by='score', ascending=False)
    st.write(round_scoreboard_sorted)
    
    
main()