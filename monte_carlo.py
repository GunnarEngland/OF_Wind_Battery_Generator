#  Monte Carlo simulation to randomize the wind data
import pandas as pd
import numpy as np
import sys


def monte_carlo_simulation(df):
    df = df.set_index(pd.DatetimeIndex(df['Unnamed: 0']))
    df = df.drop(['Unnamed: 0'], axis=1)
    n_years = [1997, 1998, 1999, 2001, 2002, 2003, 2005, 2006, 2007, 2009, 2010, 2011,
               2013, 2014, 2015, 2017, 2018, 2019]
    l_years = [1996, 2000, 2004, 2008, 2012, 2016]
    df_random = pd.DataFrame()
    years = []
    for i in range(20):
        if i in [1, 5, 9, 13, 17]:
            l_year = np.random.choice(l_years, replace=False)
            df_filtered = df[df.index.year == l_year]
            years.append(l_year)
        else:
            n_year = np.random.choice(n_years, replace=False)
            df_filtered = df[df.index.year == n_year]
            years.append(n_year)
        df_random = pd.concat([df_random, df_filtered], ignore_index=True)
    print(f'Created a random set using the years: {years}')
    return df_random

