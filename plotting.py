import matplotlib.pyplot as plt
import pandas as pd


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
    plt.show()
    return