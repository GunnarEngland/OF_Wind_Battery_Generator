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
    plot_wind_and_power_freq, wind_speed_histogram, power_output_histogram, power_coef_plot, consumption_plot, \
    mean_std_con, mean_std_con_year, timeplot, group_plot, meanstdcon, confreq, emission_plot, diesel_plot, \
    seasonal_prod, wind_speed_multihistogram, power_curve_multiplot
from analysis import calculate_monthly_averages, diesel_calc, seasonal, wasted_vs_elgen
import sys
# Chose what is active, wind, battery and generator
wind_mode = True  # Include wind calculation
bat_mode = True  # Include battery (could also be set to 0 for packs)
gen_mode = True  # With or without generator
mcr = False
monthly = False
thirdheight = False
scenario_text = True
multiple_text = False
compare_plot = False
time_plot = False
SCRLOLP = True

#  Choose number of turbines
#n_turbines = [1, 2, 3]
n_turbines = [1]
if not wind_mode:
    n_turbines = [0]
#  Choose number of battery packs
#bat_packs = [0, 20, 30, 40]
#bat_packs = [20, 30, 40]
bat_packs = [20]
if not bat_mode:
    bat_packs = [00]
#  Choose which turbine will be used
name = 'SWT-2.3-113'  # S2x, SWT-2.3-113

# Read wind data and consumption data from csv
read_consumption = pd.read_csv('con_full.csv')
consumption = read_consumption['0'].values.tolist()
X = np.arange(0, len(consumption), 1)
idx = pd.date_range('2024-01-01 00:00', periods=len(consumption), freq='H')
read_consumption = read_consumption.set_index([idx])
read_consumption = read_consumption.drop('Unnamed: 0', axis=1)
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
#confreq(read_consumption)


total_gen = []
# Select turbine
# https://openenergy-platform.org/dataedit/view/supply/wind_turbine_library
if wind_mode:
    turbine, turbines = turbineinfo(name)

# String splitting
    x_value = string_to_float(turbine.power_curve_wind_speeds)
    y_value = string_to_float(turbine.power_curve_values)
    hub_height = string_to_float(turbine.hub_height)
    if thirdheight:
        turbine2, turbines = turbineinfo('S2x')
        x_value2 = string_to_float(turbine2.power_curve_wind_speeds)
        y_value2 = string_to_float(turbine2.power_curve_values)
        hub_height2 = string_to_float(turbine2.hub_height)
    #  Wind height
    h = hub_height[-1]  # Set desirable wind height
    c_wind, c_same = c_height(wind, h)  # Calls wind_height module
    c_name = 'Wind Speed ' + str(h)  # Sets name of column
    if not c_same:
        wind[c_name] = np.array(c_wind)  # Adds new wind speed into dataframe with column-name c_name
    if thirdheight:
        t = 99.5
        b_name = 'Wind Speed ' + str(t)
        b_wind, b_same = c_height(wind, t)
        wind[b_name] = np.array(b_wind)

df_generator = pd.DataFrame()
df_generator['time'] = idx
df_max = pd.DataFrame()
df_max['time'] = idx
wastedlist = []
maxlist = []
onlist = []
emissionlist = []
generatorlist = []

if thirdheight:
    mean = seasonal(wind)

if monthly:
    monthly_average = wind[c_name].resample('M').mean()
    least_windy_month = monthly_average.sort_values().index[-1].strftime('%B %Y')
    print(least_windy_month)
    month, year = least_windy_month.split()
    data_of_month = wind[c_name][(wind[c_name].index.month == pd.to_datetime(month, format='%B').month) & (wind[c_name].index.year == int(year))]
    monthly_average_con = read_consumption['0'].resample('M').mean()
    highest_consumption_month = monthly_average_con.sort_values().index[0].strftime('%B %Y')
    print(highest_consumption_month)
    month, year = highest_consumption_month.split()
    data_of_month_con = read_consumption['0'][(read_consumption['0'].index.month == pd.to_datetime(month, format='%B').month) & (read_consumption['0'].index.year == int(year))]
    c_wind = data_of_month[:len(data_of_month_con)]
    consumption = data_of_month_con.values.tolist()

    X = np.arange(0, len(consumption), 1)
    idx = pd.date_range('2024-01-01 00:00', periods=len(consumption), freq='H')

