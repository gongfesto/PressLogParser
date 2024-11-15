# src/ui_components.py
import streamlit as st
import plotly.express as px
import pandas as pd
import re
from typing import List

def display_data_table(dataframe: pd.DataFrame, title: str) -> None:
    """
    Display a DataFrame as a table in the Streamlit app.

    Args:
        dataframe (pd.DataFrame): The DataFrame to display.
        title (str): Title of the table.
    """
    st.write(title)
    st.dataframe(dataframe)

def calculate_velocity(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate velocity based on position and time, and add it as a new column to the DataFrame.

    Args:
        dataframe (pd.DataFrame): The DataFrame containing Position and Time columns.

    Returns:
        pd.DataFrame: The updated DataFrame with a Velocity column.
    """
    dataframe = dataframe.copy()
    # Assuming time is in the format 'T#XmYsZms' and extracting total time in seconds
    def parse_time(time_str: str) -> float:
        match = re.match(r'T#(?:(\d+)m)?(?:(\d+)s)?(\d+)ms', time_str)
        if match:
            minutes = int(match.group(1)) if match.group(1) else 0
            seconds = int(match.group(2)) if match.group(2) else 0
            milliseconds = int(match.group(3))
            return minutes * 60 + seconds + milliseconds / 1000.0
        return 0.0

    dataframe['Time (s)'] = dataframe['Time'].apply(parse_time)
    dataframe['Time (s)'] = dataframe['Time (s)'] - dataframe['Time (s)'][0]
    dataframe['Velocity'] = dataframe['Position'].diff() / dataframe['Time (s)'].diff()
    dataframe['Velocity'].fillna(0, inplace=True)  # Fill NaN values with 0 for the first row
    return dataframe

def select_axis(dataframe: pd.DataFrame, record_index: int) -> tuple:
    """
    Display select boxes to choose X and multiple Y axes for plotting.

    Args:
        dataframe (pd.DataFrame): The DataFrame for which axes are to be selected.
        record_index (int): The index of the current record for unique key identification.

    Returns:
        tuple: Selected X axis and list of Y axes.
    """
    x_axis = st.selectbox(f"Select X axis for Record {record_index}:", options=dataframe.columns, index=1, key=f"x_axis_{record_index}")
    y_axes = st.multiselect(f"Select Y axis for Record {record_index}:", options=dataframe.columns, default=[dataframe.columns[2]], key=f"y_axis_{record_index}")
    return x_axis, y_axes

def plot_curve(dataframe: pd.DataFrame, x_axis: str, y_axes: List[str], title: str) -> None:
    """
    Plot an interactive curve using Plotly based on selected X and multiple Y axes.

    Args:
        dataframe (pd.DataFrame): The DataFrame containing data to plot.
        x_axis (str): The column to use for the X axis.
        y_axes (List[str]): The columns to use for the Y axes.
        title (str): The title of the plot.
    """
    fig = px.line(dataframe, x=x_axis, y=y_axes, markers=True, title=title)
    fig.update_traces(mode="lines+markers")
    fig.update_layout(xaxis_title=x_axis, yaxis_title=', '.join(y_axes), hovermode='x unified')
    st.plotly_chart(fig)
