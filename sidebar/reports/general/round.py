import streamlit as st
import pandas as pd
import altair as alt

def show_round():

    def load_data():
        return pd.read_csv("final-data/round_summary_adjusted.csv")

    def checkbox_group(label, options, key_prefix, columns=3):
        cols = st.columns(columns)
        selected = []
        for i, option in enumerate(options):
            if cols[i % columns].checkbox(str(option), value=True, key=f"{key_prefix}_{option}"):
                selected.append(option)
        return selected

    def calculate_player_stats(df):
        stats = df.groupby('player_ip').agg({
            'score': ['max', 'mean', 'sum'],
            'game_round': ['first', 'last']  # To get the range of rounds
        }).reset_index()
        stats.columns = ['player_ip', 'highest_score', 'average_score', 'total_score', 'first_round', 'last_round']
        stats['average_score'] = stats['average_score'].round(2)
        
        highest_score_rounds = df.loc[df.groupby('player_ip')['score'].idxmax()][['player_ip', 'game_round', 'score']]
        highest_score_rounds = highest_score_rounds.rename(columns={'game_round': 'highest_score_round'})
        stats = stats.merge(highest_score_rounds, on='player_ip', suffixes=('', '_highest'))
        
        return stats

    # Custom CSS for rounded boxes and responsive design
    st.markdown("""
    <style>
        .rounded-box {
            border-radius: 10px;
            padding: 20px;
            background-color: #f0f2f6;
            margin-bottom: 20px;
        }
        .player-box {
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .stat-row {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            margin-bottom: 10px;
        }
        .stat-column {
            flex: 1;
            min-width: 150px;
            text-align: center;
            margin-bottom: 10px;
        }
        @media (max-width: 768px) {
            .stat-column {
                flex-basis: 100%;
            }
        }
    </style>
    """, unsafe_allow_html=True)

    # Load data
    df = load_data()

    st.title("Round Scoreboard")

    # View selection
    st.subheader("Select View")
    view_option = st.radio(
        "Choose a view option",
        ["All Rounds", "By Round", "By Map"],
        index=0
    )

    if view_option == "All Rounds":
        filtered_df = df
    elif view_option == "By Round":
        st.subheader("Select Round")
        selected_round = st.selectbox("Choose a round", sorted(df['game_round'].unique()))
        filtered_df = df[df['game_round'] == selected_round]
    else:  # By Map
        st.subheader("Select Map")
        selected_map = st.radio("Choose a map", sorted(df['map'].unique()))
        filtered_df = df[df['map'] == selected_map]

    # Players checkboxes
    st.subheader("Select Players")
    player_options = sorted(df['player_ip'].unique())
    selected_players = checkbox_group("Choose players to display", player_options, "player", columns=3)

    # Apply player filter
    filtered_df = filtered_df[filtered_df['player_ip'].isin(selected_players)]

    # Create a line chart for player scores
    if view_option == "All Rounds":
        chart = alt.Chart(filtered_df).mark_line(point=True).encode(
            x='game_round:O',
            y='score:Q',
            color='player_ip:N',
            tooltip=['game_round', 'player_ip', 'score', 'map', 'latency']
        ).properties(
            width=700,
            height=400,
            title='Player Scores Across All Rounds'
        ).interactive()
    elif view_option == "By Round":
        chart = alt.Chart(filtered_df).mark_bar().encode(
            x='player_ip:N',
            y='score:Q',
            color='player_ip:N',
            tooltip=['player_ip', 'score', 'map', 'latency']
        ).properties(
            width=700,
            height=400,
            title=f'Player Scores for Round {selected_round}'
        ).interactive()
    else:  # By Map
        chart = alt.Chart(filtered_df).mark_line(point=True).encode(
            x='game_round:O',
            y='score:Q',
            color='player_ip:N',
            tooltip=['game_round', 'player_ip', 'score', 'latency']
        ).properties(
            width=700,
            height=400,
            title=f'Player Scores for Map: {selected_map}'
        ).interactive()

    st.altair_chart(chart, use_container_width=True)

    # Display summary statistics in a rounded box
    st.markdown('<div class="rounded-box">', unsafe_allow_html=True)
    st.subheader("Overall Summary Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Highest Score", filtered_df['score'].max() if not filtered_df.empty else "N/A")
    col2.metric("Average Score", round(filtered_df['score'].mean(), 2) if not filtered_df.empty else "N/A")
    col3.metric("Total Rounds", filtered_df['game_round'].nunique())
    st.markdown('</div>', unsafe_allow_html=True)

    # Calculate and display player statistics
    st.subheader("Player Statistics")
    if not filtered_df.empty:
        player_stats = calculate_player_stats(filtered_df)
        
        # Custom CSS for styling
        st.markdown("""
        <style>
        .player-stats-header {
            font-weight: bold;
            border-bottom: 2px solid #4B5563;
            padding-bottom: 10px;
            margin-bottom: 10px;
        }
        .player-stats-row {
            border-bottom: 1px solid #4B5563;
            padding-bottom: 10px;
            margin-bottom: 10px;
        }
        .player-icon {
            font-size: 24px;
            color: #60A5FA;
        }
        .player-name {
            font-weight: bold;
            color: #60A5FA;
        }
        </style>
        """, unsafe_allow_html=True)

        # Create header
        cols = st.columns([1, 2, 2, 2, 2, 1, 1])
        cols[0].markdown('<div class="player-stats-header">Player</div>', unsafe_allow_html=True)
        cols[1].markdown('<div class="player-stats-header">Total Score</div>', unsafe_allow_html=True)
        cols[2].markdown('<div class="player-stats-header">Highest Score</div>', unsafe_allow_html=True)
        cols[3].markdown('<div class="player-stats-header">Average Score</div>', unsafe_allow_html=True)
        cols[4].markdown('<div class="player-stats-header">First Round</div>', unsafe_allow_html=True)
        cols[5].markdown('<div class="player-stats-header">Last Round</div>', unsafe_allow_html=True)

        # Add rows for each player
        for _, player in player_stats.iterrows():
            cols = st.columns([1, 2, 2, 2, 2, 1, 1])
            cols[0].markdown(f'<div class="player-stats-row"><i class="bi bi-person-badge-fill player-icon"></i> <span class="player-name">{player["player_ip"]}</span></div>', unsafe_allow_html=True)
            cols[1].markdown(f'<div class="player-stats-row">{player["total_score"]:.2f}</div>', unsafe_allow_html=True)
            cols[2].markdown(f'<div class="player-stats-row">{player["highest_score"]} (Round {player["highest_score_round"]})</div>', unsafe_allow_html=True)
            cols[3].markdown(f'<div class="player-stats-row">{player["average_score"]:.2f}</div>', unsafe_allow_html=True)
            cols[4].markdown(f'<div class="player-stats-row">{player["first_round"]}</div>', unsafe_allow_html=True)
            cols[5].markdown(f'<div class="player-stats-row">{player["last_round"]}</div>', unsafe_allow_html=True)

    else:
        st.write("No data available for the selected view and players.")

    # Display raw data
    st.subheader("Raw Data")
    st.dataframe(filtered_df)