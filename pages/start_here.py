import os
import streamlit as st
import subprocess
import time
import pandas as pd

def display_temporary_message(message, type='info', duration=5):
    placeholder = st.empty()
    getattr(placeholder, type)(message)
    time.sleep(duration)
    placeholder.empty()

if 'files_uploaded' not in st.session_state:
    st.session_state.files_uploaded = False
if 'operation_completed' not in st.session_state:
    st.session_state.operation_completed = False
if 'processing_started' not in st.session_state:
    st.session_state.processing_started = False

run_script = "run_all.py"
log_file_path = ""
demographic_file_path = ""

st.title("Start Here")

if not st.session_state.files_uploaded:
    st.header("File Import")
    
    uploaded_log_file = st.file_uploader("Import Log File", type=["log", "txt"])
    uploaded_demographic_file = st.file_uploader("Import Demographic CSV File", type=["csv"])

    if uploaded_log_file and uploaded_demographic_file:
        progress_bar = st.progress(0)
        status_text = st.empty()

        for i in range(100):
            # Simulating file upload progress
            progress_bar.progress(i + 1)
            status_text.text(f"Uploading... {i+1}%")
            time.sleep(0.01)

        log_file_name = uploaded_log_file.name
        demographic_file_name = uploaded_demographic_file.name
        
        log_file_path = os.path.join("import", log_file_name)
        demographic_file_path = os.path.join("survey-data", demographic_file_name)
        
        os.makedirs("import", exist_ok=True)
        os.makedirs("survey-data", exist_ok=True)

        with open(log_file_path, "wb") as f:
            f.write(uploaded_log_file.getbuffer())
        
        with open(demographic_file_path, "wb") as f:
            f.write(uploaded_demographic_file.getbuffer())
        
        st.session_state.files_uploaded = True
        progress_bar.empty()
        status_text.empty()
        st.success("Files uploaded successfully!")

# Check if files have been uploaded
if st.session_state.files_uploaded and not st.session_state.operation_completed:    
    if not st.session_state.processing_started:
        if st.button("Process Data"):
            st.session_state.processing_started = True
    
    if st.session_state.processing_started:
        progress_bar = st.progress(0)
        status_text = st.empty()
        status_text.text("Please wait... Processing data")
        
        # Update the input path in 1_start.py
        with open("processes/1_start.py", "r") as file:
            script_content = file.read()
        script_content = script_content.replace("log_file_path = ''", f"log_file_path = '{log_file_path}'")
        with open("processes/1_start.py", "w") as file:
            file.write(script_content)
        
        # Simulate processing with progress bar
        for i in range(100):
            time.sleep(0.1)  # Simulate some work being done
            progress_bar.progress(i + 1)
        
        result = subprocess.run(["python3", run_script], capture_output=True, text=True)
        
        if result.returncode != 0:
            st.error(f"Error processing data: {result.stderr}")
        else:
            st.session_state.operation_completed = True
            progress_bar.empty()
            status_text.empty()
            st.success("Data processing completed successfully!")

def display_selected_players(selected_players, df):
    if not selected_players:
        st.info("No players selected. Please choose players from the list above.")
        return

    st.subheader("Selected Players")
    
    # Create a 3-column layout
    cols = st.columns(3)
    
    for idx, player in enumerate(selected_players):
        with cols[idx % 3]:
            with st.expander(f"**Player:** {player}", expanded=True):
                player_data = df[df['player_ip'] == player]
                
                # Display basic player statistics
                st.markdown(f"**Total Games:** {player_data['game_round'].nunique()}")
                # st.markdown(f"**Total Kills:** {player_data['killed_by_Player_' + player].sum()}")
                # st.markdown(f"**Total Deaths:** {player_data['deaths_total'].sum()}")
                
                # # Calculate K/D ratio
                # kd_ratio = player_data['killed_by_Player_' + player].sum() / player_data['deaths_total'].sum() if player_data['deaths_total'].sum() > 0 else 0
                # st.markdown(f"**K/D Ratio:** {kd_ratio:.2f}")
                
                # # Display a mini bar chart of kills per game
                # kills_per_game = player_data.groupby('game_round')['killed_by_Player_' + player].sum()
                # st.bar_chart(kills_per_game, use_container_width=True, height=100)
                
                # if st.button(f"Analyse {player}", key=f"analyse_{player}"):
                #     st.session_state.selected_player = player
                #     st.success(f"Analysing {player}. Navigate to the Player Performance page for detailed analysis.")

if st.session_state.operation_completed:
    st.subheader('Player Analysis')
    metadata = "final-data/player_performance.csv"
    if os.path.exists(metadata):
        df = pd.read_csv(metadata)
        unique_players = df['player_ip'].unique()
        selected_players = st.multiselect("Select players for detailed analysis", unique_players)

        display_selected_players(selected_players, df)

        if selected_players:
            if st.button("Continue"):
                st.session_state.pages_unlocked = True
                st.switch_page("pages/dashboard.py")
    else:
        st.error(f"Player performance data not found. Please ensure the file {metadata} exists.")