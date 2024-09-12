import streamlit as st
from streamlit_option_menu import option_menu
import general.latency as general_latency
import general.round as general_round
import player_specific.player as player_specific_player

# st.set_page_config(page_title="Game Analysis Reports", page_icon="📊", layout="wide")
# def show_reports():
#     # Horizontal options menu
#     selected_category = option_menu(
#         menu_title=None,
#         options=["General", "Player-specific"],
#         icons=["graph-up", "person"],
#         menu_icon="cast",
#         default_index=0,
#         orientation="horizontal",
#     )

#     if selected_category == "General":
#         # Select box for General category
#         general_option = st.selectbox(
#             "Select analysis type",
#             options=["Latency", "Round"],
#             index=0  # Default to Latency
#         )

#         if general_option == "Latency":
#             general_latency.show_latency()
#         elif general_option == "Round":
#             general_round.show_round()

#     elif selected_category == "Player-specific":
#         # Select box for Player-specific category
#         player_option = st.selectbox(
#             "Select analysis type",
#             options=["Player Performance"],
#             index=0  # Only one option, so default index is 0
#         )

#         if player_option == "Player Performance":
#             player_specific_player.show_player()

# Horizontal options menu
selected_category = option_menu(
    menu_title=None,
    options=["General", "Player-specific"],
    icons=["graph-up", "person"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)

if selected_category == "General":
    # Select box for General category
    general_option = st.selectbox(
        "Select analysis type",
        options=["Latency", "Round"],
        index=0  # Default to Latency
    )

    if general_option == "Latency":
        general_latency.show_latency()
    elif general_option == "Round":
        general_round.show_round()

elif selected_category == "Player-specific":
    # Select box for Player-specific category
    player_option = st.selectbox(
        "Select analysis type",
        options=["Player Performance"],
        index=0  # Only one option, so default index is 0
    )

    if player_option == "Player Performance":
        player_specific_player.show_player()
