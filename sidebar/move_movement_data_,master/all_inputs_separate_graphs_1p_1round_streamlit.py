import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import pytz

# Set page to wide mode
st.set_page_config(layout="wide")

# Load the datasets
@st.cache_data
def load_player_performance():
    try:
        df = pd.read_csv('final-data/player_performance.csv')
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df = df.dropna(subset=['timestamp'])  # Remove rows with invalid timestamps
        
        # Clean and convert game_round to integer
        df['game_round'] = pd.to_numeric(df['game_round'], errors='coerce')
        df = df.dropna(subset=['game_round'])
        df['game_round'] = df['game_round'].astype(int)
        
        # Clean and convert latency to integer
        df['latency'] = pd.to_numeric(df['latency'], errors='coerce')
        df = df.dropna(subset=['latency'])
        df['latency'] = df['latency'].astype(int)
        
        return df
    except Exception as e:
        st.error(f"Error loading player performance data: {e}")
        return None

@st.cache_data
def load_mouse_data(ip_address):
    try:
        filename = f'{ip_address}_activity_data.csv'
        df = pd.read_csv(filename)
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s', errors='coerce')
        df = df.dropna(subset=['timestamp'])  # Remove rows with invalid timestamps
        return df
    except Exception as e:
        st.error(f"Error loading the mouse movement data for IP {ip_address}: {str(e)}")
        return None

@st.cache_data
def load_event_data(round_number, player_ip):
    try:
        filename = f'final-data/player_performance_per_round.csv/round_{round_number}_player_{player_ip}.csv'
        df = pd.read_csv(filename)
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df = df.dropna(subset=['timestamp'])  # Remove rows with invalid timestamps
        return df
    except Exception as e:
        st.warning(f"No event data available for round {round_number} and player {player_ip}")
        return None

# Load player performance data
player_performance = load_player_performance()

