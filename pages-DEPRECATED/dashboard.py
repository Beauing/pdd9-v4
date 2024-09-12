import streamlit as st
import pandas as pd

# source = "final-data/player_performance.csv"
# sb_summary = "final-data/round_summary_adjusted.csv"
# df = pd.read_csv(source)
# sb = pd.read_csv(sb_summary)

# select_maps = df['map'].unique()
# select_latency = df['latency'].unique()
# select_latency.sort()
# select_player = df['player_ip'].unique()
# select_round = df['game_round'].unique()

# st.set_page_config(
#     page_title="Dashboard",
#     page_icon=":bar_chart:",
# )

st.title("Dashboard")

# col1, col2, col3, col4 = st.columns(4)

# selected_attributes = ['', '', '', '']

# with col1:
#     selected_maps = st.multiselect("Select map/s:", select_maps)

# with col2:
#     selected_latency = st.multiselect("Latency", select_latency)

# with col3:
#     select_round = st.multiselect("Round", select_round)
    
# with col4:
#     select_player = st.multiselect("Player", select_player)
    
# st.divider()

# st.info("Show scoreboard")