# Ocean Farm 1 currently uses 3 times 184 kW diesel generators according to Sindre
from Battery_module import battery_charge
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


def gen_drain(needed, battery, max_charge, capacity, drained, charged, gen):
    missing = 0.0
    gen_eff = 0.3*gen  # 1200 (30% of 4000)
    battery_old = battery
    if gen_eff > needed:
        surplus = gen_eff - needed
        least = min(max_charge, surplus)  # least is how much the battery can be charged
        if least > 0 and drained is False:
            battery, charge, surplus = battery_charge(battery, max_charge, capacity, least, charged)
            kwh = needed + battery - battery_old
        else:
            kwh = needed
    elif gen_eff <= needed:
        missing = needed - gen_eff
        kwh = gen_eff
    return kwh, battery, missing


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
