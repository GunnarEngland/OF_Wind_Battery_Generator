# Wind module: Converting wind to energy
import pandas as pd
import numpy as np


def wind_module(wind, x, f):

    power_output = []
    cutin = x[0]
    cutout = x[-1]
    for i in wind.values:
        if i < cutin:
            power_output.append(0.0)
        elif i > cutout:
            power_output.append(0.0)
        else:
            power_output.append(f(i))

    value = [float(x) for x in power_output]
    return value


def wind_split(rest):
    #years = ['ws96', 'ws97', 'ws98', 'ws99', 'ws00', 'ws01', 'ws02', 'ws09', 'ws10', 'ws11',
     #        'ws12', 'ws13', 'ws14', 'ws15', 'ws16', 'ws17', 'ws18', 'ws19']
    #hour = [0, 8784, 17544, 26304, 35064, 43848, 52608, 61368, 70128, 78888, 87648, 96432,
     #       105192, 113952, 122712, 131472, 140256, 149016, 157778]
    years = ['ws03', 'ws04', 'ws05', 'ws06', 'ws07', 'ws08']
    hour = [0, 8760, 17544, 26304, 35064,43824, 52608]
    for i in range(0, 6, 1):
        df = pd.DataFrame(rest[hour[i]:hour[i+1]].values)
        df.to_excel(years[i]+'.xlsx')
        print('Printed to excel: ' + years[i])


def wind_merge():
    years = ['ws96', 'ws97', 'ws98', 'ws99', 'ws00', 'ws01', 'ws02', 'ws03', 'ws04', 'ws05', 'ws06', 'ws07', 'ws08',
             'ws09', 'ws10', 'ws11', 'ws12', 'ws13', 'ws14', 'ws15', 'ws16', 'ws17', 'ws18', 'ws19']
    idxl = pd.date_range('2000-01-01 00:00', periods=8784, freq='H')
    idxn = pd.date_range('2001-01-01 00:00', periods=8760, freq='H')
    dfl = pd.DataFrame(index=idxl)
    dfn = pd.DataFrame(index=idxn)
    for i in range(0, 24, 1):
        cl = pd.read_excel(years[i]+'.xlsx')
        da = cl.iloc[:, -1]
        if years[i] in ['ws96', 'ws00', 'ws04', 'ws08', 'ws12', 'ws16']:
            dfl[years[i]] = da
        else:
            dfn[years[i]] = da
    print(dfl.head(-5))
    print(dfn.head(-5))
    dfl.to_excel('leapyears.xlsx')

    return True


def mergetest():
    df1 = pd.read_excel('VindDataOF1_6year101.xlsx', usecols='B')
    df2 = pd.read_excel('VindDataOF1_resterende.xlsx', usecols='B')
    split_point = 61368
    df2_upper = df2.iloc[:split_point]
    df2_lower = df2.iloc[split_point:]
    df = pd.concat([df2_upper, df1, df2_lower], axis=0)
    idx = pd.date_range('1996-01-01 00:00', periods=len(df), freq='H')
    df = df.set_index([idx])
    df.to_csv('TestResult.csv')

    return df


def splittest():
    df = pd.read_excel('TestResult.xlsx')
    df.index = pd.date_range('1996-01-01 00:00', periods=len(df), freq='H')
    df['Year'] = df.index.year
    grouped = df.groupby(df.index.year)
    df_list = []
    for year, data in grouped:
        df_year = pd.DataFrame(data)
        df_list.append(df_year)

    final_df = pd.concat(df_list, axis=1)
    final_df.to_excel('FinalWind.xlsx')
    return final_df

