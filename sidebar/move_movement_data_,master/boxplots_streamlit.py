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

    # Function to calculate input frequencies between events
    def calculate_input_frequencies(player_data, mouse_keyboard_data, event_type, latency):
        events = player_data[player_data['latency'] == latency]
        events = events.sort_values('timestamp')
        
        input_frequencies = {col: [] for col in ['mouse_clicks', 'SPACE', 'A', 'W', 'S', 'D']}
        
        for i in range(1, len(events)):
            start_time = events.iloc[i-1]['timestamp']
            end_time = events.iloc[i]['timestamp']
            
            start_data = mouse_keyboard_data[mouse_keyboard_data['timestamp'] <= start_time].iloc[-1] if not mouse_keyboard_data[mouse_keyboard_data['timestamp'] <= start_time].empty else pd.Series({col: 0 for col in input_frequencies.keys()})
            end_data = mouse_keyboard_data[mouse_keyboard_data['timestamp'] <= end_time].iloc[-1] if not mouse_keyboard_data[mouse_keyboard_data['timestamp'] <= end_time].empty else pd.Series({col: 0 for col in input_frequencies.keys()})
            
            for col in input_frequencies.keys():
                input_frequencies[col].append(end_data[col] - start_data[col])
        
        return input_frequencies

    # Streamlit app
    st.title('Player Performance Box Plot Visualization')

    # Sidebar for selections
    st.sidebar.header('Filters')

    # Player selection
    all_players = pd.concat([player_performance['killer_ip'], player_performance['victim_ip']]).unique()
    selected_players = st.sidebar.multiselect('Select Players', all_players)

    # Latency selection
    all_latencies = sorted(player_performance['latency'].unique())
    selected_latencies = st.sidebar.multiselect('Select Latencies', all_latencies)

    # Map selection
    all_maps = player_performance['map'].unique()
    selected_maps = st.sidebar.multiselect('Select Maps', all_maps)

    # Event type selection
    event_type = st.sidebar.radio("Select Event Type", ('Deaths', 'Kills'))

    # Input columns
    input_columns = ['mouse_clicks', 'SPACE', 'A', 'W', 'S', 'D']

    if selected_players and selected_latencies and selected_maps:
        all_player_data = []

        for player in selected_players:
            st.subheader(f'Performance for {player}')
            player_data = player_performance[(player_performance['killer_ip' if event_type == 'Kills' else 'victim_ip'] == player) & 
                                             (player_performance['map'].isin(selected_maps))]
            mouse_keyboard_data = load_mouse_data(player.split('_')[1])

            if mouse_keyboard_data is None:
                st.warning(f"No mouse movement data available for {player}")
                continue

            mouse_keyboard_data['timestamp'] = pd.to_datetime(mouse_keyboard_data['timestamp'], unit='s').apply(to_aest)

            player_latency_data = []

            for input_col in input_columns:
                fig = go.Figure()

                for latency in selected_latencies:
                    input_frequencies = calculate_input_frequencies(player_data, mouse_keyboard_data, event_type, latency)
                    
                    boxplot = go.Box(y=input_frequencies[input_col], name=f'{latency}ms', boxmean=True)
                    fig.add_trace(boxplot)
                    
                    player_latency_data.extend([(freq, latency, player, input_col) for freq in input_frequencies[input_col]])

                fig.update_layout(title=f'{input_col.capitalize()} Frequency Between {event_type} (Maps: {", ".join(selected_maps)})',
                                  xaxis_title='Latency',
                                  yaxis_title='Frequency',
                                  height=400,
                                  boxmode='group')
                
                # Adjust y-axis to remove scaling
                fig.update_layout(yaxis=dict(tickformat='.2f'))

                st.plotly_chart(fig, use_container_width=True)

                # Add statistical information after each set of boxplots
                st.write(f"### Statistical Insights for {input_col.capitalize()}")
                baseline_latency = min(selected_latencies)
                baseline_data = [freq for freq, lat, _, inp in player_latency_data if lat == baseline_latency and inp == input_col]
                
                for latency in selected_latencies:
                    if latency != baseline_latency:
                        latency_data = [freq for freq, lat, _, inp in player_latency_data if lat == latency and inp == input_col]
                        
                        percent_change = ((np.mean(latency_data) - np.mean(baseline_data)) / np.mean(baseline_data)) * 100
                        t_stat, p_value = stats.ttest_ind(baseline_data, latency_data)
                        
                        st.write(f"At {latency}ms latency compared to {baseline_latency}ms:")
                        st.write(f"- {input_col.capitalize()} frequency {'increased' if percent_change > 0 else 'decreased'} by {abs(percent_change):.2f}%")
                        st.write(f"- T-statistic: {t_stat:.4f}, p-value: {p_value:.4f}")
                        
                        if p_value < 0.05:
                            st.write("  This change is statistically significant.")
                            st.write("  Explanation: The p-value is less than 0.05, which means there is strong evidence to reject the null hypothesis. "
                                     "In other words, the difference in input frequency between the two latencies is unlikely to have occurred by chance.")
                        else:
                            st.write("  This change is not statistically significant.")
                            st.write("  Explanation: The p-value is greater than or equal to 0.05, which means there is not enough evidence to reject the null hypothesis. "
                                     "The difference in input frequency between the two latencies could have occurred by chance.")
                        
                        st.write("  T-statistic explanation: The t-statistic measures the size of the difference relative to the variation in the data. "
                                 "A larger absolute t-value indicates a greater difference between the two latencies.")
                
                st.write("---")

            all_player_data.extend(player_latency_data)

        # Create DataFrame with all player data
        all_player_df = pd.DataFrame(all_player_data, columns=['frequency', 'latency', 'player', 'input'])

        # Display average box plots if more than one player is selected
        if len(selected_players) > 1:
            st.subheader(f'Average Performance Across All Selected Players (Maps: {", ".join(selected_maps)})')
            for input_col in input_columns:
                avg_fig = go.Figure()

                for latency in selected_latencies:
                    latency_data = all_player_df[(all_player_df['latency'] == latency) & (all_player_df['input'] == input_col)]['frequency']
                    avg_fig.add_trace(go.Box(y=latency_data, name=f'{latency}ms', boxmean=True))

                avg_fig.update_layout(title=f'Average {input_col.capitalize()} Frequency Between {event_type} (All Players)',
                                      xaxis_title='Latency',
                                      yaxis_title='Frequency',
                                      height=400)
                
                # Adjust y-axis to remove scaling
                avg_fig.update_layout(yaxis=dict(tickformat='.2f'))

                st.plotly_chart(avg_fig, use_container_width=True)

    else:
        st.warning('Please select at least one player, one latency value, and one map.')

else:
    st.error("Cannot proceed with analysis due to data loading error.")