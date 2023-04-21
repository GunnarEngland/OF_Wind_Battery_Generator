import pandas as pd


def calculate_monthly_averages(data, name):
    """
    Calculates the monthly averages of wind data.

    Args:
        data (pandas.DataFrame or pandas.Series): A pandas DataFrame or Series containing wind data.
            The DataFrame or Series should have a DatetimeIndex and a column named 'wind_speed'.

    Returns:
        pandas.DataFrame: A DataFrame containing the monthly averages of wind speed.
            The DataFrame has a DatetimeIndex and a column named 'monthly_average'.
    """

    # If the input is a Series, convert it to a DataFrame with a 'wind_speed' column
    if isinstance(data, pd.Series):
        data = pd.DataFrame(data, columns=[name])

    # Calculate the monthly averages using pandas resample function
    monthly_averages = data[name].resample('M').mean()

    # Create a DataFrame with a 'monthly_average' column
    monthly_averages_df = pd.DataFrame(monthly_averages, columns=['monthly_average'])

    return monthly_averages_df
