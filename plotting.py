import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from average import average_plot


def power_curve_plot(x_value, y_value, f, name):
    plt.xlabel('Wind speed')
    plt.ylabel('Power output')
    plt.title(f'Power curve for {name}')
    plt.plot(x_value, y_value, 'o')
    plt.plot(x_value, f(x_value), '-')
    plt.savefig(f'powercurve_{name}.png')
    plt.show()
    return


def consumption_plot(df):
    df.plot(x=df.index, y='0')
    plt.xlabel('Consumption')
    plt.ylabel('kW')
    plt.show()
    return


def wind_plot(y_wind):
    x_wind = np.arange(0, len(y_wind), 1)
    wind_ave = average_plot(x_wind, y_wind, 1000)
    plt.plot(x_wind, y_wind, x_wind, wind_ave)
    plt.title('Yearly wind speeds for 2019')
    plt.xlabel('Hours')
    plt.ylabel('Wind Speed (m/s)')
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

