# src/ui_components.py
import streamlit as st
import plotly.express as px
import pandas as pd
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

def select_axis(dataframe: pd.DataFrame, record_index: int) -> tuple:
    """
    Display select boxes to choose X and Y axis for plotting.

    Args:
        dataframe (pd.DataFrame): The DataFrame for which axes are to be selected.
        record_index (int): The index of the current record for unique key identification.

    Returns:
        tuple: Selected X and Y axis.
    """
    x_axis = st.selectbox(f"Select X axis for Record {record_index}:", options=dataframe.columns, index=1, key=f"x_axis_{record_index}")
    y_axis = st.selectbox(f"Select Y axis for Record {record_index}:", options=dataframe.columns, index=2, key=f"y_axis_{record_index}")
    return x_axis, y_axis

def plot_curve(dataframe: pd.DataFrame, x_axis: str, y_axis: str, title: str) -> None:
    """
    Plot an interactive curve using Plotly based on selected X and Y axis.

    Args:
        dataframe (pd.DataFrame): The DataFrame containing data to plot.
        x_axis (str): The column to use for the X axis.
        y_axis (str): The column to use for the Y axis.
        title (str): The title of the plot.
    """
    fig = px.line(dataframe, x=x_axis, y=y_axis, markers=True, title=title)
    fig.update_traces(mode="lines+markers")
    fig.update_layout(xaxis_title=x_axis, yaxis_title=y_axis, hovermode='x unified')
    st.plotly_chart(fig)
