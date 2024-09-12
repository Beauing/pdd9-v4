import streamlit as st
import sidebar as sb

def show_support():
        
    # Create the Table of Contents at the top of the screen
    st.title("Support")
    st.markdown("""
    ##### [How to Navigate the Site](#how-to-navigate-the-site)
    """)
    st.markdown("""
    ##### [How to Read the Game Logs](#how-to-read-the-game-logs)
    """)
    st.markdown("""
    ##### [Credits](#credits)
    """)

    # Add some spacing between the ToC and sections
    st.markdown("---")

    st.markdown("## How to navigate the site")
    sb.show_navigation()
    st.markdown("---")
    
    st.markdown("## How to read the game logs")
    sb.show_read_logs()
    st.markdown("---")

    st.markdown("## Credits")
    sb.show_credits()
    