import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import interpolate

from average import average_plot


def power_curve_plot(x_value, y_value, f, name, save):
    plt.xlabel('Wind speed (m/s)')
    plt.ylabel('Power output (kW)')
    plt.title(f'Power curve for {name}')
    plt.plot(x_value, y_value, 'o')
    plt.plot(x_value, f(x_value), '-')
    plt.xlim([0, 50])
    plt.ylim([0, 2500])
    plt.grid()
    if save:
        plt.savefig(f'Figures/powercurve_{name}.png')
    plt.show()
    return


def consumption_plot(df):
    # plot the data
    fig, ax = plt.subplots(figsize=(10, 6))
    df.plot(ax=ax, legend=False)

    # set x-ticks to the start of each year
    year_starts = pd.date_range(start=df.index[0], end=df.index[-1], freq='YS')
    ax.set_xticks(year_starts)

    # format x-tick labels to show only the year
    ax.set_xticklabels([tick.strftime('%Y') for tick in year_starts], rotation=45, ha='right')

    # Set the axis labels and title
    ax.set_xlabel('Year')
    ax.set_ylabel('Consumption [kWh]')
    ax.set_title('20 Years of consumption data of the Ocean Farm 1')
    plt.savefig('Figures/twenty_year_con.png')
    plt.show()
    return


def wind_plot(x_wind, y_wind):
    #idx = pd.date_range('1996-01-01 00:00', periods=len(y_wind), freq='H')
    plt.plot(x_wind, y_wind)
    plt.title('Wind speeds 1996-2015')
    plt.xlabel('Time (h)')
    plt.ylabel('Wind Speed (m/s)')
    plt.savefig('Figures/windspeeds1996-2015.png')
    plt.show()
    return


def engine_plot(diesel_eff, x_eff, y_eff):
    plt.plot(x_eff, y_eff, 'o')
    plt.plot(x_eff, diesel_eff(x_eff))
    plt.grid()
    plt.xlabel('Power output')
    plt.ylabel('Engine efficiency')
    plt.show()
    return


def basic_plot(df, k, l, name, y_label, c_name):
    for i in range(k):
        for j in range(l):
            ave = average_plot(df[c_name], df[f'{i},{j}'], 1000)
            plt.plot(df['time'], ave, label=f'{i},{j}')
    plt.title(name)
    plt.legend(loc='upper right')
    plt.xlabel('Time')
    plt.ylabel(y_label)
    plt.show()
    return


def bar_plot(data, ylabel, title, save):
    x_value = np.arange(0, len(data), 1)
    plt.bar(x_value, data)
    plt.xlabel("Scenario")
    plt.ylabel(ylabel)
    plt.title(title)
    if save:
        plt.savefig(f'Figures/{title}.png')
    plt.show()
    return


def sorted_bar_plot(wind_speeds, save, c_name):
    # Calculate the frequencies of each wind speed
    bins = np.arange(0, 41, 1)
    freq, _ = np.histogram(wind_speeds, bins=bins)

    # Create a pandas dataframe with the frequencies
    df = pd.DataFrame({'wind_speed': bins[:-1], 'frequency': freq})

    # Plot the frequency distribution as bars with lines between the bars
    plt.bar(df['wind_speed'], df['frequency'], width=1, align='edge', edgecolor='black')
    plt.xlabel('Wind speed (m/s)')
    plt.ylabel('Frequency')
    plt.title(f'{c_name} m.a.s.l. frequency distribution')
    if save:
        plt.savefig(f'Figures/{c_name}.png')
    plt.show()
    return


