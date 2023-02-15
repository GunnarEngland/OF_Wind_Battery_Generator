# Ocean Farm 1 currently uses 3 times 184 kW diesel generators according to Sindre
from Battery_module import battery_charge
from scipy import interpolate


def gen_drain(needed, battery, max_charge, capacity, gen):
    gen_eff = 0.3*gen
    charge = 0.8 * max_charge - battery
    if gen_eff > needed:
        surplus = gen_eff - needed
        if charge > 0 or surplus > 0:
            least = min(charge, surplus)
            if least < 0:
                least = 0
            battery, surplus = battery_charge(battery, max_charge, capacity, least)
            kwh = needed + least
            missing = 0.0
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


def co2_emission(consumption, output, gen, X):
    efficiency = [0] * len(X)
    x_value = range(0, 1400, 100)  # len() = 14
    y_value = [0.0, 6.5, 13, 17.5, 21.5, 25, 28, 30.5, 32, 33, 34, 34.5, 34.75, 35]
    f = interpolate.interp1d(x_value, y_value, kind='cubic')
    for x in X:
        efficiency[x] = f(output[x])
        diesel = output[x]/efficiency[x]
    return f, x_value, y_value, efficiency
