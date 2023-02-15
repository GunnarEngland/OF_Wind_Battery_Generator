#  Monte Carlo simulation to randomize the wind data
import pandas as pd
import numpy as np
import sys


def monte_carlo_simulation():
    df = pd.read_csv('TestResult.csv')
    df.index = pd.to_datetime(df.index)
    n_years = [1997, 1998, 1999, 2001, 2002, 2003, 2005, 2006, 2007, 2009, 2010, 2011,
               2013, 2014, 2015, 2017, 2018, 2019]
    l_years = [1996, 2000, 2004, 2008, 2012, 2016]
    df_random = pd.DataFrame()
    for i in range(20):
        if i in [1, 5, 9, 13, 17]:
            l_year = np.random.choice(l_years, replace=False)
            df_filtered = df[df.index.year == l_year]
        else:
            n_year = np.random.choice(n_years, replace=False)
            df_filtered = df[df.index.year == n_year]
        df_random.append(df_filtered, ignore_index=True)
    print(df_random.head())
    return df_random
    #df_filtered = df[(df.index.year >= 1996) & (df.index.year <= 2019)]
    #print(df_filtered.head())
    #df_random = df.sample(frac=20 / 24, replace=False, random_state=0)
    #print(df_random.head(-5))
    #return df_random


    chosen_years = pd.DataFrame()
    for i in range(20):
        if i in [1, 5, 9, 13, 17]:
            y = l_selection[0]
            l_selection = np.delete(l_selection, 0, axis=None)
            print(df.head())
            df.values.tolist()
            chosen_years = chosen_years.append(df, ignore_index=True)
            p = y
        else:
            x = n_selection[0]
            n_selection = np.delete(n_selection, 0, axis=None)
            df = pd.read_excel(x+'.xlsx')
            chosen_years = chosen_years.append(df, ignore_index=True)
            p = x
        print('Added year to chosen: ' + p)
        print(len(chosen_years))

    return chosen_years
