import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


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


def mask_below(wind):
    # Create a Boolean mask for wind speeds below 3 m/s
    mask = wind['Wind Speed 101'] < 3

    # Create a new grouping column that increments every time there is a change in the mask
    groups = mask.ne(mask.shift()).cumsum().where(mask)

    # Calculate the duration of each group in hours
    group_durations = groups.groupby(groups).apply(lambda x: x.index[-1] - x.index[0]).dt.total_seconds() / 3600

    # Find the longest period below 3 m/s
    longest_period = group_durations.max()

    # Convert the longest period to a timedelta object
    longest_period_timedelta = pd.to_timedelta(longest_period, unit='h')

    # Find the start and end times of the longest period
    start_time = groups.loc[group_durations.idxmax()].index[0]
    end_time = groups.loc[group_durations.idxmax()].index[-1]

    print(f'The longest consecutive period the wind speed is below 3 m/s is {longest_period_timedelta}.')
    print(f'The period starts on {start_time} and ends on {end_time}.')
    # 37, 37, 38, 39, 39, 42, 43, 47, 63, 67
    diffs = wind.index.to_series().diff()

    # Create a new grouping column that increments every time there is a gap in time greater than 1 hour
    groups = ((diffs > pd.Timedelta(hours=1)).cumsum() * mask).rename('group')

    # Calculate the duration of each group in hours
    group_durations = groups.groupby(groups).apply(lambda x: x.index[-1] - x.index[0]).dt.total_seconds() / 3600

    # Find the longest period below 3 m/s
    longest_period = group_durations.max()

    # Convert the longest period to a timedelta object
    longest_period_timedelta = pd.to_timedelta(longest_period, unit='h')
    plt.plot(mask.astype(int), 'o')
    plt.show()
    print(f'The longest consecutive period the wind speed is below 3 m/s is {longest_period_timedelta}.')


def diesel_calc(emission):
    diesel_liter = []
    for val in emission:
        diesel_liter.append(val / 2.67)

    idx = pd.date_range('2024-01-01 00:00', periods=len(emission), freq='H')
    dieseldf = pd.DataFrame(data=diesel_liter, index=idx, columns=['diesel'])
    monthly_sum = dieseldf['diesel'].resample('M').sum()

    return monthly_sum
    # diesel = [i for i in diesel_kwh if i != 0]
    # dieseldf = pd.DataFrame(data=diesel)
    # confreq(dieseldf)


def seasonal(df):
    idx = pd.date_range('2024-01-01 00:00', periods=len(df), freq='H')
    # Convert the timestamp column into a DatetimeIndex
    df['timestamp'] = pd.to_datetime(idx)
    df.set_index('timestamp', inplace=True)
    # Group the data by month and hour
    grouped = df.groupby([df.index.month, df.index.hour])

    # Calculate the mean wind speed for each month and hour
    mean_wind_speed = grouped.mean()

    # Plot the mean wind speed for each month and hour
    mean_wind_speed.plot(figsize=(12, 6))
    plt.xlabel('Month and Hour')
    plt.ylabel('Mean Wind Speed')
    plt.show()
    return mean_wind_speed
