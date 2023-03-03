import pandas as pd
# Turbine info
#  csv gathered from


def turbineinfo(name):
    turbines = pd.read_csv('wind_turbine.csv')
    select_turbine = turbines.loc[turbines['name'] == name]
    #if not select_turbine.has_power_curve:
        #raise Exception('Turbine does not have a power curve.')
    print('Returned values for ' + str(name) + ' turbine')
    return select_turbine, turbines

# turbines.loc[len(turbines)] = [141, 153, 'SeaTwirl', 'S2x', 'S2x 1MW', 1000, 50, 2000, 50, np.nan, np.nan,
#                               np.nan, np.nan, np.nan, np.nan, True, [3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0,
#          20.0, 21.0, 22.0, 23.0, 24.0, 25.0], [0.0, 2.0, 14.0, 38.0, 77.0, 141.0, 228.0, 336.0, 480.0, 645.0, 770.0, 870.0, 930.0, 970.0, 990.0, 1000.0,
#          1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0, 1000.0], False, np.nan, np.nan, False, np.nan, np.nan, 'https://seatwirl.com/products/seatwirl-s2/']

