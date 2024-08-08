import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
    st.title("Player Performance")
    
    source = "final-data/player_performance.csv"
    sb_summary = "final-data/round_summary_adjusted.csv"
    df = pd.read_csv(source)
    sb = pd.read_csv(sb_summary)
    
    select_maps = df['map'].unique()
    select_latency = df['latency'].unique()
    select_latency.sort()
    select_player = df['player_ip'].unique()
    select_round = df['game_round'].unique()
    
    option_player = st.selectbox("Select a Player", [""] + list(select_player), index=1)
    
    col1, col2 = st.columns(2)
    
    with col1:
        
        player_pts = sb[sb['player_ip'] == option_player]
        st.write(f"{option_player} Points Overview")
        
        player_pts = player_pts.drop(columns=['player_id', 'player_ip'])

        if not player_pts.empty:
            # Create a bar chart for the round scoreboard
            fig, ax = plt.subplots()
            player_pts.plot(kind='bar', x='game_round', y='score', ax=ax, legend=False)
            ax.set_xlabel('Game Round')
            ax.set_ylabel('Score')
            ax.set_title(f'Points Earned Per Round by {option_player}')
            st.pyplot(fig)
            
            # Sort the table by score in descending order and display it
            player_pts_sorted = player_pts.sort_values(by='score', ascending=False)
            st.write(player_pts_sorted)
            
    with col2:
            
        player_deaths = sb[sb['player_ip'] == option_player]
        st.write(f"{option_player} Death Count Overview")
        
        player_deaths = player_deaths.drop(columns=['player_id', 'player_ip'])

        if not player_deaths.empty:
            # Create a bar chart for the round scoreboard
            fig, ax = plt.subplots()
            player_deaths.plot(kind='bar', x='game_round', y='score', ax=ax, legend=False)
            ax.set_xlabel('Game Round')
            ax.set_ylabel('Score')
            ax.set_title(f'Number of times {option_player} has been killed')
            st.pyplot(fig)
            
            # Sort the table by score in descending order and display it
            player_deaths_sorted = player_deaths.sort_values(by='score', ascending=False)
            st.write(player_deaths_sorted)
        
    

main()