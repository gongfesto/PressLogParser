# app.py
import streamlit as st
from src.log_parser import LogParser
import src.ui_components as ui
import plotly.express as px


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

            x_axis, y_axes = ui.select_axis(record_df, index)

            ui.plot_curve(record_df, x_axis, y_axes, f"{x_axis} vs. {y_axes} Curve for Record {index}" )
    else:
        st.write("No records found under '[Recorded curves]'.")
