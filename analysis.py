import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter


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
    #a_power = mean_wind_speed['Wind Speed 101'].values.tolist()
    #b_power = mean_wind_speed['Wind Speed 50'].values.tolist()
    #c_power = mean_wind_speed['Wind Speed 99.5'].values.tolist()
    # Plot the mean wind speed for each month and hour
    #fig, ax = plt.subplots(figsize=(12, 6))
    #x_value = range(len(a_power))
    # Generate x-axis labels with months
    #month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    #month_ticks = list(range(0, 288, 24))

    #ax.set_xticks(month_ticks)
    #ax.xaxis.set_major_locator(FixedLocator(month_ticks))
    #ax.xaxis.set_major_formatter(FixedFormatter(month_labels))

    #ax.plot(x_value, a_power, label='Wind Speed 101')
    #ax.plot(x_value, b_power, label='Wind Speed 99.5')
    #ax.plot(x_value, c_power, label='Wind Speed 50')
    #ax.legend()
    #plt.ylim([0, 700])
    #plt.xlabel('Month')
    #plt.ylabel('Mean Wind Speed (m/s)')
    #plt.title(f'Seasonal Variations in Mean Wind Speed over 20 Years')
    #plt.savefig('Figures/seasonalvariationwind.png')
    #plt.show()
    return mean_wind_speed


def wasted_vs_elgen():
    wasted = [0, 27.5, 24.95, 24.01, 23.19, 57.42, 55.98, 55.41, 54.90, 69.55, 68.60, 68.21, 67.87, 65.94, 64.99,
              64.60, 64.26]
    el_gen = [100, 42.04, 40.04, 39.29, 38.63, 31.98, 29.68, 28.76, 27.94, 27.03, 24.75, 23.82, 22.99, 19.85, 17.62,
              16.72, 15.90]
    labels = ['Base Case', '1S2x/0', '1S2x/1200', '1S2x/1800', '1S2x/2400', '2S2x/0', '2S2x/1200', '2S2x/1800',
              '2S2x/2400', '3S2x/0', '3S2x/1200', '3S2x/1800', '3S2x/2400', 'SWT/0', 'SWT/1200', 'SWT/1800',
              'SWT/2400']
    x = np.arange(len(labels))  # Create x values for the plot
    condition = np.array(wasted) >= np.array(el_gen)  # Boolean condition for filling the area
    plt.figure(figsize=(10, 6))
    plt.plot(x, wasted, marker='o', label='Wasted Wind Energy (%)')
    plt.plot(x, el_gen, marker='o', label='Electricity from Diesel Generator (%)')
    #plt.fill_between(x, wasted, el_gen, where=condition, color='red', alpha=0.5)
    #plt.fill_between(x, wasted, el_gen, where=~condition, color='green', alpha=0.5)
    plt.xlabel('Scenario')
    plt.ylabel('Percentage (%)')
    plt.title('Comparison of Wasted Wind Energy versus Electricity from Diesel Generator')
    plt.xticks(x, labels, rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig('Figures/wastedwindvselgen.png')
    plt.show()
    return


    plt.bar(labels, wasted, label='Wasted Wind Energy (%)', alpha=1)
    plt.bar(labels, el_gen, label='Electricity from Diesel Generator (%)', alpha=0.75)
    plt.xlabel('Scenario', fontsize=5)
    plt.ylabel('Percentage (%)')
    plt.title('Comparison of Wasted Wind Energy with Electricity from Diesel Generator')
    plt.xticks(rotation=45)
    plt.legend()
    plt.show()
