import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
    # Define timezones
    utc = pytz.UTC
    aest = pytz.timezone('Australia/Sydney')

    # Function to convert timestamp to AEST
    def to_aest(time_obj):
        if isinstance(time_obj, str):
            time_obj = pd.to_datetime(time_obj)
        if time_obj.tzinfo is None:
            time_obj = time_obj.tz_localize(utc)
        return time_obj.astimezone(aest)

    # Convert timestamps for player performance data
    player_performance['timestamp'] = pd.to_datetime(player_performance['timestamp']).apply(to_aest)

    # Function to create frequency data
    def create_frequency_data(data, columns, start_time):
        data = data.sort_values('timestamp')
        date_range = pd.date_range(start=start_time, periods=600, freq='s')
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

    # Function to remove outliers
    def remove_outliers(data, column, z_threshold=3):
        z_scores = np.abs(stats.zscore(data[column]))
        return data[z_scores < z_threshold]

    # Streamlit app
    st.title('Player Performance Visualization')

    # Sidebar for player and latency selection
    st.sidebar.header('Filters')

    # Player selection
    all_players = pd.concat([player_performance['killer_ip'], player_performance['victim_ip']]).unique()
    selected_players = st.sidebar.multiselect('Select Players', all_players)

    # Latency selection
    all_latencies = player_performance['latency'].unique()
    selected_latencies = st.sidebar.multiselect('Select Latencies', all_latencies)

    # Input columns
    input_columns = ['mouse_clicks', 'SPACE', 'A', 'W', 'S', 'D']

    # Define a color map for latencies
    color_map = {
        0: 'green',
        50: 'yellow',
        100: 'orange',
        150: 'pink',
        200: 'red',
    }

    if selected_players and selected_latencies:
        for player in selected_players:
            st.subheader(f'Performance for {player}')

            # Load mouse movement data for this player
            mouse_keyboard_data = load_mouse_data(player.split('_')[1])  # Assuming player is in format "Player_IP"
            
            if mouse_keyboard_data is None:
                st.warning(f"No mouse movement data available for {player}")
                continue

            # Convert timestamps for mouse movement data
            mouse_keyboard_data['timestamp'] = pd.to_datetime(mouse_keyboard_data['timestamp'], unit='s').apply(to_aest)

            # Filter data for the selected player
            kills_data = player_performance[player_performance['killer_ip'] == player]
            deaths_data = player_performance[player_performance['victim_ip'] == player]

            # Create a figure for each player
            fig = make_subplots(rows=len(input_columns), cols=1, 
                                shared_xaxes=True, 
                                vertical_spacing=0.05,
                                subplot_titles=[f'{col.capitalize()} Events per Second' for col in input_columns])

            for idx, col in enumerate(input_columns):
                for latency in selected_latencies:
                    # Filter data for this latency
                    latency_data = player_performance[(player_performance['killer_ip'] == player) & 
                                                      (player_performance['latency'] == latency)]
                    
                    if not latency_data.empty:
                        start = latency_data['timestamp'].min()
                        end = start + timedelta(minutes=10)
                        
                        # Filter data for this latency period
                        period_data = mouse_keyboard_data[(mouse_keyboard_data['timestamp'] >= start) & 
                                                          (mouse_keyboard_data['timestamp'] <= end)]
                        
                        # Create frequency data
                        freq_data = create_frequency_data(period_data, input_columns, start)
                        
                        # Normalize time to start from 0 for each period
                        freq_data['normalized_time'] = (freq_data['timestamp'] - start).dt.total_seconds()
                        
                        # Remove outliers
                        freq_data = remove_outliers(freq_data, f'{col}_diff')
                        
                        # Plot the data
                        fig.add_trace(go.Scatter(x=freq_data['normalized_time'], 
                                                 y=freq_data[f'{col}_diff'],
                                                 mode='lines', 
                                                 name=f'Latency: {latency}ms',
                                                 line=dict(color=color_map.get(latency, 'gray'))),
                                      row=idx+1, col=1)
                        
                        # Add kill events
                        period_kills = kills_data[(kills_data['timestamp'] >= start) & (kills_data['timestamp'] <= end)]
                        kill_times = [(kill['timestamp'] - start).total_seconds() for _, kill in period_kills.iterrows()]
                        kill_y = [freq_data.loc[freq_data['normalized_time'] == find_nearest_second(kt, freq_data), f'{col}_diff'].values[0] 
                                  if find_nearest_second(kt, freq_data) is not None else None for kt in kill_times]
                        fig.add_trace(go.Scatter(x=kill_times, y=kill_y, mode='markers', 
                                                 marker=dict(symbol='triangle-up', size=10, color=color_map.get(latency, 'gray')),
                                                 name=f'Kills ({latency}ms)',
                                                 showlegend=False),
                                      row=idx+1, col=1)
                        
                        # Add death events
                        period_deaths = deaths_data[(deaths_data['timestamp'] >= start) & (deaths_data['timestamp'] <= end)]
                        death_times = [(death['timestamp'] - start).total_seconds() for _, death in period_deaths.iterrows()]
                        death_y = [freq_data.loc[freq_data['normalized_time'] == find_nearest_second(dt, freq_data), f'{col}_diff'].values[0]
                                   if find_nearest_second(dt, freq_data) is not None else None for dt in death_times]
                        fig.add_trace(go.Scatter(x=death_times, y=death_y, mode='markers',
                                                 marker=dict(symbol='triangle-down', size=10, color=color_map.get(latency, 'gray')),
                                                 name=f'Deaths ({latency}ms)',
                                                 showlegend=False),
                                      row=idx+1, col=1)

                fig.update_xaxes(title_text='Time (seconds from start of latency period)', range=[0, 600], row=idx+1, col=1)
                fig.update_yaxes(title_text='Events per Second', row=idx+1, col=1)
                
                # Add legend for each subplot
                fig.update_layout({f'legend{idx+1}': dict(
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )})

            fig.update_layout(height=300*len(input_columns), 
                              title_text=f"Player Performance Visualization for {player}",
                              legend_tracegroupgap=5)  # Adjust legend spacing

            st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning('Please select at least one player and one latency value.')

else:
    st.error("Cannot proceed with analysis due to data loading error.")