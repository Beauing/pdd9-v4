import streamlit as st

def welcome_page():
    st.title("Welcome to the Quake 3 Analysis Dashboard")
    
    st.markdown("""
    This dashboard is designed to help you analyse player performance, game rounds, and other important metrics in a comprehensive way. 
    Use the sidebar to navigate through different sections and get the insights you need.
    """)
    
    st.subheader("Navigation Guide")
    
    st.markdown("""
    **Home**
    - **Welcome:** Overview of the dashboard and navigation instructions.
    - **Dashboard:** A summary view of key metrics and quick insights.

    **Reports**
    - **Player Performance:** Analyse individual player metrics and compare performances.
    - **Round Scoreboard:** Review and compare scores for each game round.
    - **Map Analysis:** Understand how different maps impact player performance and game outcomes.
    - **Latency Analysis:** Examine how latency affects player performance across different rounds.

    **Support**
    - **How to:** Detailed guide on understanding log event components.
    """)
    
    st.info("Use the sidebar to explore these sections and start analysing your data!")

welcome_page()
