import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

csv_file = 'survey-data/demographics.csv'

st.set_option('deprecation.showPyplotGlobalUse', False)

# Function to plot pie chart for a categorical column
def plot_pie_chart(column_name):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)
    
    # Count unique values for the column, excluding NaN
    counts = df[column_name].value_counts(dropna=True)
    
    # Plotting the pie chart
    plt.figure(figsize=(8, 6))
    counts.plot.pie(autopct='%1.1f%%', startangle=140)
    plt.title(f'Distribution of {column_name}')
    plt.ylabel('')  # Remove the default ylabel 'column_name'
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot()

    # Streamlit app
def main():
    st.title('Participant Analysis')
    st.info('Pie Charts of CSV Columns')
    
    # Display column selection and pie charts
    df = pd.read_csv(csv_file)
    columns_to_plot = st.multiselect('Select Columns to Plot', df.columns)
    
    if columns_to_plot:
        for column in columns_to_plot:
            plot_pie_chart(column)

main()

#beau's code