def plot_wind_and_power_freq(wind_speeds, power_output):
    # Calculate the frequencies of each wind speed
    bins_wind = np.arange(0, 41, 1)
    freq_wind, _ = np.histogram(wind_speeds, bins=bins_wind)

    # Calculate the frequencies of the power output values
    bins_power = np.arange(0, np.max(power_output) + 1000, 1000)
    freq_power, _ = np.histogram(power_output, bins=bins_power)

    # Create a pandas dataframe with the wind speed frequencies
    df_wind = pd.DataFrame({'wind_speed': bins_wind[:-1], 'frequency': freq_wind})

    # Create a pandas dataframe with the power output frequencies
    df_power = pd.DataFrame({'power_output': bins_power[:-1], 'frequency': freq_power})
    df_power = df_power[df_power['power_output'] <= np.max(power_output) + 1000]
    df_power = df_power[df_power['power_output'] >= 0]

    # Create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))

    # Plot the wind speed frequency distribution as bars with lines between the bars
    ax1.bar(df_wind['wind_speed'], df_wind['frequency'], width=1, align='edge', edgecolor='black')
    ax1.set_xlabel('Wind speed (m/s)')
    ax1.set_ylabel('Frequency')
    ax1.set_title('Wind speed frequency distribution')

    # Plot the power output frequency distribution as a line
    ax2.plot(df_power['power_output'], df_power['frequency'], 'r-')
    ax2.set_xlim([0, np.max(power_output) + 1000])
    ax2.set_ylim([0, np.max(freq_power) + 10])
    ax2.set_xlabel('Power output (W)')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Power output frequency distribution')

    return fig, (ax1, ax2)


def wind_speed_histogram(wind_speeds, bin_width, h):
    bins = np.arange(0, np.max(wind_speeds) + bin_width, bin_width)
    freq, _ = np.histogram(wind_speeds, bins=bins)
    plt.bar(bins[:-1], freq, width=bin_width, align="edge", edgecolor="black")
    plt.ylim([0, 15000])
    plt.xlim([0, 40])
    plt.xlabel("Wind speed (m/s)")
    plt.ylabel("Frequency")
    plt.title(f'Wind speed distribution for {h} m.a.s.l.')
    plt.savefig(f'Figures/windspeeddis{h}.png')
    plt.show()


def power_output_histogram(power_output, bin_width=50):
    bins = np.arange(0, np.max(power_output) + bin_width, bin_width)
    freq, _ = np.histogram(power_output, bins=bins)
    plt.bar(bins[:-1], freq, width=bin_width, align="edge", edgecolor="black")
    plt.xlabel("Power output (kWh)")
    plt.ylabel("Frequency")
    plt.title("Power output distribution for SWT-2.3-113")
    plt.savefig(f'Figures/Power output distributionSWT.png')
    plt.show()


def power_coef_plot(x_value, y_value, name, save):
    plt.xlabel('Wind speed (m/s)')
    plt.ylabel('Power coefficient')
    plt.title(f'Power coefficient for {name}')
    plt.plot(x_value, y_value, 'o')
    f = interpolate.interp1d(x_value, y_value, kind='cubic')
    plt.plot(x_value, f(x_value), '-')
    plt.grid()
    if save:
        plt.savefig(f'Figures/powercoefficient_{name}.png')
    plt.show()
    return


def one_year_plot():
    one_year = pd.read_excel('Forbruk_OF_korr.xlsx')
    one_year_idx = pd.date_range('2021-01-01 00:00', periods=len(one_year), freq='H')
    one_year = one_year.set_index([one_year_idx])
    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(one_year.index, one_year['Forbruk [kW]'])

    # Set the ticks and labels
    xtick_loc = one_year.resample('M').mean().index + pd.offsets.MonthBegin(1) - pd.Timedelta(28, 'D')
    ax.set_xticks(xtick_loc)
    ax.set_xticklabels(xtick_loc.strftime('%B'), rotation=45, ha='right')
    # Set the x-axis label
    ax.set_xlabel('Month')

    # Set the y-axis label
    ax.set_ylabel('Consumption [kWh]')

    # Set the title
    ax.set_title('Consumption data of one year from Ocean Farm 1')
    # Show the plot
    plt.savefig('Figures/one_year_consumption.png')
    plt.show()


def mean_std_con(df):
    # Assuming your data is in a pandas DataFrame called `df` with a datetime index
    monthly_data = df.resample('M').mean()
    monthly_mean = monthly_data.mean(axis=1)
    monthly_std = monthly_data.std(axis=1, ddof=0)
    print(monthly_std)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(monthly_mean, label='Mean')
    ax.fill_between(monthly_data.index, monthly_mean - monthly_std, monthly_mean + monthly_std, alpha=0.4,
                    label='Standard Deviation')
    ax.legend()
    ax.set_xlabel('Year')
    ax.set_ylabel('Consumption [kWh]')
    plt.show()


