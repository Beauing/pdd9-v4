import streamlit as st
import pandas as pd
import altair as alt

def load_data():
    return pd.read_csv("final-data/round_summary_adjusted.csv")

def multiselect_with_select_all(label, options, key):
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected = st.multiselect(label, options, key=key)
    
    with col2:
        if st.button("Select All", key=f"select_all_{key}"):
            return options
    
    return selected

def calculate_player_stats(df):
    stats = df.groupby('player_ip').agg({
        'score': ['max', 'mean', 'sum'],
        'game_round': ['first', 'last']  # To get the range of rounds
    }).reset_index()
    stats.columns = ['player_ip', 'highest_score', 'average_score', 'total_score', 'first_round', 'last_round']
    stats['average_score'] = stats['average_score'].round(2)
    
    # Find the round with the highest score for each player
    highest_score_rounds = df.loc[df.groupby('player_ip')['score'].idxmax()][['player_ip', 'game_round', 'score']]
    highest_score_rounds = highest_score_rounds.rename(columns={'game_round': 'highest_score_round'})
    stats = stats.merge(highest_score_rounds, on='player_ip', suffixes=('', '_highest'))
    
    return stats

# Custom CSS for rounded boxes
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
        justify-content: space-between;
        margin-bottom: 10px;
    }
    .stat-column {
        flex: 1;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Load data
df = load_data()

st.title("Round Scoreboard")

# Filter at the top of the page
st.header("Filter")

# Rounds multiselect with Select All button
round_options = sorted(df['game_round'].unique())
selected_rounds = multiselect_with_select_all(
    "Select Rounds",
    options=round_options,
    key="game_round"
)

# Filter data based on selections
filtered_df = df[df['game_round'].isin(selected_rounds)]

# Create a line chart for player scores across rounds
chart = alt.Chart(filtered_df).mark_line(point=True).encode(
    x='game_round:O',
    y='score:Q',
    color='player_ip:N',
    tooltip=['game_round', 'player_ip', 'score', 'map', 'latency']
).properties(
    width=700,
    height=400,
    title='Player Scores Across Rounds'
).interactive()

st.altair_chart(chart, use_container_width=True)

# Display summary statistics in a rounded box
st.markdown('<div class="rounded-box">', unsafe_allow_html=True)
st.subheader("Overall Summary Statistics")
col1, col2, col3 = st.columns(3)
col1.metric("Highest Score", filtered_df['score'].max() if not filtered_df.empty else "N/A")
col2.metric("Average Score", round(filtered_df['score'].mean(), 2) if not filtered_df.empty else "N/A")
col3.metric("Total Rounds", len(selected_rounds))
st.markdown('</div>', unsafe_allow_html=True)

# Calculate and display player statistics
st.subheader("Player Statistics")
if not filtered_df.empty:
    player_stats = calculate_player_stats(filtered_df)
    colors = ['#ffcccc', '#ccffcc', '#ccccff', '#ffffcc', '#ffccff', '#ccffff']
    for i, (_, player) in enumerate(player_stats.iterrows()):
        color = colors[i % len(colors)]  # Cycle through colors
        st.markdown(f'''
        <div class="player-box" style="background-color: {color};">
            <h3>{player['player_ip']}</h3>
            <div class="stat-row">
                <div class="stat-column">
                    <strong>Highest Score</strong><br>
                    {player['highest_score']} (Round {player['highest_score_round']})
                </div>
                <div class="stat-column">
                    <strong>Average Score</strong><br>
                    {player['average_score']}
                </div>
                <div class="stat-column">
                    <strong>Total Score</strong><br>
                    {player['total_score']}
                </div>
            </div>
            <div>Rounds: {player['first_round']} - {player['last_round']}</div>
        </div>
        ''', unsafe_allow_html=True)
else:
    st.write("No data available for the selected rounds.")

# Display raw data
st.subheader("Raw Data")
st.dataframe(filtered_df)