import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import pytz
from scipy import stats

# Set page to wide mode
st.set_page_config(layout="wide")

# Load the datasets
@st.cache_data
def load_player_performance():
    try:
        df = pd.read_csv('final-data/player_performance.csv')
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df = df.dropna(subset=['timestamp'])  # Remove rows with invalid timestamps
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

# Load player performance data
player_performance = load_player_performance()

if player_performance is not None:
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

    # Get unique player IPs
    player_ips = sorted(pd.concat([player_performance['killer_ip'], player_performance['victim_ip']]).unique())

    # Streamlit app
    st.title('Latency Comparison Visualization')

    # User selection
    st.sidebar.header('Filters')
    selected_player = st.sidebar.selectbox('Select Player', player_ips)

    # Load mouse data for the selected player
    mouse_keyboard_data = load_mouse_data(selected_player.split('_')[-1])

    if mouse_keyboard_data is not None:
        # Convert timestamps for mouse movement data
        mouse_keyboard_data['timestamp'] = mouse_keyboard_data['timestamp'].apply(to_aest)

        # Filter performance data for selected player
        kills_data = player_performance[player_performance['killer_ip'] == selected_player]
        deaths_data = player_performance[player_performance['victim_ip'] == selected_player]

        # Get latency changes
        latency_changes = player_performance[player_performance['latency'] != player_performance['latency'].shift(1)]
        latency_changes = latency_changes[latency_changes['killer_ip'] == selected_player]

        # If there are multiple entries with 0ms latency, keep only the one with more events
        zero_latency_data = latency_changes[latency_changes['latency'] == 0]
        if len(zero_latency_data) > 1:
            events_count = zero_latency_data.apply(lambda row: 
                len(kills_data[(kills_data['timestamp'] >= row['timestamp']) & 
                               (kills_data['timestamp'] < row['timestamp'] + timedelta(minutes=10))]) + 
                len(deaths_data[(deaths_data['timestamp'] >= row['timestamp']) & 
                                (deaths_data['timestamp'] < row['timestamp'] + timedelta(minutes=10))]),
                axis=1)
            keep_index = events_count.idxmax()
            latency_changes = latency_changes[~((latency_changes['latency'] == 0) & (latency_changes.index != keep_index))]

        st.write("Latency changes:")
        st.write(latency_changes[['timestamp', 'latency']])

        # Function to create frequency data
        def create_frequency_data(data, column, start_time):
            data = data.sort_values('timestamp')
            date_range = pd.date_range(start=start_time, periods=600, freq='s')
            freq_data = pd.DataFrame({'timestamp': date_range})
            
            def get_last_value(group):
                return group.iloc[-1] if len(group) > 0 else 0

            grouped = data.groupby(data['timestamp'].dt.floor('S'))[column].apply(get_last_value)
            full_range = pd.date_range(start=grouped.index.min(), end=grouped.index.max(), freq='S')
            filled_data = grouped.reindex(full_range).ffill().reset_index()
            freq_data = pd.merge(freq_data, filled_data, left_on='timestamp', right_on='index', how='left')
            freq_data[column] = freq_data[column].ffill().fillna(0)
            freq_data = freq_data.drop('index', axis=1)

            freq_data[f'{column}_diff'] = freq_data[column].diff().fillna(0)
            
            return freq_data

        # Function to find nearest second
        def find_nearest_second(time, freq_data):
            if freq_data.empty or 'normalized_time' not in freq_data.columns:
                return None
            time_diff = np.abs(freq_data['normalized_time'] - time)
            nearest_idx = time_diff.idxmin()
            return freq_data.loc[nearest_idx, 'normalized_time']

        # Function to remove outliers
        def remove_outliers(data, column, z_threshold=3):
            z_scores = np.abs(stats.zscore(data[column]))
            return data[z_scores < z_threshold]

        # Function to plot comparison
        def plot_comparison(zero_latency_data, other_latency_data, other_latency_value, kills_data, deaths_data, input_type):
            fig = go.Figure()

            # Plot 0 latency data
            fig.add_trace(go.Scatter(x=zero_latency_data['normalized_time'], y=zero_latency_data[f'{input_type}_diff'],
                                     mode='lines', name='Latency: 0', line=dict(color='blue', width=2)))
            
            # Plot other latency data
            fig.add_trace(go.Scatter(x=other_latency_data['normalized_time'], y=other_latency_data[f'{input_type}_diff'],
                                     mode='lines', name=f'Latency: {other_latency_value}', line=dict(color='red', width=2)))
            
            # Add kill events
            for _, kill in kills_data.iterrows():
                kill_time = (kill['timestamp'] - zero_latency_data['timestamp'].iloc[0]).total_seconds()
                nearest_second = find_nearest_second(kill_time, zero_latency_data)
                if nearest_second is not None:
                    fig.add_trace(go.Scatter(x=[nearest_second], 
                                             y=[zero_latency_data.loc[zero_latency_data['normalized_time'] == nearest_second, f'{input_type}_diff'].values[0]],
                                             mode='markers', marker=dict(symbol='triangle-up', size=10, color='blue'), 
                                             name='Kill (0ms)', showlegend=False))
            
            # Add death events
            for _, death in deaths_data.iterrows():
                death_time = (death['timestamp'] - zero_latency_data['timestamp'].iloc[0]).total_seconds()
                nearest_second = find_nearest_second(death_time, zero_latency_data)
                if nearest_second is not None:
                    fig.add_trace(go.Scatter(x=[nearest_second], 
                                             y=[zero_latency_data.loc[zero_latency_data['normalized_time'] == nearest_second, f'{input_type}_diff'].values[0]],
                                             mode='markers', marker=dict(symbol='triangle-down', size=10, color='blue'), 
                                             name='Death (0ms)', showlegend=False))
            
            fig.update_layout(
                title=f'{input_type.capitalize()} Input Frequency - 0ms vs {other_latency_value}ms',
                xaxis_title="Time (seconds from start of latency period)",
                yaxis_title=f"Change in {input_type.capitalize()} Inputs per Second",
                legend_title="Latency",
                height=400
            )

            return fig

        # Create visualizations
        input_columns = ['mouse_clicks', 'SPACE', 'A', 'W', 'S', 'D']

        # Check if there's 0ms latency data
        zero_latency_data = latency_changes[latency_changes['latency'] == 0]
        if zero_latency_data.empty:
            st.warning("No 0ms latency data available for this player. Unable to create comparison visualizations.")
        else:
            zero_latency = zero_latency_data.iloc[0]
            zero_start = zero_latency['timestamp'].floor('S')
            zero_end = zero_start + timedelta(minutes=10)
            zero_period_data = mouse_keyboard_data[(mouse_keyboard_data['timestamp'] >= zero_start) & (mouse_keyboard_data['timestamp'] < zero_end)]

            non_zero_latencies = latency_changes[latency_changes['latency'] != 0]

            for input_type in input_columns:
                zero_freq_data = create_frequency_data(zero_period_data, input_type, zero_start)
                zero_freq_data['normalized_time'] = (zero_freq_data['timestamp'] - zero_start).dt.total_seconds()
                zero_freq_data = remove_outliers(zero_freq_data, f'{input_type}_diff')

                st.subheader(f'{input_type.capitalize()} Input Comparisons')

                if non_zero_latencies.empty:
                    st.info(f"No non-zero latency data available for comparison with 0ms latency for {input_type}.")
                else:
                    for _, change in non_zero_latencies.iterrows():
                        start = change['timestamp'].floor('S')
                        end = start + timedelta(minutes=10)
                        
                        period_data = mouse_keyboard_data[(mouse_keyboard_data['timestamp'] >= start) & (mouse_keyboard_data['timestamp'] < end)]
                        freq_data = create_frequency_data(period_data, input_type, start)
                        freq_data['normalized_time'] = (freq_data['timestamp'] - start).dt.total_seconds()
                        freq_data = remove_outliers(freq_data, f'{input_type}_diff')
                        
                        period_kills = kills_data[(kills_data['timestamp'] >= zero_start) & (kills_data['timestamp'] < zero_end)]
                        period_deaths = deaths_data[(deaths_data['timestamp'] >= zero_start) & (deaths_data['timestamp'] < zero_end)]
                        
                        fig = plot_comparison(zero_freq_data, freq_data, change['latency'], period_kills, period_deaths, input_type)
                        st.plotly_chart(fig, use_container_width=True)

    else:
        st.error("Cannot proceed with visualization due to data loading error.")

else:
    st.error("Cannot proceed with visualization due to player performance data loading error.")