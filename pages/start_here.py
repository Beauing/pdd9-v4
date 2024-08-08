import os
import streamlit as st
import subprocess
import time
import pandas as pd

def display_temporary_message(message, type='info', duration=5):
    placeholder = st.empty()
    if type == 'success':
        placeholder.success(message)
    elif type == 'info':
        placeholder.info(message)
    elif type == 'warning':
        placeholder.warning(message)
    elif type == 'error':
        placeholder.error(message)
    else:
        placeholder.info(message)
    
    time.sleep(duration)
    placeholder.empty()
    
# Initialize session state variables
if 'files_uploaded' not in st.session_state:
    st.session_state.files_uploaded = False
if 'operation_completed' not in st.session_state:
    st.session_state.operation_completed = False
if 'import_button_clicked' not in st.session_state:
    st.session_state.import_button_clicked = False

# Set paths
run_script = "run_all.py"
log_file_path = ""
demographic_file_path = ""

if not st.session_state.files_uploaded:
    # File uploaders
    uploaded_log_file = st.file_uploader("Import Log File", type=["log", "txt"])
    uploaded_demographic_file = st.file_uploader("Import Demographic CSV File", type=["csv"])

    # Save the uploaded files and set the input paths
    if uploaded_log_file and uploaded_demographic_file:
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

# Check if files have been uploaded
files_uploaded = st.session_state.files_uploaded

if files_uploaded and not st.session_state.operation_completed:
    if not st.session_state.import_button_clicked:
        if st.button("Import"):
            st.session_state.import_button_clicked = True
            
            # Update the input path in 1_start.py
            with open("processes/1_start.py", "r") as file:
                script_content = file.read()

            script_content = script_content.replace("log_file_path = ''", f"log_file_path = '{log_file_path}'")

            with open("processes/1_start.py", "w") as file:
                file.write(script_content)
                
            result = subprocess.run(["python3", run_script], capture_output=True, text=True)
            
            # Display the progress bar
            progress_text = "Processing..."
            my_bar = st.progress(0, text=progress_text)

            for percent_complete in range(100):
                time.sleep(0.01)
                my_bar.progress(percent_complete + 1, text=progress_text)
            
            # Give it a little time to show 100% completion
            time.sleep(1)
            my_bar.empty()

            # Run the central script
            if result.returncode != 0:
                st.error(f"Error running {run_script}: {result.stderr}")
            else:
                st.session_state.operation_completed = True
                                
                if st.button("Upload new files"):
                    st.session_state.files_uploaded = False
                    st.session_state.operation_completed = False
                    st.session_state.import_button_clicked = False
                    st.experimental_rerun()

if st.session_state.operation_completed:
    # Reveal new section for player selection and input
    st.subheader('Player Selection')
    metadata = "final-data/player_performance.csv"
    if os.path.exists(metadata):
        df = pd.read_csv(metadata)
        unique_players = df['player_ip'].unique()
        selected_players = st.multiselect("Select players", unique_players)

        player_numbers = {}
                
        for player in selected_players:
            player_numbers[player] = st.write(f"{player}", min_value=0, step=1)

        if st.button("Submit", disabled=not selected_players):
            st.info("This opens to another page.")
    else:
        st.error(f"File {metadata} not found.")