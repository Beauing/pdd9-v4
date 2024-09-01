import streamlit as st
from datetime import datetime
from PIL import Image

# Set page config
st.set_page_config(page_title="Large Event Experiments", layout="wide")

# Main title
st.title("Large Event Experiments")

# Add poster image
# Note: Replace 'path_to_your_image.jpg' with the actual path to your image file
poster_image = Image.open('Images/largeevent.png')
st.image(poster_image, caption='Event Poster', use_column_width=True)

# Upcoming Events
st.header("Upcoming Events")
st.write("""
Get ready for an exciting series of large-scale gaming experiments! As part of our ongoing research on the impact of latency in first-person shooting (FPS) games, we're hosting several large event experiments that will allow you to experience gaming in a controlled environment, contribute to cutting-edge research, and connect with other gamers.
""")

# Event Details
st.header("Event Details")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Event Information")
    st.write("**Event Name:** [Insert Event Name]")
    st.write("**Date:** TBC")
    st.write("**Time:** TBC")
    st.write("**Location:** University of Technology Sydney (UTS) - TBC")

with col2:
    st.subheader("What to Expect")
    st.markdown("""
    * **Structured Gameplay:** Participate in multiple gaming sessions where you'll experience different latency conditions and see how they affect your performance.
    * **Data Collection:** Your gameplay data will be recorded and analyzed as part of our research. This is your chance to contribute valuable insights to the future of online gaming.
    * **Networking Opportunities:** Meet fellow gamers, researchers, and industry professionals. Share your experiences and learn from others in the gaming community.
    * **Prizes and Giveaways:** As a token of our appreciation, participants will have the chance to win gaming-related prizes and receive exclusive giveaways.
    """)

# How to Participate
st.header("How to Participate")
st.write("Interested in joining our large event experiments? Here's how you can get involved:")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    * **Pre-Register:** Ensure your spot by pre-registering online. Space is limited, so we recommend signing up early.
    * **Walk-In Registration:** Limited walk-in spots will be available on the day of the event. Arrive early to secure your place.
    * **Group Participation:** Bring your friends! Group registrations are welcome. Indicate your group size when you pre-register.
    """)

with col2:
    if st.button("Pre-Register Now"):
        st.success("Thank you for your interest! Pre-registration will be available soon.")

# Who Can Participate
st.header("Who Can Participate?")
st.markdown("""
* **Eligibility:** Open to all gamers aged 18 and above, regardless of experience level. Whether you're a seasoned pro or new to FPS games, your participation is valuable.
* **Requirements:** Participants should be able to attend the UTS campus on the event date. No special gaming equipment is needed; everything will be provided.
""")

# Why Participate
st.header("Why Participate?")
st.markdown("""
* **Contribute to Research:** Help us understand the effects of network latency on gameplay. Your participation will provide crucial data that could shape the future of gaming.
* **Improve Your Skills:** Experience firsthand how latency affects your gameplay and learn strategies to improve your performance.
* **Enjoy the Community:** Take part in a fun and engaging event, meet new people, and enjoy a day dedicated to gaming and research.
""")

# Questions
st.header("Questions?")
st.write("If you have any questions about the upcoming events, please don't hesitate to reach out to us at email@example.com. We're happy to provide more information and assist with your registration.")

# Countdown Timer (placeholder)
st.sidebar.header("Event Countdown")
event_date = st.sidebar.date_input("Event Date", datetime.now())
event_time = st.sidebar.time_input("Event Time", datetime.now().time())
if st.sidebar.button("Set Countdown"):
    event_datetime = datetime.combine(event_date, event_time)
    time_left = event_datetime - datetime.now()
    st.sidebar.write(f"Time left: {time_left}")

# Footer
st.markdown("---")
st.write("© 2024 Large Event Experiments - Gaming Latency Research")