power_output = [0] * len(X)
for i in range(len(n_turbines)):

    if n_turbines[i] > 1:
        y_value = [x * n_turbines[i] for x in y_value]
    if wind_mode:
        # Interpolating the power curve
        f = interpolate.interp1d(x_value, y_value, kind='cubic')
        if thirdheight:
            f2 = interpolate.interp1d(x_value2, y_value2, kind='cubic')
        # Going from wind data to power output, through the use of the power curve
        power_output = wind_module(c_wind, x_value, f)
        if thirdheight:
            power_output_b = wind_module(b_wind, x_value, f)
            #power_output_histogram(power_output)
            a_power = wind_module(mean['Wind Speed 101'], x_value, f)
            b_power = wind_module(mean['Wind Speed 99.5'], x_value, f)
            c_power = wind_module(mean['Wind Speed 50.0'], x_value, f)
    for j in range(len(bat_packs)):
        gen = 4000
        diesel_kwh = [0] * len(X)
        on = 0
        b_list = [0] * len(X)

        if wind_mode and bat_mode and gen_mode:
            max_output, b_list, diesel_kwh, on, needed, emission, not_enough, wasted, where, powbat = \
                wind_bat_gen(power_output, consumption, X, gen, bat_packs[j])
        if wind_mode is False and bat_mode and gen_mode:  # Currently not working, gen negative
            max_output, needed, diesel_kwh, b_list, on, emission = bat_gen(consumption, X, gen)
        if wind_mode is True and bat_mode is True and gen_mode is False:  # Has not been looked at in a while.
            max_output, needed, b_list = wind_bat(power_output, consumption, X)
        if wind_mode is False and bat_mode is False and gen_mode is True:
            max_output, needed, diesel_kwh, on, emission, not_enough, wasted = gen_solo(consumption, X, gen)
        if multiple_text:
            wastedlist.append(np.sum(wasted) - (b_list[-1]-b_list[0]))
            maxlist.append(np.sum(max_output))
            onlist.append(on)
            emissionlist.append(np.sum(emission)/1000)
            generatorlist.append(np.sum(diesel_kwh))
        temp = 0
        prod = 0
        if SCRLOLP:
            for x in X:
                temp += min(power_output[x]+max(0, b_list[x-1]-b_list[x]), consumption[x])
                prod += consumption[x]
            SSR = temp / prod
            #print(f'The SSR is {SSR}')
            temp = 0
            prod = 0
            for x in X:
                temp += min(power_output[x]+max(0, b_list[x-1]-b_list[x]), consumption[x])
                prod += power_output[x]+max(0, b_list[x-1]-b_list[x])
            SCR = temp / prod
            #print(f'The SCR is {SCR}')

            LOLP = 0
            for x in X:
                if power_output[x]+max(0, b_list[x-1]-b_list[x]) < consumption[x]:
                    LOLP += 1
            LOLPprint = LOLP/len(consumption)*100
            print(f'{SSR*100:.2f} & {SCR*100:.2f} & {LOLPprint:.2f} &')
        if wind_mode:
            print(f'Calculated scenario: {n_turbines[i]}{name}/{bat_packs[j]*60}')
            #print(f'Yearly emission {(np.sum(emission) / 1000) / 20:.2f} tons of CO2')
            #print(f'emission percentage: {(np.sum(emission) / 1000) / 91086.595 * 100:.2f} %')
        #total_gen.append(np.sum(df_generator[f'{i},{j}']))

#seasonal_prod(a_power, b_power, c_power)

if compare_plot:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(power_output, label='Power output')
    ax.set_xlabel('Date')
    ax.set_ylabel('Power output [kWh]')

    ax2 = ax.twinx()  # create a second y-axis
    ax2.plot(consumption, label='Consumption', color='red')
    ax2.set_ylabel('Consumption [kWh]')

    plt.title(f'Highest consumption month versus lowest wind speed month')
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')
    plt.show()
if multiple_text:
    print(f'Wasted = {wastedlist}')
    print(f'Max output = {maxlist}')
    print(f'Emission = {emissionlist}')
    print(f'gen percentage = {generatorlist/np.sum(consumption)}')
#bar_plot(total_gen, "Summed kWh produced by generator", "Generator produced kWh by scenario", False)
#basic_plot(df_max, len(n_turbines), len(bat_packs), 'Generator comparison', "kWh", "time")
if scenario_text:
    if wind_mode:
        print(f'The wind turbines produces {np.sum(power_output): .3f} kWh.')
    print(f"The maximum energy produced adds up to {np.sum(max_output): .3f} kWh.")
    print('There is a lack in energy for: %d hours, which is %3.2f percent.' % (not_enough, not_enough/len(X)*100))
    if wind_mode:
        print(f'For these hours: {where}')
    print(f'The energy needed sums up to {abs(np.sum(needed))} kWh')
    print(f'The amount wasted is {np.sum(wasted): .3f} kWh, and max in an hour is {np.max(wasted): .3f} kW')
    print(f'Sum of energy from consumption is {np.sum(consumption): .3f} kWh')
    print(f'Sum of energy from diesel is {np.sum(diesel_kwh): .3f} kWh, which is '
          f'{(np.sum(diesel_kwh)/np.sum(consumption))*100: .2f}% of consumption.')
    print('Hours generator is on:', on)
    if gen_mode:
        print(f'This means that the generator emits {np.sum(emission)/1000: .3f} tons of CO2')

if time_plot:
    timeplot(X, consumption, b_list, power_output, diesel_kwh, needed, idx, wind_mode, bat_mode, gen_mode, n_turbines,
             name, bat_packs, timestep=500)

print('Program ended.')

