import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def show_latency():
    @st.cache_data
    def load_data():
        try:
            return pd.read_csv('final-data/round_summary_adjusted.csv')
        except Exception as e:
            st.error(f"Error loading the data: {str(e)}")
            return None

    df = load_data()

    if df is not None:
        def generate_statistics(df):
            grouped = df.groupby('latency')
            result_dfs = {}
            
            for latency, group in grouped:
                unique_player_ips = group['player_ip'].unique()
                latency_df = pd.DataFrame(index=unique_player_ips)
                
                group = group[group['latency'] == latency]
                
                for game_round in group['game_round'].unique():
                    round_scores = group[group['game_round'] == game_round].set_index('player_ip')['score'].rename(f'Round_{game_round}')
                    latency_df = latency_df.join(round_scores, how='left')
                
                latency_df['Mean'] = latency_df.mean(axis=1)
                latency_df['StdDev'] = latency_df.std(axis=1)
                
                if 0 in result_dfs:
                    latency_df['mean_difference'] = latency_df['Mean'] - result_dfs[0]['Mean']
                else:
                    latency_df['mean_difference'] = 0
                
                result_dfs[latency] = latency_df
            
            return result_dfs

        result_dfs = generate_statistics(df)

        # st.title('Players\' Mean Scores vs Latency Statistical Analysis')

        # Create checkboxes for latency values
        st.sidebar.subheader('Select Latency Values (ms)')
        latency_values = list(result_dfs.keys())
        selected_latencies = {latency: st.sidebar.checkbox(str(latency), value=True) for latency in latency_values}

        # Create checkboxes for players
        st.sidebar.subheader('Select Players')
        all_players = df['player_ip'].unique()
        selected_players = {player: st.sidebar.checkbox(f'Player {player}', value=True) for player in all_players}

        # Create an interactive line plot
        fig = go.Figure()

        for player_ip in all_players:
            if selected_players[player_ip]:
                means = [result_dfs[latency].loc[player_ip, 'Mean'] for latency in latency_values if player_ip in result_dfs[latency].index and selected_latencies[latency]]
                latencies = [latency for latency in latency_values if player_ip in result_dfs[latency].index and selected_latencies[latency]]
                fig.add_trace(go.Scatter(x=latencies, y=means, mode='lines+markers', name=f'Player {player_ip}'))

        fig.update_layout(
            title={
                'text': 'Players\' Mean Scores vs Latency',
                'y':0.98,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 20}
            },
            xaxis_title='Latency',
            yaxis_title='Mean Score',
            height=650,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                font=dict(size=10)
            ),
            margin=dict(t=100)
        )

        st.plotly_chart(fig, use_container_width=True)

        # Display statistics for selected latencies
        st.subheader('Statistics for Selected Latencies')
        for latency in latency_values:
            if selected_latencies[latency]:
                st.write(f'Latency {latency}')
                st.dataframe(result_dfs[latency])

    else:
        st.error("Cannot proceed with analysis due to data loading error.")