import streamlit as st
from streamlit_option_menu import option_menu
import sidebar as sb
from datetime import datetime

pages = [
    {"name": "Home", "icon": "house"},
    {"name": "Demographic", "icon": "people"},
    {"name": "Reports", "icon": "clipboard-data"},
    # {"name": "Gaming Experiments", "icon": "controller"},
    {"name": "Support", "icon": "question-circle"}
]

def display_page(page_name):
    if page_name == "Home":
        sb.show_welcome()
    elif page_name == "Demographic":
        sb.show_demographic()
    elif page_name == "Reports":
        sb.show_reports()
    # elif page_name == "Gaming Experiments":
    #     sb.show_experiments()
    elif page_name == "Support":
        sb.show_support()

# Initialize session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"

# Sidebar navigation
with st.sidebar:
    st.title("Main Menu")
    
    selected_page = option_menu(
        menu_title=None,
        options=[page["name"] for page in pages],
        icons=[page["icon"] for page in pages],
        menu_icon="cast",
        default_index=next((i for i, page in enumerate(pages) if page["name"] == st.session_state.current_page), 0),
    )

    # Update current page if selection changes
    if selected_page != st.session_state.current_page:
        st.session_state.current_page = selected_page
        st.rerun()

# Display the selected page
display_page(st.session_state.current_page)

def add_footer():
    year = datetime.now().year
    footer = f"""
    <div class="footer" style="text-align: center;">
        <hr style="margin-top: 50px; border: 0; border-top: 1px solid #ccc;">
        <p>© {year} University of Technology Sydney. All rights reserved.</p>
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)

add_footer()