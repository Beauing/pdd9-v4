import streamlit as st
        
pages = {
    "Home": [ 
        st.Page("pages/landing_page.py", title="Welcome", icon=":material/waving_hand:"),
        st.Page("pages/start_here.py", title="Start Here", icon=":material/start:"),
    ],
    "Demographic": [
        st.Page("pages/demographics.py", title="Participant Analysis", icon=":material/demography:"),  
    ],
    "Reports": [
        st.Page("pages/dashboard.py", title="Dashboard", icon=":material/dashboard:"),
        st.Page("pages/latency.py", title="Latency Analysis", icon=":material/signal_cellular_alt:"),
        st.Page("pages/player.py", title="Player Performance", icon=":material/person:"),
        st.Page("pages/round.py", title="Round Scoreboard", icon=":material/grid_on:"),
    ],
    "Gaming Experiments":[
        st.Page("pages/utsexperiments.py", title="UTS Campus Experiments", icon=":material/person:"),
        st.Page("pages/eventexperiments.py", title="Large Event Experiments", icon=":material/person:"),
    ],
    "Support": [
        st.Page("pages/navigation.py", title="Site Guide", icon=":material/book:"),
        st.Page("pages/how_to_read_log.py", title="How to Read Logs", icon=":material/info:"),
        st.Page("pages/credits.py", title="Credits", icon=":material/copyright:"),
    ],   
}

pg = st.navigation(pages)
pg.run()