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
if 'file_uploaded' not in st.session_state:
    st.session_state.file_uploaded = False
if 'operation_completed' not in st.session_state:
    st.session_state.operation_completed = False
if 'import_button_clicked' not in st.session_state:
    st.session_state.import_button_clicked = False

# Set paths
run_script = "run_all.py"
input_file_path = "processes/1_start.py"

if not st.session_state.file_uploaded:
    # Import button
    uploaded_file = st.file_uploader("Import File")

    # Save the uploaded file and set the input path for the first script
    if uploaded_file:
        input_file_name = uploaded_file.name
        input_file_path = os.path.join("import", input_file_name)
        
        os.makedirs("import", exist_ok=True)
        with open(input_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.session_state.file_uploaded = True

# Check if a file has been uploaded
file_uploaded = st.session_state.file_uploaded

if file_uploaded and not st.session_state.operation_completed:
    if not st.session_state.import_button_clicked:
        if st.button("Import"):
            st.session_state.import_button_clicked = True
            
            # Update the input path in 1_start.py
            with open("processes/1_start.py", "r") as file:
                script_content = file.read()

            script_content = script_content.replace("input_path = ''", f"input_path = '{input_file_path}'")

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
                # display_temporary_message(f"{run_script} completed successfully.", 'success', duration=3)
                # st.text(result.stdout)
                
                st.session_state.operation_completed = True
                                
                if st.button("Upload a new file"):
                    st.session_state.file_uploaded = False
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