def mean_std_con_year(df):
    # Assuming your data is in a pandas DataFrame called `df` with a datetime index
    yearly_data = df.resample('M').mean()
    yearly_mean = yearly_data.mean(axis=1)
    yearly_std = yearly_data.std(axis=1)
    print(yearly_std)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(yearly_mean, label='Mean')
    ax.fill_between(yearly_data.index, yearly_mean - yearly_std, yearly_mean + yearly_std, alpha=0.4,
                    label='Standard Deviation')
    ax.legend()
    ax.set_xlabel('Year')
    ax.set_ylabel('Wind speed (m/s)')
    plt.show()


def timeplot(X, consumption, b_list, power_output, diesel_kwh, needed, idx, wind_mode, bat_mode, gen_mode, n_turbines,
             name, bat_packs, timestep):
    ave_con = average_plot(X, consumption, timestep)
    if bat_mode:
        chosen_average = average_plot(X, b_list, timestep)
    if wind_mode:
        other_average = average_plot(X, power_output, timestep)
    if gen_mode:
        gen_ave = average_plot(X, diesel_kwh, timestep)
    need_ave = average_plot(X, needed, timestep)
    plt.figure(figsize=(10, 6))
    plt.xlabel('Year')
    plt.ylabel('kWh')
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
        plt.savefig('base_case.png')
    plt.show()


def group_plot(df):
    # Group the data by month and hour
    grouped = df.groupby([df.index.month, df.index.hour])

    # Calculate the mean wind speed for each month and hour
    mean_wind_speed = grouped.mean()

    # Plot the mean wind speed for each month and hour
    mean_wind_speed.plot(figsize=(12, 6))
    plt.xlabel('Month and Hour')
    plt.ylabel('Consumption [kWh]')
    plt.title(f'Seasonal Variations in the consumption over 20 Years')
    plt.savefig('Figures/seasonalvariationcon.png')
    plt.show()


def meanstdbar_plot(wind):
    # Calculate the mean and standard deviation for each column
    mean = np.mean(wind[['Wind Speed 101', 'Wind Speed 99.5', 'Wind Speed 50']], axis=0)
    std = np.std(wind[['Wind Speed 101', 'Wind Speed 99.5', 'Wind Speed 50']], axis=0)

    # Create a bar chart showing the mean wind speed and standard deviation for each column
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(['101', '99.5', '50'], mean, yerr=std, capsize=5)
    ax.set_ylabel('Mean Wind Speed (m/s)')
    ax.set_xlabel('Height (m.a.s.l.)')
    plt.savefig('Figures/meanstdthreeheights.png')
    plt.show()


def meanstdcon(df):
    # calculate mean and standard deviation for each year
    yearly_mean = df.groupby(df.index.month).apply(np.mean)
    yearly_std = df.groupby(df.index.month).apply(np.std)
    years = []
    for year in range(2024, 2044):
        years.append(str(year))
    # plot the results
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(yearly_mean.index, yearly_mean, yerr=yearly_std, capsize=4)
    #ax.set_xticks(years)
    #ax.set_xticklabels(years, rotation=45)
    ax.set_xlabel('Year')
    ax.set_ylabel('Mean Wind Speed (m/s)')
    ax.set_title('Mean Wind Speed per Year with Standard Deviation')
    #plt.savefig('Figures/meanstdwind.png')
    plt.show()


def confreq(df):
    # Flatten the dataframe into a Series
    consumption = df.stack()

    # Plot the histogram with 50 bins
    fig, ax = plt.subplots()
    consumption.hist(bins=50, ax=ax, edgecolor='black')
    ax.grid(False)
    # Set the plot labels
    ax.set_xlabel('Energy from generator [kWh]')
    ax.set_ylabel('Frequency')
    ax.set_title('Generator Frequency Plot (SWT/1200)')
    plt.savefig('Figures/diefreq.png')
    # Show the plot
    plt.show()


def emission_plot():
    emission_list = [3262.15, 1481.32, 1402.39, 1372.12, 1346.31, 1129.6, 1040.88, 1004.48, 972.90, 953.37, 866.81,
                     830.28, 798.05, 705.338, 623.33, 587.76, 556.25]
    x_axis = np.arange(0, len(emission_list), 1)
    labels = ['Base Case', '1S2x/0', '1S2x/1200', '1S2x/1800', '1S2x/2400', '2S2x/0', '2S2x/1200', '2S2x/1800',
              '2S2x/2400', '3S2x/0', '3S2x/1200', '3S2x/1800', '3S2x/2400', 'SWT/0', 'SWT/1200', 'SWT/1800',
              'SWT/2400']
    twenty = 0.2 * emission_list[0]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xticks(x_axis)
    ax.set_xticklabels(labels, rotation=30, ha='right')
    ax.set_yticks(np.arange(0, 6000, 500))
    ax.plot(x_axis, emission_list)
    ax.set_xlabel('Scenario')
    ax.set_ylabel('Emission (tons')
    ax.set_title('Emission in tons by Scenario')
    plt.grid()
    plt.axhline(y=twenty, color='r')
    ax.text(-0.5, twenty, "20 % of Base Case", ha="right", va="bottom", color="r")
    plt.savefig('Figures/emissionbyscenario.png')
    plt.show()
    return


