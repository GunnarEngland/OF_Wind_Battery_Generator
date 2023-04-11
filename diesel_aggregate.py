# Ocean Farm 1 currently uses 3 times 184 kW diesel generators according to Sindre
from Battery_module import battery_charge, bat_test
from scipy import interpolate
import numpy as np

# ------------------------------------------
# Gen drain takes energy from the generator to cover the needed energy.
# It uses the leftover energy to charge the battery.
# Input
# needed = energy needed to cover the consumption.
# battery = amount of energy in the battery.
# max_charge = How much energy the batteries can charge in an hour.
# capacity = max capacity of battery.
# gen = size of generator.

# Output
# kwh = amount of energy used from generator
# battery = new value of battery
# missing = amount of energy missing incase generator is not enough
# -------------------------------------------------------------------


def gen_drain(needed, consumption, output, battery, max_charge, capacity, change, gen):
    gen_eff = 0.3*gen  # 1200 (30% of 4000)
    battery_old = battery
    if gen_eff > needed:
        kwh = needed + max(battery - battery_old, 0)
    elif gen_eff <= needed:
        missing = needed - gen_eff
        kwh = gen_eff
    missing = max(consumption - output - change - kwh, 0)
    return kwh, battery, missing, change


def gen_mode(battery, max_capacity, operative):
    if battery >= 0.8 * max_capacity and operative > 5:
        operative = 0
        mode = False
        return mode, operative
    operative += 1
    mode = True
    return mode, operative


def co2_emission(f, output, diesel_per_kWh):
    diesel_consumption = f(output) * diesel_per_kWh  # Find numbers from papers
    emission = diesel_consumption * 2.67  # Find number from papers
    return emission


def efficiency_curve():
    x_eff = range(0, 1400, 100)  # len() = 14
    y_eff = [0.0, 6.5, 13, 17.5, 21.5, 25, 28, 30.5, 32, 33, 34, 34.5, 34.75, 35]
    f = interpolate.interp1d(x_eff, y_eff, kind='cubic')
    return f
