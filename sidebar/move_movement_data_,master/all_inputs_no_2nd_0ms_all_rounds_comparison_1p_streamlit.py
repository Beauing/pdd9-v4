import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import pytz
from scipy import stats

# Set the page to wide mode
st.set_page_config(layout="wide")

# Load the datasets
@st.cache_data
def load_data():
    try:
        player_performance = pd.read_csv('final-data/player_performance.csv')
        return player_performance
    except Exception as e:
        st.error(f"Error loading the player performance data: {str(e)}")
        return None

@st.cache_data
def load_mouse_data(ip_address):
    try:
        filename = f'{ip_address}_activity_data.csv'
        return pd.read_csv(filename)
    except Exception as e:
        st.error(f"Error loading the mouse movement data for IP {ip_address}: {str(e)}")
        return None

player_performance = load_data()

if player_performance is not None:
    # Define timezones and conversion function
    aest = pytz.timezone('Australia/Sydney')
    def to_aest(time_obj):
        return pd.to_datetime(time_obj).dt.tz_localize('UTC').dt.tz_convert(aest)

    # Convert timestamps for player performance data
    player_performance['timestamp'] = to_aest(player_performance['timestamp'])

    # Streamlit app
    st.title('Player Performance Comparison')

    # Sidebar for player and latency selection
    st.sidebar.header('Filters')
    all_players = pd.concat([player_performance['killer_ip'], player_performance['victim_ip']]).unique()
    selected_player = st.sidebar.selectbox('Select Player', all_players)
    all_latencies = sorted(player_performance['latency'].unique())
    selected_latencies = st.sidebar.multiselect('Select Latencies', all_latencies, default=all_latencies)

    # Color map for latencies
    color_map = {
        0: 'green', 50: 'yellow', 100: 'orange', 150: 'pink', 200: 'red',
    }

    # Load mouse movement data for the selected player
    ip_address = selected_player.split('_')[-1]
    mouse_keyboard_data = load_mouse_data(ip_address)
    
    if mouse_keyboard_data is None:
        st.warning(f"No mouse movement data available for {selected_player}")
    else:
        # Convert timestamps for mouse movement data
        mouse_keyboard_data['timestamp'] = to_aest(pd.to_datetime(mouse_keyboard_data['timestamp'], unit='s'))

        # Filter kill and death data for the selected player
        kills_data = player_performance[player_performance['killer_ip'] == selected_player]
        deaths_data = player_performance[player_performance['victim_ip'] == selected_player]

        # Function to create frequency data
        def create_frequency_data(data, columns, start_time):
            data = data.sort_values('timestamp')
            date_range = pd.date_range(start=start_time, periods=600, freq='s')
            freq_data = pd.DataFrame({'timestamp': date_range})
            
            for column in columns:
                grouped = data.groupby(data['timestamp'].dt.floor('S'))[column].last()
                full_range = pd.date_range(start=grouped.index.min(), end=grouped.index.max(), freq='S')
                filled_data = grouped.reindex(full_range).ffill().reset_index()
                freq_data = pd.merge(freq_data, filled_data, left_on='timestamp', right_on='index', how='left')
                freq_data[column] = freq_data[column].ffill().fillna(0)
                freq_data = freq_data.drop('index', axis=1)

            freq_data['total_inputs'] = freq_data[columns].sum(axis=1)
            freq_data['total_inputs_diff'] = freq_data['total_inputs'].diff().fillna(0)
            return freq_data

        # Function to remove outliers
        def remove_outliers(data, column, z_threshold=3):
            z_scores = np.abs(stats.zscore(data[column]))
            return data[z_scores < z_threshold]

        # Create visualization
        input_columns = ['mouse_clicks', 'SPACE', 'A', 'W', 'S', 'D']
        fig = go.Figure()

        for latency in selected_latencies:
            latency_data = player_performance[(player_performance['killer_ip'] == selected_player) & 
                                              (player_performance['latency'] == latency)]
            
            if not latency_data.empty:
                start = latency_data['timestamp'].min()
                end = start + timedelta(minutes=10)
                
                period_data = mouse_keyboard_data[(mouse_keyboard_data['timestamp'] >= start) & 
                                                  (mouse_keyboard_data['timestamp'] < end)]
                
                freq_data = create_frequency_data(period_data, input_columns, start)
                freq_data['normalized_time'] = (freq_data['timestamp'] - start).dt.total_seconds()
                freq_data = remove_outliers(freq_data, 'total_inputs_diff')
                
                # Remove NaN values
                freq_data = freq_data.dropna(subset=['normalized_time', 'total_inputs_diff'])
                
                fig.add_trace(go.Scatter(
                    x=freq_data['normalized_time'], 
                    y=freq_data['total_inputs_diff'],
                    mode='lines',
                    name=f'Latency: {latency}ms',
                    line=dict(color=color_map.get(latency, 'gray'), width=2),
                    opacity=0.7
                ))

                # Add kill events
                period_kills = kills_data[(kills_data['timestamp'] >= start) & (kills_data['timestamp'] < end)]
                kill_times = [(kill['timestamp'] - start).total_seconds() for _, kill in period_kills.iterrows()]
                kill_y = [freq_data.loc[freq_data['normalized_time'] == time, 'total_inputs_diff'].values[0] 
                          if time in freq_data['normalized_time'].values else None for time in kill_times]
                fig.add_trace(go.Scatter(
                    x=kill_times, 
                    y=kill_y, 
                    mode='markers',
                    marker=dict(symbol='triangle-up', size=10, color=color_map.get(latency, 'gray')),
                    name=f'Kills ({latency}ms)',
                    showlegend=False
                ))

                # Add death events
                period_deaths = deaths_data[(deaths_data['timestamp'] >= start) & (deaths_data['timestamp'] < end)]
                death_times = [(death['timestamp'] - start).total_seconds() for _, death in period_deaths.iterrows()]
                death_y = [freq_data.loc[freq_data['normalized_time'] == time, 'total_inputs_diff'].values[0]
                           if time in freq_data['normalized_time'].values else None for time in death_times]
                fig.add_trace(go.Scatter(
                    x=death_times, 
                    y=death_y, 
                    mode='markers',
                    marker=dict(symbol='triangle-down', size=10, color=color_map.get(latency, 'gray')),
                    name=f'Deaths ({latency}ms)',
                    showlegend=False
                ))

        fig.update_layout(
            title=f'Change in Total Input Events per Second for {selected_player} (First 10 Minutes)',
            xaxis_title='Time (seconds from start of latency period)',
            yaxis_title='Change in Total Inputs per Second',
            xaxis_range=[0, 600],
            legend_title='Latency',
            height=600,
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
        )

        st.plotly_chart(fig, use_container_width=True)

        # Display diagnostic information
        st.subheader("Data Ranges:")
        st.write(f"Mouse and Keyboard Data: {mouse_keyboard_data['timestamp'].min()} to {mouse_keyboard_data['timestamp'].max()}")
        st.write(f"Player Performance Data: {player_performance['timestamp'].min()} to {player_performance['timestamp'].max()}")

else:
    st.error("Cannot proceed with analysis due to data loading error.")