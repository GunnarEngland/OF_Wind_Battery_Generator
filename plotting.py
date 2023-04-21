import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from average import average_plot


def power_curve_plot(x_value, y_value, f, name, save):
    plt.xlabel('Wind speed (m/s)')
    plt.ylabel('Power output (kW)')
    plt.title(f'Power curve for {name}')
    plt.plot(x_value, y_value, 'o')
    plt.plot(x_value, f(x_value), '-')
    plt.xlim([0, 50])
    plt.ylim([0, 2500])
    plt.grid()
    if save:
        plt.savefig(f'powercurve_{name}.png')
    plt.show()
    return


def consumption_plot(df):
    df.plot(x=df.index, y='0')
    plt.xlabel('Consumption')
    plt.ylabel('kW')
    plt.show()
    return


def wind_plot(x_wind, y_wind):
    #idx = pd.date_range('1996-01-01 00:00', periods=len(y_wind), freq='H')
    plt.plot(x_wind, y_wind)
    plt.title('Wind speeds 1996-2015')
    plt.xlabel('Time (h)')
    plt.ylabel('Wind Speed (m/s)')
    plt.savefig('windspeeds1996-2015.png')
    plt.show()
    return


def engine_plot(diesel_eff, x_eff, y_eff):
    plt.plot(x_eff, y_eff, 'o')
    plt.plot(x_eff, diesel_eff(x_eff))
    plt.grid()
    plt.xlabel('Power output')
    plt.ylabel('Engine efficiency')
    plt.show()
    return


def basic_plot(df, k, l, name, y_label, c_name):
    for i in range(k):
        for j in range(l):
            ave = average_plot(df[c_name], df[f'{i},{j}'], 1000)
            plt.plot(df['time'], ave, label=f'{i},{j}')
    plt.title(name)
    plt.legend(loc='upper right')
    plt.xlabel('Time')
    plt.ylabel(y_label)
    plt.show()
    return


def bar_plot(data, ylabel, title, save):
    x_value = np.arange(0, len(data), 1)
    plt.bar(x_value, data)
    plt.xlabel("Scenario")
    plt.ylabel(ylabel)
    plt.title(title)
    if save:
        plt.savefig(f"{title}.png")
    plt.show()
    return


def sorted_bar_plot(wind_speeds, save, c_name):
    # Calculate the frequencies of each wind speed
    bins = np.arange(0, 41, 1)
    freq, _ = np.histogram(wind_speeds, bins=bins)

    # Create a pandas dataframe with the frequencies
    df = pd.DataFrame({'wind_speed': bins[:-1], 'frequency': freq})

    # Plot the frequency distribution as bars with lines between the bars
    plt.bar(df['wind_speed'], df['frequency'], width=1, align='edge', edgecolor='black')
    plt.xlabel('Wind speed (m/s)')
    plt.ylabel('Frequency')
    plt.title(f'{c_name} m.a.s.l. frequency distribution')
    if save:
        plt.savefig(f'{c_name}.png')
    plt.show()
    return


def plot_wind_and_power_freq(wind_speeds, power_output):
    # Calculate the frequencies of each wind speed
    bins_wind = np.arange(0, 41, 1)
    freq_wind, _ = np.histogram(wind_speeds, bins=bins_wind)

    # Calculate the frequencies of the power output values
    bins_power = np.arange(0, np.max(power_output) + 1000, 1000)
    freq_power, _ = np.histogram(power_output, bins=bins_power)

    # Create a pandas dataframe with the wind speed frequencies
    df_wind = pd.DataFrame({'wind_speed': bins_wind[:-1], 'frequency': freq_wind})

    # Create a pandas dataframe with the power output frequencies
    df_power = pd.DataFrame({'power_output': bins_power[:-1], 'frequency': freq_power})
    df_power = df_power[df_power['power_output'] <= np.max(power_output) + 1000]
    df_power = df_power[df_power['power_output'] >= 0]

    # Create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))

    # Plot the wind speed frequency distribution as bars with lines between the bars
    ax1.bar(df_wind['wind_speed'], df_wind['frequency'], width=1, align='edge', edgecolor='black')
    ax1.set_xlabel('Wind speed (m/s)')
    ax1.set_ylabel('Frequency')
    ax1.set_title('Wind speed frequency distribution')

    # Plot the power output frequency distribution as a line
    ax2.plot(df_power['power_output'], df_power['frequency'], 'r-')
    ax2.set_xlim([0, np.max(power_output) + 1000])
    ax2.set_ylim([0, np.max(freq_power) + 10])
    ax2.set_xlabel('Power output (W)')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Power output frequency distribution')

    return fig, (ax1, ax2)


def wind_speed_histogram(wind_speeds, bin_width=1):
    bins = np.arange(0, np.max(wind_speeds) + bin_width, bin_width)
    freq, _ = np.histogram(wind_speeds, bins=bins)
    plt.bar(bins[:-1], freq, width=bin_width, align="edge", edgecolor="black")
    plt.xlabel("Wind speed (m/s)")
    plt.ylabel("Frequency")
    plt.title("Wind speed distribution")

def power_output_histogram(power_output, bin_width=50):
    bins = np.arange(0, np.max(power_output) + bin_width, bin_width)
    freq, _ = np.histogram(power_output, bins=bins)
    plt.bar(bins[:-1], freq, width=bin_width, align="edge", edgecolor="black")
    plt.xlabel("Power output (kW)")
    plt.ylabel("Frequency")
    plt.title("Power output distribution for SWT-2.3-113")
    #plt.savefig('Power output distributionSWT.png')


