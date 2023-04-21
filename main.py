import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from wind_turbineinfo import turbineinfo, set_info
from Wind_module import wind_module, wind_split, wind_merge, mergetest, splittest
from wind_height import c_height
from string_to_float import string_to_float
from average import average_plot
from Calculation_module import wind_bat_gen, bat_gen, gen_solo, wind_bat
from Battery_module import battery_charge, battery_deplete
from diesel_aggregate import gen_drain, co2_emission, efficiency_curve
from monte_carlo import monte_carlo_simulation, non_random
from Consumption_length import consumption_length, list_consumption
from plotting import power_curve_plot, engine_plot, basic_plot, bar_plot, wind_plot, sorted_bar_plot, \
    plot_wind_and_power_freq, wind_speed_histogram, power_output_histogram
from analysis import calculate_monthly_averages
import sys

# Chose what is active, wind, battery and generator
wind_mode = True
bat_mode = True
gen_mode = True
mcr = False
# Read wind data and consumption data from csv
read_consumption = pd.read_csv('con_full.csv')
consumption = read_consumption['0'].values.tolist()
X = np.arange(0, len(consumption), 1)
idx = pd.date_range('2023-01-01 00:00', periods=len(consumption), freq='H')
read_consumption = read_consumption.set_index([idx])

# Test numbers to figure out summation.
#consumption = [700, 700, 1000, 1000, 1000, 1000, 150, 150, 150, 1200, 1200, 1200, 800, 800]
#wind_list = [10, 20, 20, 15, 20, 1, 15, 20, 15, 10, 7, 7, 20, 20]
#X = np.arange(0, len(consumption), 1)
#idx = pd.date_range('2023-01-01 00:00', periods=len(consumption), freq='H')
#wind = pd.DataFrame(wind_list)

if wind_mode:
    temp_wind = pd.read_csv('FullWind.csv')
    if mcr:
        wind = monte_carlo_simulation(temp_wind)
    else:
        wind = non_random(temp_wind)

wind_idx = pd.date_range('1996-01-01 00:00', periods=len(wind), freq='H')
wind = wind.set_index([wind_idx])
#  Choose number of turbines
#n_turbines = [1, 2, 3]
n_turbines = [1]
if not wind_mode:
    n_turbines = [0]
#  Choose number of battery packs
#bat_packs = [10, 15, 20, 25]
#bat_packs = [20, 30, 40, 50]
bat_packs = [20]
if not bat_mode:
    bat_packs = [0]
total_gen = []
# Select turbine
# https://openenergy-platform.org/dataedit/view/supply/wind_turbine_library
if wind_mode:
    name = 'SWT-2.3-113'  # GE 2.5-120, E-53/800(not offshore), V100/1800, S2x (O H), SWT-2.3-113 (L V)
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
wastedlist = []
maxlist = []
onlist = []
emissionlist = []

monthly_average = wind[c_name].resample('M').mean()
least_windy_month = monthly_average.sort_values().index[0].strftime('%B %Y')
month, year = least_windy_month.split()
data_of_month = wind[c_name][(wind[c_name].index.month == pd.to_datetime(month, format='%B').month) & (wind[c_name].index.year == int(year))]
# Resample the data at a weekly frequency, using the mean of the values in each week
data_of_week = data_of_month.resample('W').mean()

# Find the week with the lowest mean wind speed
min_week = data_of_week.idxmin()

# Extract the data for that week
data_of_min_week = data_of_month[(data_of_month.index.isocalendar().week == min_week.week)]
# Set the figure size
plt.figure(figsize=(10, 6))

# plot the data
fig, ax = plt.subplots()
data_of_min_week.plot.bar(ax=ax)

ax.set_xticks(range(0, len(data_of_min_week), 24))
ax.set_xticklabels(data_of_min_week.index[::24].strftime('%d'))
plt.xticks(rotation=45)
plt.ylabel("Wind speed")
plt.title("Lowest wind speed week. May 2010")
plt.show()

