import streamlit as st
import plotly.express as px
import pandas as pd
import re
from typing import List, Tuple

def display_data_table(dataframe: pd.DataFrame, title: str) -> None:
    """
    Display a DataFrame as a table in the Streamlit app.

    Args:
        dataframe (pd.DataFrame): The DataFrame to display.
        title (str): Title of the table.
    """
    st.header("Raw Data Section")
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
    dataframe['Velocity'] = dataframe['Position'].diff() / dataframe['Time (ms)'].diff() * 1000  # Convert to velocity in appropriate units
    dataframe['Velocity'] = dataframe['Velocity'].fillna(method='ffill')  # Fill NaN values with 0 for the first row
    
    # Add the moving average of the velocity
    dataframe['Velocity_MA(5)'] = dataframe['Velocity'].rolling(window=5).mean()
    # Fill NaN values in 'Velocity_MA' with the previous row's value
    dataframe['Velocity_MA(5)'] = dataframe['Velocity_MA(5)'].fillna(method='ffill')
    return dataframe

def evaluate_sampling_interval(dataframe: pd.DataFrame) -> Tuple[float, float]:
    """
    Evaluate the sampling performance by calculating the average and standard deviation of the sampling interval.

    Args:
        dataframe (pd.DataFrame): The DataFrame containing the Time column.

    Returns:
        Tuple[float, float]: The average sampling interval and its standard deviation.
    """
    time_diff = dataframe['Time (ms)'].diff().dropna()
    avg_interval = time_diff.mean()
    std_interval = time_diff.std()
    return avg_interval, std_interval

def plot_sampling_interval(dataframe: pd.DataFrame, nbins:int=20) -> None:
    """
    Plot a histogram to visualize the distribution of the sampling intervals.

    Args:
        dataframe (pd.DataFrame): The DataFrame containing the Time column.
        nbins (int): The number of bins to use for the histogram.
    """
    time_diff = dataframe['Time (ms)'].diff().dropna()
    fig = px.histogram(time_diff, nbins=nbins, title="Sampling Interval Distribution")
    fig.update_layout(xaxis_title="Sampling Interval (ms)", yaxis_title="Frequency", hovermode='x unified')
    st.plotly_chart(fig)

def display_sampling_interval_analysis(dataframe: pd.DataFrame, record_index: int) -> None:
    """
    Display sampling interval analysis including average, standard deviation, and a histogram.

    Args:
        dataframe (pd.DataFrame): The DataFrame containing the Time column.
        record_index (int): The index of the current record.
    """
    st.header("Sampling Interval Analysis Section")
    avg_interval, std_interval = evaluate_sampling_interval(dataframe)
    st.write(f"Average Sampling Interval for Record {record_index}: {avg_interval:.4f} ms")
    st.write(f"Standard Deviation of Sampling Interval for Record {record_index}: {std_interval:.4f} ms")
    nbins = st.slider(f"Select number of bins for sampling interval histogram (Record {record_index}):", min_value=10, max_value=500, value=50, step=5)
    plot_sampling_interval(dataframe, nbins=nbins)

def select_and_plot_curve(dataframe: pd.DataFrame, record_index: int) -> None:
    """
    Allow the user to select X and Y axes and plot the curve based on the selected columns.

    Args:
        dataframe (pd.DataFrame): The DataFrame for which axes are to be selected and plotted.
        record_index (int): The index of the current record.
    """
    x_axis, y_axes = select_axis(dataframe, record_index)
    plot_curve(dataframe, x_axis, y_axes, f"{x_axis} vs. {', '.join(y_axes)} Curve for Record {record_index}")

def select_axis(dataframe: pd.DataFrame, record_index: int) -> tuple:
    """
    Display select boxes to choose X and multiple Y axes for plotting.

    Args:
        dataframe (pd.DataFrame): The DataFrame for which axes are to be selected.
        record_index (int): The index of the current record for unique key identification.

    Returns:
        tuple: Selected X axis and list of Y axes.
    """
    st.header("Curve Plotting Section")
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


def display_footer(app_version: str, company_name: str) -> None:
    """
    Display a footer with app version and copyright information.

    Args:
        app_version (str): The version of the app.
        company_name (str): The name of the company or individual.
    """
    footer = f"""
    <hr style='margin-top: 50px;'>
    <div style='text-align: center; color: grey; font-size: 12px;'>
        <p>App Version: {app_version} | © {company_name}</p>
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)
