import streamlit as st
from PIL import Image
import qrcode
import io

# Set page config
st.set_page_config(page_title="UTS Campus Experiments", layout="wide")

# Main title
st.title("UTS Campus Experiments")
# Add poster image
# Note: Replace 'path_to_your_image.jpg' with the actual path to your image file
poster_image = Image.open('Images/utsevent.png')
st.image(poster_image, caption='Event Poster', use_column_width=True)

# Subtitle
st.header("Welcome to the Gaming Latency Impact Study")

# About the Study
st.subheader("About the Study")
st.write("""
Are you a gamer interested in how network latency affects your performance? We invite you to participate in an exciting research study conducted by the University of Technology Sydney (UTS). This study explores how different levels of latency impact gameplay in first-person shooting (FPS) games, with the aim of improving gaming experiences for everyone.
""")

# Why Participate
st.subheader("Why Participate?")
st.markdown("""
* **Contribute to Cutting-Edge Research:** Your participation will help us better understand the effects of latency on gaming performance and player experience, contributing to the future of online gaming.
* **Enhance Your Gaming Skills:** Through structured gameplay sessions, you'll gain insights into how latency affects your performance, potentially improving your strategies in FPS games.
* **Receive Compensation:** As a thank you for your time, participants will receive a $30 gift card or voucher.
""")

# What to Expect
st.subheader("What to Expect")
st.markdown("""
* **Duration:** Each session will last approximately 3 hours, including gameplay, breaks, and surveys.
* **Location:** All sessions will be held at the UTS campus in a dedicated gaming lab.
* **Activities:** You will play multiple rounds of a popular FPS game under different latency conditions, followed by brief surveys to capture your experience.
""")

# Who Can Participate
st.subheader("Who Can Participate?")
st.markdown("""
* **Eligibility:** We are looking for both experienced and novice FPS gamers aged 18 and above. Whether you're a seasoned player or just getting started, your input is valuable.
* **Requirements:** You should be available to visit the UTS campus for the experimental session. No special equipment or prior experience with the specific game is required.
""")

# How to Register
st.subheader("How to Register")
st.write("To express your interest in participating, you have two easy options:")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    1. **Fill Out the Registration Form:** Click the button below to complete the online registration form. Once we receive your registration, we will contact you with more details and available time slots.
    """)
    if st.button("Register Now"):
        st.markdown("[Registration Form](https://forms.gle/4ycjRbZMy9zcZwiXA)")

with col2:
    st.markdown("""
    2. **Scan the QR Code:** If you have the poster with you, simply scan the QR code with your smartphone. It will take you directly to the registration page where you can sign up in just a few clicks.
    """)
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data('https://forms.gle/4ycjRbZMy9zcZwiXA')
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert PIL image to bytes
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    byte_im = buf.getvalue()

    # Display QR code
    st.image(byte_im, caption='Scan to Register', width=200)

# Questions
st.subheader("Questions?")
st.write("If you have any questions or need more information, feel free to reach out to our research team at email@example.com.")

# Footer
st.markdown("---")
st.write("© 2024 University of Technology Sydney - Gaming Latency Impact Study")