def diesel_plot():
    diesel_max = [5660.4798964351085, 4713.50694780554, 4675.992176476462, 4667.555561368581, 4658.490167969307,
                  4039.437533301029, 3936.757760429382, 3896.400802688124, 3862.641229276157, 3571.7900832324126,
                  3428.338119380571, 3367.385477411131, 3313.71347132398, 2740.9251045537353, 2558.2647684877616,
                  2480.31478002967, 2419.369957417569]
    diesel_min = [4209.572700480878, 585.7126816954881, 433.31517031304213, 375.7288587856899, 324.1675041868724,
                  375.72850347936384, 264.96654268321333, 215.6466385588212, 178.5562902979011, 288.22919897024497,
                  201.35712003327123, 160.75952765901687, 127.97562623081566, 228.7910215923156, 155.74142478033437,
                  119.38850125605136, 88.16903570966946]
    diesel_std = [280.9525639169696, 796.0624679577357, 821.0625861329654, 832.1495688208815, 841.4012484165302,
                  686.9682429391488, 691.8546180094593, 695.0829720019101, 697.1275380646462, 617.1308707590197,
                  612.4686513680792, 611.3673168452215, 609.8320723033764, 474.05929196276594, 461.00658511764846,
                  457.44558669187035, 454.19275430623367]
    diesel_mean = [5090.740814248144, 2311.667272251175, 2188.5041353251577, 2141.253372150787, 2100.9855215984003,
                   1762.789963528148, 1624.345782218431, 1567.5357907651219, 1518.260338483044, 1487.7785237030441,
                   1352.6936570599553, 1295.6933672394869, 1245.3999235754502, 1100.714716083865, 972.73473003891,
                   917.2214259636569, 868.0486374357281]
    x_axis = np.arange(0, len(diesel_max), 1)
    labels = ['Base Case', '1S2x/0', '1S2x/1200', '1S2x/1800', '1S2x/2400', '2S2x/0', '2S2x/1200', '2S2x/1800',
              '2S2x/2400', '3S2x/0', '3S2x/1200', '3S2x/1800', '3S2x/2400', 'SWT/0', 'SWT/1200', 'SWT/1800',
              'SWT/2400']
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xticks(x_axis)
    ax.set_xticklabels(labels, rotation=30, ha='right')
    ax.set_yticks(np.arange(0, 6000, 500))
    ax.plot(x_axis, diesel_mean, 'o-', label='Mean')
    ax.fill_between(x_axis, diesel_min, diesel_max, alpha=0.2, label='Range')
    ax.set_xlabel('Scenario')
    ax.set_ylabel('Diesel (l)')
    ax.set_title('Diesel (l) needed in a month by Scenario')
    plt.grid()
    plt.legend()
    plt.savefig('Figures/newdieselbyscenario.png')
    plt.show()


def seasonal_prod(a_power, b_power, c_power):
    # create x-axis values (assuming it's a range from 0 to len(a_power))
    x_value = range(len(a_power))

    # plot three lines on the same graph
    fig, ax = plt.subplots(figsize=(12, 6))
    # set x-axis tick labels to show month abbreviations for every 24 values
    ticks = np.arange(0, 288, 24)
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    ax.set_xticks(ticks)
    ax.set_xticklabels(months)
    ax.plot(x_value, a_power, label='Wind Speed 101')
    ax.plot(x_value, b_power, label='Wind Speed 99.5')
    ax.plot(x_value, c_power, label='Wind Speed 50')

    ax.set_xlabel('Time (months)')
    ax.set_ylabel('Power Production (kW)')
    ax.set_title('Seasonal Variation of Power Production')
    ax.legend()
    plt.savefig('Figures/seasonalvariationpowerproduction.png')
    plt.show()
