import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from wind_turbineinfo import turbineinfo
from Wind_module import wind_module, wind_split, wind_merge, mergetest, splittest
from wind_height import c_height
from string_to_float import string_to_float
from average import average_plot
from Calculation_module import wind_bat_gen, bat_gen, gen_solo, wind_bat
from Battery_module import battery_charge, battery_deplete
from diesel_aggregate import gen_drain, co2_emission, efficiency_curve
from monte_carlo import monte_carlo_simulation
from Consumption_length import consumption_length, list_consumption
from plotting import power_curve_plot, engine_plot, basic_plot
import sys

# Chose what is active, wind, battery and generator
wind_mode = True
bat_mode = True
gen_mode = True

x_value = [3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0,
           20.0, 21.0, 22.0, 23.0, 24.0, 25.0]
y_value = [0.0, 10.0, 20.0, 40.0, 75.0, 105.0, 140.0, 190.0, 240.0, 290.0, 340.0, 390.0, 440.0, 490.0, 550.0, 610.0,
           690.0, 790.0, 870.0, 930.0, 970.0, 990.0, 1000.0]
plt.plot(x_value, y_value)
plt.grid()
plt.show()
sys.exit()
# Read wind data and consumption data from csv
if wind_mode:
    temp_wind = pd.read_csv('FullWind.csv')
    wind = monte_carlo_simulation(temp_wind)
read_consumption = pd.read_csv('con_full.csv')
consumption = read_consumption['0'].values.tolist()
X = np.arange(0, len(consumption), 1)
idx = pd.date_range('2023-01-01 00:00', periods=len(consumption), freq='H')
read_consumption = read_consumption.set_index([idx])

n_turbines = [1, 2, 3]
if not wind_mode:
    n_turbines = [0]
bat_packs = [10, 15, 20, 25]
if not bat_mode:
    bat_packs = [0]
#at_packs = [20]
total_gen = []
# Select turbine
# https://openenergy-platform.org/dataedit/view/supply/wind_turbine_library
if wind_mode:
    name = 'S2x'  # GE 2.5-120, E-53/800(not offshore), V100/1800, S2x
    turbine, turbines = turbineinfo(name)

# String splitting
    x_value = string_to_float(turbine.power_curve_wind_speeds)
    y_value = string_to_float(turbine.power_curve_values)
    hub_height = string_to_float(turbine.hub_height)

    #  Wind height
    h = hub_height[-1]  # Set desirable wind height
    c_wind, b_same = c_height(wind, h)  # Calls wind_height module
    c_name = 'Wind Speed ' + str(h)  # Sets name of column
    if not b_same:
        wind[c_name] = np.array(c_wind)  # Adds new wind speed into dataframe with column-name c_name
df_generator = pd.DataFrame()
df_generator['time'] = idx
df_max = pd.DataFrame()
df_max['time'] = idx
for i in range(len(n_turbines)):

    if n_turbines[i] > 1:
        y_value = [x * n_turbines[i] for x in y_value]
    if wind_mode:
# Interpolating the power curve
        f = interpolate.interp1d(x_value, y_value, kind='cubic')

# Wind module
        power_output = wind_module(c_wind, x_value, f)

    for j in range(len(bat_packs)):
        gen = 4000
        diesel_kwh = [0] * len(X)
        on = 0
        b_list = [0] * len(X)

# Combo True False True does not exist - value?

        if wind_mode and bat_mode and gen_mode:
            max_output, b_list, diesel_kwh, on, needed, emission = wind_bat_gen(power_output, consumption,
                                                                                X, gen, bat_packs[j])
        if wind_mode is False and bat_mode and gen_mode:
            max_output, needed, diesel_kwh, b_list, on, emission = bat_gen(consumption, X, gen)  # Currently not working, gen negative
        if wind_mode is True and bat_mode is True and gen_mode is False:
            max_output, needed, b_list = wind_bat(power_output, consumption, X)
        if wind_mode is False and bat_mode is False and gen_mode is True:
            max_output, needed, diesel_kwh, on, emission = gen_solo(consumption, X, gen)
# Finds amount of wasted energy
        wasted = [0] * len(X)
        not_enough = 0
        for x in X:
            if max_output[x] > consumption[x]:
                wasted[x] = max_output[x] - consumption[x]
                needed[x] = 0
            elif max_output[x] < consumption[x]:
                not_enough += 1
                needed[x] = consumption[x] - max_output[x]
        df_generator[f'{i},{j}'] = diesel_kwh
        df_max[f'{i},{j}'] = max_output
        print(f'Calculated scenario: {i},{j}')
        total_gen.append(np.sum(df_generator[f'{i},{j}']))

print(total_gen)
basic_plot(df_max, len(n_turbines), len(bat_packs), 'Generator comparison', "kWh", "time")
print('There is a lack in energy for: %d hours, which is %3.2f percent.' % (not_enough, not_enough/len(X)*100))
print(f'The energy needed sums up to {np.sum(needed):,.3f} kWh')
was_sum = np.sum(wasted)
was_max = np.max(wasted)
print(f'The amount wasted is {was_sum:,.3f} kWh, and max in an hour is {was_max:,.3f} kWh')

con_sum = np.sum(consumption)
d_sum = np.sum(diesel_kwh)
per = (d_sum/con_sum)*100
if gen_mode:
    emi_sum = np.sum(emission)/1000
print(f'Sum of energy from consumption is {con_sum:,.3f} kWh')
print(f'Sum of energy from diesel is {d_sum:,.3f} kWh')
print(f'Part of energy from diesel is {per:3.2f} percent')
#print(max(c_list))
#print(np.mean(c_list))
print('Hours generator is on:', on)
if gen_mode:
    print(f'This means that the generator emits {emi_sum:.3f} tons of CO2')

# Shows an average through the plot. Window is chosen as how many hours are made into one
timestep = 1000
ave_con = average_plot(X, consumption, timestep)
if bat_mode:
    chosen_average = average_plot(X, b_list, timestep)
other_average = average_plot(X, max_output, timestep)
if gen_mode:
    gen_ave = average_plot(X, diesel_kwh, timestep)
need_ave = average_plot(X, needed, timestep)
#c_list_average = average_plot(X, power_output, timestep)

plt.xlabel('Year')
plt.ylabel('kW')
plt.plot(idx, consumption, label='Consumption')
plt.plot(idx, ave_con, label='Average Consumption')
if bat_mode:
    plt.plot(idx, chosen_average, 'g', label='Battery')
if gen_mode:
    plt.plot(idx, gen_ave, 'r', label='Generator')
plt.plot(idx, other_average, 'm', label='Max Output')
plt.plot(idx, need_ave, label='Needed')
#plt.plot(idx, c_list_average, 'g', label='C_list')
plt.legend(loc='upper left')
plt.show()

print('Program ended.')

