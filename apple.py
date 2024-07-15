import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
    source = "final-data/player_performance.csv"
    sb_summary = "final-data/round_summary_adjusted.csv"
    df = pd.read_csv(source)
    sb = pd.read_csv(sb_summary)
    
    select_maps = df['map'].unique()
    select_latency = df['latency'].unique()
    select_latency.sort()
    select_player = df['player_ip'].unique()
    select_round = df['game_round'].unique()

    
    with st.sidebar:
        st.info("Overview")
        
        st.subheader("Filters")
        filter_options = ["", "Map", "Latency", "Player Points", "Player Death Count", "Player Performance", "Round Scoreboard"]
        filter_select = st.selectbox("Select a filter", filter_options, key='filter_select')

        if filter_select == "Map":
            option_map = st.selectbox("Select a Map", [""] + list(select_maps), key='map_select')

        elif filter_select == "Latency":
            option_latency = st.selectbox("Select Latency", [""] + list(select_latency), key='latency_select')

        elif filter_select == "Player Points":
            option_points = st.selectbox("Select a Player", [""] + list(select_player), key='points_select')

        elif filter_select == "Player Death Count":
            option_deaths = st.selectbox("Select a Player", [""] + list(select_player), key='deaths_select')

        elif filter_select == "Player Performance":
            option_performance = st.selectbox("Select a Player", [""] + list(select_player), key='performance_select')

        elif filter_select == "Round Scoreboard":
            option_round = st.selectbox("Select a Round", [""] + list(select_round), key='round_select')


    # Create a Streamlit page with three filters side by side
    st.subheader('Overview')

    selected_maps = st.multiselect("Select map/s:", select_maps)

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_latency = st.multiselect("Latency", select_latency)

    with col2:
        st.warning("Jitter not available.")

    with col3:
        st.warning("Loss not available.")
        
    st.divider()
    
    st.info("Show scoreboard")

    # Filter the dataframe based on the selected maps and latency
    filtered_df = df[df['map'].isin(selected_maps) & df['latency'].isin(selected_latency)]

    # Create a bar chart based on the filtered data
    if not filtered_df.empty:
        fig, ax = plt.subplots()
        filtered_df.groupby('player_ip')['points'].sum().plot(kind='bar', ax=ax)
        ax.set_xlabel('Player IP')
        ax.set_ylabel('Points')
        ax.set_title('Points by Player IP')
        st.pyplot(fig)
    else:
        st.write("No data available for the selected filters.")

    if filter_select == "Player Points" and option_points:
        player_pts = sb[sb['player_ip'] == option_points]
        st.subheader(f"{option_points} Points Overview")
        
        player_pts = player_pts.drop(columns=['player_id', 'player_ip'])

        if not player_pts.empty:
            # Create a bar chart for the round scoreboard
            fig, ax = plt.subplots()
            player_pts.plot(kind='bar', x='game_round', y='score', ax=ax, legend=False)
            ax.set_xlabel('Player IP')
            ax.set_ylabel('Score')
            ax.set_title(f'Points Earned Per Round by {option_points}')
            st.pyplot(fig)
            
            # Sort the table by score in descending order and display it
            player_pts_sorted = player_pts.sort_values(by='score', ascending=False)
            st.write(player_pts_sorted)
        else:
            st.write("No data available for the selected round.")
    
    if filter_select == "Player Death Count" and option_deaths:
        player_deaths = sb[sb['player_ip'] == option_deaths]
        st.subheader(f"{option_deaths} Death Count Overview")
        
        player_deaths = player_deaths.drop(columns=['player_id', 'player_ip'])

        if not player_deaths.empty:
            # Create a bar chart for the round scoreboard
            fig, ax = plt.subplots()
            player_deaths.plot(kind='bar', x='game_round', y='score', ax=ax, legend=False)
            ax.set_xlabel('Player IP')
            ax.set_ylabel('Score')
            ax.set_title(f'Number of times {option_deaths} has been killed')
            st.pyplot(fig)
            
            # Sort the table by score in descending order and display it
            player_deaths_sorted = player_deaths.sort_values(by='score', ascending=False)
            st.write(player_deaths_sorted)
        else:
            st.write("No data available for the selected round.")
            
    if filter_select == "Player Performance" and option_performance:
        performance = df[df['player_ip'] == option_performance]
        st.subheader(f"Victims killed by {option_performance}")
        
        performance = performance.drop(columns=['player_id', 'player_ip'])

        if not performance.empty:
            # Create a bar chart for the round scoreboard
            fig, ax = plt.subplots()
            performance.plot(kind='bar', x='game_round', y='score', ax=ax, legend=False)
            ax.set_xlabel('Victim IP')
            ax.set_ylabel('Score')
            ax.set_title(f'Number of times {option_performance} has killed others')
            st.pyplot(fig)
            
            # Sort the table by score in descending order and display it
            performance_sorted = performance.sort_values(by='score', ascending=False)
            st.write(performance_sorted)
        else:
            st.write("No data available for the selected round.")

            
    if filter_select == "Round Scoreboard" and option_round:
        round_scoreboard = sb[sb['game_round'] == int(option_round)]
        map_name = round_scoreboard['map'].iloc[0] if not round_scoreboard.empty else "N/A"
        latency = round_scoreboard['latency'].iloc[0] if not round_scoreboard.empty else "N/A"

        st.subheader(f"Round {option_round} Scoreboard")
        st.info(f"Map: {map_name}")
        st.info(f"Latency: {latency} ms")
        
        round_scoreboard = round_scoreboard.drop(columns=['game_round', 'map', 'latency'])

        if not round_scoreboard.empty:
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
        else:
            st.write("No data available for the selected round.")

        
if __name__ == "__main__":
    main()