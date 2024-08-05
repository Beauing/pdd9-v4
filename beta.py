import streamlit as st

pages = {
    "Home": [ 
        st.Page("pages/landing_page.py", title="Welcome", icon=":material/waving_hand:"),
        st.Page("pages/start_here.py", title="Start Here", icon=":material/start:"),
        st.Page("pages/dashboard.py", title="Dashboard", icon=":material/dashboard:"),
    ],
    "Reports": [
        st.Page("pages/player.py", title="Player Performance", icon=":material/person:"),
        st.Page("pages/round.py", title="Round Scoreboard", icon=":material/grid_on:"),
        st.Page("pages/map.py", title="Map Analysis", icon=":material/public:"),
        st.Page("pages/latency.py", title="Latency Analysis", icon=":material/signal_cellular_alt:")
    ],
    "Support": [
        st.Page("pages/how_to.py", title="How to", icon=":material/info:"),
    ],   
}

pg = st.navigation(pages)
pg.run()