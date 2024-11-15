import streamlit as st
from src.log_parser import LogParser
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
            st.write(f"Data for Record {index}:")
            st.dataframe(record_df)

            # Allow user to select x and y axis for plotting for each record
            x_axis = st.selectbox(f"Select X axis for Record {index}:", options=record_df.columns, index=1, key=f"x_axis_{index}")
            y_axis = st.selectbox(f"Select Y axis for Record {index}:", options=record_df.columns, index=2, key=f"y_axis_{index}")

            # Plot the interactive curve using Plotly for each record
            st.write(f"{x_axis} vs. {y_axis} Curve for Record {index}")
            fig = px.line(record_df, x=x_axis, y=y_axis, markers=True, title=f"{x_axis} vs. {y_axis} Curve for Record {index}")
            fig.update_traces(mode="lines+markers")
            fig.update_layout(xaxis_title=x_axis, yaxis_title=y_axis, hovermode='x unified')

            # Display the plot in Streamlit
            st.plotly_chart(fig)
    else:
        st.write("No records found under '[Recorded curves]'.")