#for i in range(len)
#for i in
for i in range(len(n_turbines)):

    if n_turbines[i] > 1:
        y_value = [x * n_turbines[i] for x in y_value]
    if wind_mode:
        # Interpolating the power curve
        f = interpolate.interp1d(x_value, y_value, kind='cubic')

        # Going from wind data to power output, through the use of the power curve
        power_output = wind_module(c_wind, x_value, f)
        week_output = wind_module(data_of_min_week, x_value, f)
        print(np.sum(week_output))
        #wind[c_name].value_counts(sort=False).plot.bar()
        #plt.figure()
        #ax = wind.plot.kde()
        #ax = wind[c_name].value_counts(sort=True).plot.bar()
        windlist = c_wind.tolist()
        #sorted_bar_plot(windlist, True, c_name)
        #plot_wind_and_power_freq(windlist, power_output)
        #plt.show()
        # Example usage
        #wind_speed_histogram(windlist)
        #power_output_histogram(power_output)
        #plt.show()
        #plt.show()
    for j in range(len(bat_packs)):
        gen = 4000
        diesel_kwh = [0] * len(X)
        on = 0
        b_list = [0] * len(X)

# Combo True False True does not exist - value?

        if wind_mode and bat_mode and gen_mode:
            max_output, b_list, diesel_kwh, on, needed, emission, not_enough, wasted = \
                wind_bat_gen(power_output, consumption, X, gen, bat_packs[j])
        if wind_mode is False and bat_mode and gen_mode:
            max_output, needed, diesel_kwh, b_list, on, emission = bat_gen(consumption, X, gen)  # Currently not working, gen negative
        if wind_mode is True and bat_mode is True and gen_mode is False:
            max_output, needed, b_list = wind_bat(power_output, consumption, X)
        if wind_mode is False and bat_mode is False and gen_mode is True:
            max_output, needed, diesel_kwh, on, emission, not_enough, wasted = gen_solo(consumption, X, gen)
        df_generator[f'{i},{j}'] = diesel_kwh
        df_max[f'{i},{j}'] = max_output
        wastedlist.append(np.sum(wasted))
        maxlist.append(np.sum(max_output))
        onlist.append(on)
        emissionlist.append(np.sum(emission))
        print(f'Calculated scenario: {i},{j}')
        total_gen.append(np.sum(df_generator[f'{i},{j}']))

print(total_gen)
time_plot = False
scenario_text = False
#bar_plot(total_gen, "Summed kWh produced by generator", "Generator produced kWh by scenario", False)
#basic_plot(df_max, len(n_turbines), len(bat_packs), 'Generator comparison', "kWh", "time")
if scenario_text:
    if wind_mode:
        print(f'The wind turbines produces {np.sum(power_output): .3f} kWh.')
    print(f"The maximum energy produced adds up to {np.sum(max_output): .3f} kWh.")
    print('There is a lack in energy for: %d hours, which is %3.2f percent.' % (not_enough, not_enough/len(X)*100))
    print(f'The energy needed sums up to {abs(np.sum(needed))} kWh')
    print(f'The amount wasted is {np.sum(wasted): .3f} kWh, and max in an hour is {np.max(wasted): .3f} kW')
    print(f'Sum of energy from consumption is {np.sum(consumption): .3f} kWh')
    print(f'Sum of energy from diesel is {np.sum(diesel_kwh): .3f} kWh, which is '
          f'{(np.sum(diesel_kwh)/np.sum(consumption))*100: .2f}% of consumption.')
    print('Hours generator is on:', on)
    if gen_mode:
        print(f'This means that the generator emits {np.sum(emission)/1000: .3f} tons of CO2')

if time_plot:
    # Shows an average through the plot. Window is chosen as how many hours are made into one
    timestep = 500
    ave_con = average_plot(X, consumption, timestep)
    if bat_mode:
        chosen_average = average_plot(X, b_list, timestep)
    if wind_mode:
        other_average = average_plot(X, power_output, timestep)
    if gen_mode:
        gen_ave = average_plot(X, diesel_kwh, timestep)
    need_ave = average_plot(X, needed, timestep)

    plt.xlabel('Year')
    plt.ylabel('kW')
    plt.plot(idx, consumption, label='Consumption')
    plt.plot(idx, ave_con, label='Average Consumption')
    if bat_mode:
        plt.plot(idx, chosen_average, 'g', label='Battery')
    if gen_mode:
        plt.plot(idx, gen_ave, 'r', label='Generator')
    if wind_mode:
        plt.plot(idx, other_average, 'm', label='Wind Output')
    plt.plot(idx, need_ave, label='Needed')
    plt.legend(loc='upper left')
    if wind_mode:
        plt.title(f'Scenario with {n_turbines[0]} {name} turbine(s) and battery capacity of {bat_packs[-1]*60} kWh')
    else:
        plt.title('Base case with only generator')
    plt.show()

print('Program ended.')

