import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Latency Analysis", page_icon="📊", layout="wide")

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

    st.title('Players\' Mean Scores vs Latency Statistical Analysis')

    latency_values = list(result_dfs.keys())
    selected_latency = st.selectbox('Select Latency Value (ms)', latency_values, index=0)

    st.subheader(f'Statistics for Latency {selected_latency}')
    st.dataframe(result_dfs[selected_latency])

    # Create an interactive line plot
    fig = go.Figure()

    for player_ip in df['player_ip'].unique():
        means = [result_dfs[latency].loc[player_ip, 'Mean'] for latency in result_dfs.keys() if player_ip in result_dfs[latency].index]
        fig.add_trace(go.Scatter(x=list(result_dfs.keys()), y=means, mode='lines+markers', name=f'Player {player_ip}'))

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
        height=650,  # Slightly reduced height
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(size=10)  # Reduced font size for legend
        ),
        margin=dict(t=100)  # Increased top margin to accommodate centered legend
    )

    st.plotly_chart(fig, use_container_width=True)

    # Additional information
    # st.write("Note: This chart shows how each player's mean score changes with different latency values. "
    #          "Each line represents a player, allowing you to compare performance across latencies.")

else:
    st.error("Cannot proceed with analysis due to data loading error.")

# Display available columns
# st.subheader("Available Data Columns")
# if df is not None:
#     st.write(f"Columns in the dataset: {', '.join(df.columns)}")
# else:
#     st.write("Data not available.")