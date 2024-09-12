import streamlit as st
from datetime import datetime
import os

def show_credits():    

    def load_css(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
            
    def user_card(user_name, email, image_path, linkedin_url, github_url=None, website_url=None):
        col1, col2 = st.columns([1, 3])  # Adjust the ratio to control the size of image and text columns
        with col1:
            # Check if image file exists before rendering
            if os.path.exists(image_path):
                st.markdown(f'<div class="circular-image"><img src="data:image/jpeg;base64,{get_image_base64(image_path)}" width="150"></div>', unsafe_allow_html=True)
            else:
                st.error(f"Image not found: {image_path}")
        
        with col2:
            st.markdown(f"**{user_name}**")
            if email:
                st.markdown(f"Email: {email}")
            links = f"[LinkedIn]({linkedin_url})"
            if github_url:
                links += f" | [GitHub]({github_url})"
            if website_url:
                links += f" | [Website]({website_url})"
            
            st.markdown(links)
        
        # Add spacing after each user card
        st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)

    def get_image_base64(image_path):
        import base64
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    load_css("styles.css")

    # st.title("Credits")

    st.markdown("The NBN Network Simulation project represents a collaborative effort between UTS and NBN, combining academic expertise with industry insight. This initiative aims to model and optimise network performance, leveraging advanced algorithms and real-world data. Our team of students, faculty, and industry professionals has worked tirelessly to create innovative solutions for modern networking challenges.")

    st.markdown("""
    <style>
    .circular-image {
        width: 150px;
        height: 150px;
        overflow: hidden;
        border-radius: 50%;
    }
    .circular-image img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    .section-spacing {
        margin-top: 20px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Capstone Students
    st.markdown("<div class='section-spacing'></div>", unsafe_allow_html=True)
    st.subheader("👥 Capstone Students")

    student1 = (
        "Sydney Melendres", 
        "sydney.n.melendres@student.uts.edu.au", 
        "images/profile/sydney.jpeg",
        "https://www.linkedin.com/in/sydneymelendres/", 
        "https://github.com/sydney-melendres", 
        "https://sydneymelendres.notion.site/Hello-I-m-Sydney-5aa767e093144cf185fbe2bcdeb13e27?pvs=4"
    )
    student2 = (
        "Beau Ingram", 
        "beau.ingram@student.uts.edu.au", 
        "images/profile/beau.jpeg",
        "https://www.linkedin.com/in/beau-ingram/",
        "https://github.com/modem9000",
        None  # No website provided
    )
    student3 = (
        "Andrew Vo", 
        "hiep.k.vo@student.uts.edu.au", 
        "images/profile/andrew.jpeg",
        "https://www.linkedin.com/in/andrew-vo-0311/",
        "https://github.com/hiepvo01",
        "https://hiepvo01.github.io/Portfolio/"
    )

    user_card(*student1) 
    user_card(*student2)
    user_card(*student3)

    # Project Team
    st.markdown("<div class='section-spacing'></div>", unsafe_allow_html=True)
    st.subheader("👥 Project Team")

    uts1 = (
        "**Minh Pham** | UTS Research Fellow", 
        "duc.pham@uts.edu.au",
        "images/profile/minh.jpeg",
        "https://www.linkedin.com/in/duc-minh-pham-3993352a/",
        None, None
    )
    uts2 = (
        "**Daniel Franklin** | UTS Associate Professor", 
        "daniel.franklin@uts.edu.au",
        "images/profile/daniel.jpeg",
        "https://www.linkedin.com/in/daniel-franklin-bb2420/overlay/photo/",
        None, None
    )
    nbn1 = (
        "**Mark Vanston** | NBN General Manager", 
        None,
        "images/profile/mark.jpeg",
        "https://www.linkedin.com/in/markvanston/",
        None, None
    )
    nbn2 = (
        "**Max Downey** | NBN Solutions Architect", 
        None,
        "images/profile/max.jpeg",
        "https://www.linkedin.com/in/max-downey-1b310147/",
        None, None
    )

    user_card(*uts1)
    user_card(*uts2)
    user_card(*nbn1)
    user_card(*nbn2)

    # Technologies Used
    st.markdown("<div class='section-spacing'></div>", unsafe_allow_html=True)
    st.subheader("💻 Technologies Used")
    technologies = [
        {"name": "Languages", "details": "Python"},
        {"name": "Deployment", "details": "Streamlit"}
    ]

    for tech in technologies:
        st.write(f"**{tech['name']}:** {tech['details']}")

    # Special Thanks
    st.markdown("<div class='section-spacing'></div>", unsafe_allow_html=True)
    st.subheader("🙏 Special Thanks")
    st.write("A big thank you to all mentors, professors, and peers who supported us throughout this project!")