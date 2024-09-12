import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from scipy import stats

# Set the page to wide mode
st.set_page_config(layout="wide")

# Load the dataset
@st.cache_data
def load_data():
    try:
        player_performance = pd.read_csv('final-data/player_performance.csv')
        return player_performance
    except Exception as e:
        st.error(f"Error loading the player performance data: {str(e)}")
        return None

player_performance = load_data()

if player_performance is not None:
    # Streamlit app
    st.title('Player Performance Box Plot Visualization')

    # Sidebar for selections
    st.sidebar.header('Filters')

    # Player selection
    all_players = pd.concat([player_performance['killer_ip'], player_performance['victim_ip']]).unique()
    selected_players = st.sidebar.multiselect('Select Players', all_players)

    # Map selection
    all_maps = player_performance['map'].unique()
    selected_maps = st.sidebar.multiselect('Select Maps', all_maps)

    # Event type selection
    event_type = st.sidebar.radio("Select Event Type", ('Deaths', 'Kills'))

    # Fixed latencies
    latencies = [0, 50, 100, 150, 200]

    if selected_players and selected_maps:
        # Create summary graph at the top
        st.subheader("Summary: All Selected Players at Different Latencies")
        summary_fig = go.Figure()

        for latency in latencies:
            for player in selected_players:
                player_data = player_performance[
                    (player_performance['killer_ip' if event_type == 'Kills' else 'victim_ip'] == player) & 
                    (player_performance['latency'] == latency) &
                    (player_performance['map'].isin(selected_maps))
                ]
                event_counts = player_data.groupby('map').size().reset_index(name='count')
                
                summary_fig.add_trace(go.Box(
                    y=event_counts['count'],
                    name=f'{player} - {latency}ms',
                    boxmean=True
                ))

        summary_fig.update_layout(
            title=f'Number of {event_type} per Map (All Players)',
            xaxis_title='Player - Latency',
            yaxis_title=f'Number of {event_type}',
            height=600,
            boxmode='group'
        )

        st.plotly_chart(summary_fig, use_container_width=True)

        # Create separate graphs for each player
        for player in selected_players:
            st.subheader(f"Performance for {player}")
            
            fig = go.Figure()
            
            for latency in latencies:
                player_data = player_performance[
                    (player_performance['killer_ip' if event_type == 'Kills' else 'victim_ip'] == player) & 
                    (player_performance['latency'] == latency) &
                    (player_performance['map'].isin(selected_maps))
                ]
                event_counts = player_data.groupby('map').size().reset_index(name='count')
                
                fig.add_trace(go.Box(
                    y=event_counts['count'],
                    name=f'{latency}ms',
                    boxmean=True
                ))

            fig.update_layout(
                title=f'Number of {event_type} per Map for {player}',
                xaxis_title='Latency',
                yaxis_title=f'Number of {event_type}',
                height=500,
                boxmode='group'
            )

            st.plotly_chart(fig, use_container_width=True)

            # Statistical analysis
            st.write("### Statistical Insights")
            baseline_latency = min(latencies)
            
            baseline_data = player_performance[
                (player_performance['killer_ip' if event_type == 'Kills' else 'victim_ip'] == player) & 
                (player_performance['latency'] == baseline_latency) &
                (player_performance['map'].isin(selected_maps))
            ].groupby('map').size().reset_index(name='count')['count']

            for latency in latencies[1:]:  # Skip the baseline latency
                latency_data = player_performance[
                    (player_performance['killer_ip' if event_type == 'Kills' else 'victim_ip'] == player) & 
                    (player_performance['latency'] == latency) &
                    (player_performance['map'].isin(selected_maps))
                ].groupby('map').size().reset_index(name='count')['count']

                percent_change = ((np.mean(latency_data) - np.mean(baseline_data)) / np.mean(baseline_data)) * 100
                t_stat, p_value = stats.ttest_ind(baseline_data, latency_data)

                st.write(f"At {latency}ms latency compared to {baseline_latency}ms:")
                st.write(f"- Average number of {event_type.lower()} {'increased' if percent_change > 0 else 'decreased'} by {abs(percent_change):.2f}%")
                st.write(f"- T-statistic: {t_stat:.4f}, p-value: {p_value:.4f}")

                if p_value < 0.05:
                    st.write("  This change is statistically significant.")
                else:
                    st.write("  This change is not statistically significant.")

            st.write("---")

        # Create average plot for all selected players
        st.subheader("Average Performance Across All Selected Players")
        avg_fig = go.Figure()

        for latency in latencies:
            all_counts = []
            for player in selected_players:
                player_data = player_performance[
                    (player_performance['killer_ip' if event_type == 'Kills' else 'victim_ip'] == player) & 
                    (player_performance['latency'] == latency) &
                    (player_performance['map'].isin(selected_maps))
                ]
                event_counts = player_data.groupby('map').size().reset_index(name='count')
                all_counts.extend(event_counts['count'])

            avg_fig.add_trace(go.Box(
                y=all_counts,
                name=f'{latency}ms',
                boxmean=True
            ))

        avg_fig.update_layout(
            title=f'Average Number of {event_type} per Map (All Selected Players)',
            xaxis_title='Latency',
            yaxis_title=f'Number of {event_type}',
            height=500,
            boxmode='group'
        )

        st.plotly_chart(avg_fig, use_container_width=True)

    else:
        st.warning('Please select at least one player and one map.')

else:
    st.error("Cannot proceed with analysis due to data loading error.")