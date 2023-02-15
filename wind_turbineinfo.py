import pandas as pd
# Turbine info
turbines = pd.read_csv('wind_turbine.csv')
#  csv gathered from


def turbineinfo(name):
    select_turbine = turbines.loc[turbines['name'] == name]
    #if not select_turbine.has_power_curve:
        #raise Exception('Turbine does not have a power curve.')
    print('Returned values for ' + str(name) + ' turbine')
    return select_turbine, turbines
