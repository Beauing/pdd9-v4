import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def show_demographic():

    csv_file = 'survey-data/demographics.csv'

    def preprocess_data(df):
        for column in df.columns:
            if df[column].dtype == 'object':
                df[column] = df[column].str.split(',')
        return df

    def plot_overall_chart(df, column_name):
        if isinstance(df[column_name].iloc[0], list):
            # Multiple choice question
            temp_df = df[column_name].explode()
            counts = temp_df.value_counts(dropna=True)
            fig = px.bar(
                x=counts.index,
                y=counts.values,
                title=f'Distribution of {column_name}',
                labels={'x': 'Response', 'y': 'Count'},
            )
        else:
            # Single choice question
            counts = df[column_name].value_counts(dropna=True)
            fig = px.bar(
                x=counts.index,
                y=counts.values,
                title=f'Distribution of {column_name}',
                labels={'x': 'Response', 'y': 'Count'},
            )

        fig.update_layout(xaxis_tickangle=-45, height=400, width=600)
        
        # Calculate percentage for each category
        total = counts.sum()
        percentages = (counts / total * 100).round(1)
        
        # Add percentage labels on top of each bar
        for i, (value, percentage) in enumerate(zip(counts, percentages)):
            fig.add_annotation(
                x=counts.index[i],
                y=value,
                text=f"{percentage}%",
                showarrow=False,
                yshift=10
            )

        # Determine the Majority
        dominant_choice = counts.index[0]
        dominant_percentage = percentages.iloc[0]

        return fig, dominant_choice, dominant_percentage

    def display_individual_summary(df, player_index):
        st.subheader(f"Player {player_index + 1} Summary")
        for column in df.columns:
            value = df.iloc[player_index][column]
            if isinstance(value, list):
                value = ', '.join(value)
            st.write(f"**{column}:** {value}")

    @st.cache_data
    def load_data():
        try:
            df = pd.read_csv(csv_file)
            return preprocess_data(df)
        except FileNotFoundError:
            st.error(f"File not found: {csv_file}")
            return None
        except pd.errors.EmptyDataError:
            st.error(f"The file {csv_file} is empty.")
            return None
        except Exception as e:
            st.error(f"An error occurred while reading the file: {str(e)}")
            return None

    st.title('Demographic Overview')

    df = load_data()

    if df is not None:        
        # Use streamlit-option-menu instead of tabs
        selected = option_menu(
            menu_title=None,
            options=["Overall", "Individual"],
            icons=["bar-chart-fill", "person-fill"],  # Bootstrap icons
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
        )
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Number of Participants", len(df))
        with col2:
            st.metric("Number of Questions", len(df.columns))
        
        if selected == "Overall":
            columns_to_plot = st.multiselect(
                'Select Questions to Analyze',
                df.columns,
                default="What platforms do you use to play games? (e.g., PC, console, mobile)"
            )
            
            if columns_to_plot:
                for column in columns_to_plot:
                    fig, dominant_choice, dominant_percentage = plot_overall_chart(df, column)
                    st.plotly_chart(fig, use_container_width=True)
                    st.info(f"Most common response: {dominant_choice} ({dominant_percentage:.1f}%)")
            else:
                st.warning("Please select at least one question to analyse.")
        
        elif selected == "Individual":
            player_index = st.selectbox("Select Player", range(len(df)), format_func=lambda x: f"Player {x + 1}")
            display_individual_summary(df, player_index)