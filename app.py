# app.py
import streamlit as st
from src.log_parser import LogParser
import src.ui_components as ui
import plotly.express as px
import requests

# Streamlit app interface
st.title("Log File Parser with Interactive Curve Diagrams")
uploaded_file = st.file_uploader("Choose a log file", type="log")

if uploaded_file:
    # Read file and parse
    file_content = uploaded_file.read().decode("utf-8")
    logparser = LogParser(file_content)
    records_dfs = logparser.parse_log()

    if records_dfs:
    
        # Display each record's data and plot
        for index, record_df in enumerate(records_dfs, start=1):
            # Calculate velocity and update DataFrame
            record_df = ui.calculate_velocity(record_df)

            ui.display_data_table(record_df, f"Data for Record {index}:")

            # Plot sampling interval analysis
            ui.display_sampling_interval_analysis(record_df, index)

            # Let user select X and Y axes
            ui.select_and_plot_curve(record_df, index)
    else:
        st.write("No records found under '[Recorded curves]'.")

ui.display_footer(app_version="0.1",company_name="Festo SE & Co. KG")