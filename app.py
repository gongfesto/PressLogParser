import streamlit as st
import re
import pandas as pd
import plotly.express as px

# Define function to parse log and extract records under "[Recorded curves]"
def parse_log(file_content):
    records = []
    record_section = False

    for line in file_content.splitlines():
        if "[Recorded curves]" in line:
            record_section = True
        elif "[Variables]" in line:  # End of recorded curves section
            record_section = False

        # Extract records within "[Recorded curves]"
        if record_section and re.match(r"^\d+;\d+\.\d+;\d+\.\d+;T#\d+m\d+s\d+ms", line):
            fields = line.split(";")
            point, position, force, time = int(fields[0]), float(fields[1]), float(fields[2]), fields[3]
            records.append({"Point": point, "Position": position, "Force": force, "Time": time})

    return pd.DataFrame(records)

# Streamlit app interface
st.title("Log File Parser with Interactive Curve Diagram")
uploaded_file = st.file_uploader("Choose a log file", type="log")

if uploaded_file:
    # Read file and parse
    file_content = uploaded_file.read().decode("utf-8")
    records_df = parse_log(file_content)

    # Display the records under "[Recorded curves]"
    if not records_df.empty:
        st.write("Records under '[Recorded curves]':")
        st.dataframe(records_df)

        # Allow user to select x and y axis for plotting
        x_axis = st.selectbox("Select X axis:", options=records_df.columns, index=1)
        y_axis = st.selectbox("Select Y axis:", options=records_df.columns, index=2)

        # Plot the interactive curve using Plotly
        st.write(f"{x_axis} vs. {y_axis} Curve")
        fig = px.line(records_df, x=x_axis, y=y_axis, markers=True, title=f"{x_axis} vs. {y_axis} Curve")
        fig.update_traces(mode="lines+markers")
        fig.update_layout(xaxis_title=x_axis, yaxis_title=y_axis, hovermode='x unified')

        # Display the plot in Streamlit
        st.plotly_chart(fig)
    else:
        st.write("No records found under '[Recorded curves]'.")
