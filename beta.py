import streamlit as st

pages = {
    "Home": [ 
        st.Page("pages/landing_page.py", title="Welcome", icon=":material/waving_hand:"),
        st.Page("pages/start_here.py", title="Start Here", icon=":material/start:"),
        # st.Page("pages/dashboard.py", title="Dashboard", icon=":material/dashboard:"),
    ],
    "Demographic": [
        st.Page("pages/demographics.py", title="Participant Analysis", icon=":material/demography:"),  
    ],
    "Reports": [
        st.Page("pages/player.py", title="Player Performance", icon=":material/person:"),
        st.Page("pages/round.py", title="Round Scoreboard", icon=":material/grid_on:"),
        # st.Page("pages/map.py", title="Map Analysis", icon=":material/public:"),
        st.Page("pages/latency.py", title="Latency Analysis", icon=":material/signal_cellular_alt:")
    ],
    "Gaming Experiments":[
        st.Page("pages/utsexperiments.py", title="UTS Campus Experiments", icon=":material/person:"),
        st.Page("pages/eventexperiments.py", title="Large Event Experiments", icon=":material/person:"),
    ],
    "About": [
        st.Page("pages/how_to.py", title="How to", icon=":material/info:"),
        st.Page("pages/credits.py", title="Credits", icon=":material/copyright:"),
    ],   
}

pg = st.navigation(pages)
pg.run()