import collections

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from plotting import consumption_plot
from average import average_plot



def consumption_length():
    consumption = pd.read_excel('Forbruk_OF_korr.xlsx', index_col=None)
    consumption = pd.concat([consumption] * 20)
    consumption = consumption.drop(columns='Index')
    consumption.index = pd.date_range(start='2023-01-01 00:00', periods=len(consumption), freq='H')
    print(consumption.head(-5))
    df_list = []
    for i in range(6):
        shifted_df = shift_data(consumption, i*744)
        #df_list.(shifted_df)
    df = pd.concat(df_list, axis=0, ignore_index=True)
    df.to_excel('result.xlsx')
    return


def shift_data(data, steps):
    return data.shift(periods=steps)


def list_consumption():
    read_consumption = pd.read_excel('Forbruk_OF_korr.xlsx', index_col=None)
    consumption = read_consumption['Forbruk [kW]'].values.tolist()
    temp = collections.deque(consumption)

    for i in range(6):
        temp.rotate(i*1440)
        cons = list(temp)
        consumption = [consumption[x] + cons[x] for x in range(len(consumption))]
    consumption = np.repeat(consumption, 20)
    new_list = consumption.copy()
    for x in range(120):
        new_list = np.append(new_list, consumption[x])
    consumption = new_list.copy()
    print(len(consumption))
    df = pd.DataFrame(data=consumption)
    df.index = pd.date_range(start='2023-01-01 00:00', periods=len(consumption), freq='H')
    print(df.head(-5))
    #df_average = average_plot(df.index, df, 1000)
    #plt.plot(df)
    #plt.plot(df_average)
    #plt.show()
    df.to_csv('con_full.csv')
    #for x in df:
    #    if
    return df
# November 1st 2024 = 16080
# April 2026 = 28464
# September 2026 = 32136
# April 2027 = 37224
# September 2027 = 40896
