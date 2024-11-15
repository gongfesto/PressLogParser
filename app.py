import streamlit as st
import re
import pandas as pd
import plotly.express as px

# Define function to parse log and extract multiple records under "[Recorded curves]"
def parse_log(file_content) -> list[pd.DataFrame]:
    records = []
    record_section = False
    current_record = None

    for line in file_content.splitlines():
        if "[Recorded curves]" in line:
            record_section = True
        elif "[Variables]" in line:  # End of recorded curves section
            record_section = False

        # Extract records within "[Recorded curves]"
        if record_section:
            if line.startswith("[Record "):
                # Start a new record
                current_record = {"points": []}
                records.append(current_record)
            elif re.match(r"^\d+;\d+\.\d+;\d+\.\d+;T#\d+m\d+s\d+ms", line):
                # Parse points within the current record
                fields = line.split(";")
                point, position, force, time = int(fields[0]), float(fields[1]), float(fields[2]), fields[3]
                current_record["points"].append({"Point": point, "Position": position, "Force": force, "Time": time})

    # Convert records into a list of dataframes
    record_dfs = [pd.DataFrame(record["points"]) for record in records if "points" in record]
    return record_dfs

# Streamlit app interface
st.title("Log File Parser with Interactive Curve Diagrams")
uploaded_file = st.file_uploader("Choose a log file", type="log")

if uploaded_file:
    # Read file and parse
    file_content = uploaded_file.read().decode("utf-8")
    records_dfs = parse_log(file_content)

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
