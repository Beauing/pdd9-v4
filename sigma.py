import os
import streamlit as st
from streamlit_navigation_bar import st_navbar
import sidebar as sb

pages = ["Home", "Demographics", "Reports", "Support", "About"]
parent_dir = os.path.dirname(os.path.abspath(__file__))

styles = {
    "nav": {
        "background-color": "rgb(139, 0, 0)",
    },
    "div": {
        "max-width": "32rem",
    },
    "span": {
        "border-radius": "0.5rem",
        "color": "rgb(255, 255, 255)",
        "margin": "0 0.125rem",
        "padding": "0.4375rem 0.625rem",
    },
    "active": {
        "background-color": "rgba(255, 255, 255, 0.25)",
    },
    "hover": {
        "background-color": "rgba(255, 255, 255, 0.35)",
    },
}
options = {
    "show_menu": False,
    "show_sidebar": False,
}

page = st_navbar(
    pages,
    styles=styles,
    options=options,
)

# Define a function to render content based on the selected page
def render_page_content(selected_page):
    if selected_page == "Home":
        sb.show_welcome()
    elif selected_page == "Demographics":
        sb.show_demographic()
    elif selected_page == "Reports":
        sb.show_reports()
    elif selected_page == "Support":
        sb.show_support()  # Make sure this function exists in your sidebar module
    elif selected_page == "About":
        sb.show_credits()

# Render the content of the selected page
render_page_content(page)