if player_performance is not None and not player_performance.empty:
    # Define timezones
    utc = pytz.UTC
    aest = pytz.timezone('Australia/Sydney')

    # Function to convert timestamp to AEST
    def to_aest(time_obj):
        if time_obj.tzinfo is None:
            time_obj = time_obj.replace(tzinfo=utc)
        return time_obj.astimezone(aest)

    # Convert timestamps for player performance data
    player_performance['timestamp'] = player_performance['timestamp'].apply(to_aest)

    # Get unique latencies and round numbers with latencies and map names
    latencies = sorted(player_performance['latency'].unique())
    round_latencies = player_performance.groupby('game_round').agg({
        'latency': 'first',
        'map': 'first'  # Changed from 'map_name' to 'map'
    }).reset_index()
    round_latencies['round_label'] = round_latencies.apply(lambda row: f"Round {row['game_round']} - {row['map']} - {row['latency']}ms", axis=1)

    # Get unique player IPs
    player_ips = sorted(pd.concat([player_performance['killer_ip'], player_performance['victim_ip']]).unique())

    # User selection
    st.sidebar.header('Filters')
    selected_latencies = st.sidebar.multiselect('Select Latencies', latencies, default=[latencies[0]] if latencies else [])
    
    # Filter rounds based on selected latencies
    filtered_rounds = round_latencies[round_latencies['latency'].isin(selected_latencies)]
    selected_rounds = st.sidebar.multiselect('Select Rounds', filtered_rounds['round_label'].tolist(), 
                                             default=[filtered_rounds['round_label'].iloc[0]] if not filtered_rounds.empty else [])
    
    selected_players = st.sidebar.multiselect('Select Players', player_ips, default=[player_ips[0]] if player_ips else [])

    # Streamlit app
    st.title('Player Input Frequency Visualization')

    if not selected_rounds or not selected_players:
        st.warning("Please select at least one round and one player.")
    else:
        # Function to create frequency data
        def create_frequency_data(data, columns, start_time, end_time):
            data = data.sort_values('timestamp')
            date_range = pd.date_range(start=start_time, end=end_time, freq='s')
            freq_data = pd.DataFrame({'timestamp': date_range})
            
            def get_last_value(group):
                return group.iloc[-1] if len(group) > 0 else 0

            for column in columns:
                grouped = data.groupby(data['timestamp'].dt.floor('S'))[column].apply(get_last_value)
                full_range = pd.date_range(start=grouped.index.min(), end=grouped.index.max(), freq='S')
                filled_data = grouped.reindex(full_range).ffill().reset_index()
                freq_data = pd.merge(freq_data, filled_data, left_on='timestamp', right_on='index', how='left')
                freq_data[column] = freq_data[column].ffill().fillna(0)
                freq_data = freq_data.drop('index', axis=1)

            for column in columns:
                freq_data[f'{column}_diff'] = freq_data[column].diff().fillna(0)
            
            return freq_data

        # Function to find nearest second
        def find_nearest_second(time, freq_data):
            if freq_data.empty or 'normalized_time' not in freq_data.columns:
                return None
            time_diff = np.abs(freq_data['normalized_time'] - time)
            nearest_idx = time_diff.idxmin()
            return freq_data.loc[nearest_idx, 'normalized_time']

        attributes = ['mouse_clicks', 'SPACE', 'A', 'W', 'S', 'D']

        for selected_player in selected_players:
            st.subheader(f"Player {selected_player}")

            # Load mouse data for the selected player
            mouse_keyboard_data = load_mouse_data(selected_player.split('_')[-1])
            if mouse_keyboard_data is None:
                st.warning(f"No mouse/keyboard data available for Player {selected_player}")
                continue

            # Convert timestamps for mouse movement data
            mouse_keyboard_data['timestamp'] = mouse_keyboard_data['timestamp'].apply(to_aest)

            # Multiselect for choosing attributes to display
            selected_attributes = st.multiselect(f'Select attributes to display for Player {selected_player}', 
                                                 attributes, default=attributes, key=f"{selected_player}")

            for attr in selected_attributes:
                fig = go.Figure()

                for round_label in selected_rounds:
                    round_number = int(round_label.split(' - ')[0].split(' ')[1])
                    event_data = load_event_data(round_number, selected_player)
                    if event_data is None or event_data.empty:
                        st.info(f"No event data available for {round_label} and Player {selected_player}")
                        continue

                    # Convert timestamps for event data
                    event_data['timestamp'] = event_data['timestamp'].apply(to_aest)

                    # Filter kill and death data
                    kills_data = event_data[event_data['event'] == 'Kill']
                    deaths_data = event_data[event_data['event'] == 'Death']

                    if kills_data.empty and deaths_data.empty:
                        st.info(f"No kill or death events for {round_label} and Player {selected_player}")
                        continue

                    # Get round start and end times
                    round_start = event_data['timestamp'].min()
                    round_end = event_data['timestamp'].max()

                    # Filter mouse_keyboard_data for the specific round
                    round_data = mouse_keyboard_data[(mouse_keyboard_data['timestamp'] >= round_start) & 
                                                     (mouse_keyboard_data['timestamp'] <= round_end)]

                    if round_data.empty:
                        st.warning(f"No mouse/keyboard data available for the time range of {round_label}")
                        continue

                    # Calculate frequency data
                    freq_data = create_frequency_data(round_data, [attr], round_start, round_end)

                    # Normalize time to start from 0 for the round
                    freq_data['normalized_time'] = (freq_data['timestamp'] - round_start).dt.total_seconds()

                    # Add input frequency line
                    fig.add_trace(go.Scatter(
                        x=freq_data['normalized_time'],
                        y=freq_data[f'{attr}_diff'],
                        mode='lines',
                        name=round_label
                    ))
                    
                    # Function to add events to the plot
                    def add_events(event_data, event_type, marker_symbol):
                        event_times = []
                        event_y_values = []
                        for _, event in event_data.iterrows():
                            event_time = (event['timestamp'] - round_start).total_seconds()
                            nearest_second = find_nearest_second(event_time, freq_data)
                            if nearest_second is not None:
                                event_times.append(nearest_second)
                                event_y_values.append(freq_data.loc[freq_data['normalized_time'] == nearest_second, f'{attr}_diff'].values[0])
                        
                        fig.add_trace(go.Scatter(
                            x=event_times,
                            y=event_y_values,
                            mode='markers',
                            marker=dict(symbol=marker_symbol, size=10),
                            name=f'{event_type}s ({round_label})'
                        ))

                    # Add kill events
                    add_events(kills_data, 'Kill', 'triangle-up')

                    # Add death events
                    add_events(deaths_data, 'Death', 'triangle-down')

                fig.update_layout(
                    title=f'{attr} Input Frequency - Player {selected_player}',
                    xaxis_title='Time (seconds from round start)',
                    yaxis_title='Input Frequency',
                    legend_title='Legend',
                    height=500
                )

                st.plotly_chart(fig, use_container_width=True)

else:
    st.error("Cannot proceed with visualization due to empty or invalid player performance data.")