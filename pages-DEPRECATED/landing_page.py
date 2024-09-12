import streamlit as st
from PIL import Image


st.set_page_config(layout="wide", page_title="Quake 3 Analysis Dashboard", page_icon="🎮")

# Custom CSS for minimal styling
st.markdown("""
<style>
.title {
    font-size: 36px;
    font-weight: bold;
    color: black;
    margin-bottom: 0;
}
.stButton>button {
    background-color: #FF4B4B;
    color: white;
    border-radius: 5px;
    padding: 10px 24px;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

# Header with logos
col1, col2, col3 = st.columns([4, 1, 1])

with col1:
    st.title("Quake 3 Analysis Dashboard")

with col2:
    logo1 = Image.open('Images/NBN.png')
    st.image(logo1, width=180)

with col3:
    logo2 = Image.open('Images/UTS.png')
    st.image(logo2, width=200)

c1, c2 = st.columns(2)

with c1:
    st.info("⬅️ New to the dashboard? Check out our Site Guide page for support.")
    st.write("This dashboard provides comprehensive insights into player performance, game rounds, and other crucial metrics in Quake 3. Explore different sections using the sidebar to gain valuable insights into your gaming data.")
    st.markdown("""
    Our dashboard offers:
    - 📊 Comprehensive player statistics
    - 🏆 Detailed round analysis
    - 🔍 Insightful latency metrics
    - 🧠 Advanced gaming experiments data
    """)
    
    # st.subheader("Participate in Our Research")
    # st.write("We're conducting exciting experiments to further our understanding of gaming performance:")
    
    # but1, but2 = st.columns([2, 5])
    
    # with but1:
    #     if st.button("UTS Campus Experiments", key="uts_experiments"):
    #         st.switch_page("utsexperiments")    
    # with but2:
    #     st.write("Our controlled studies at the UTS.")
        
    # but3, but4 = st.columns([2,5])
    
    # with but3:
    #     if st.button("Large Event Experiments", key="scaled_experiments"):
    #         st.switch_page("eventexperiments.py")
        
    # with but4:
    #     st.write("Larger-scale gaming sessions.")

with c2:
    st.subheader("How It Works")
    st.markdown("""
    1. **Data Input**: Quake 3 game logs and participant surveys are uploaded into our system.
    2. **Processing**: Our Python backend parses, extracts, and analyses the data.
    3. **Visualisation**: The processed data is transformed into interactive graphs and charts.
    4. **User Interaction**: You can access the UI, select filters, and explore the analysed data.
    """)

    if st.button("Get Started Here", key="get_started"):
        st.switch_page("pages/start_here.py")
    st.write("*Note: Additional pages will become visible once you've uploaded files.*")