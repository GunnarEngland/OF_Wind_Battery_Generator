#  Should have three different if not more def() that depend on inputs
from Battery_module import battery_charge, battery_deplete
from diesel_aggregate import gen_drain


def wind_bat_gen(power_output, consumption, X, gen):
    # Battery module
    pack = 60.00  # One module of battery in kWh
    n_batteries = 20  # Amount of modules
    battery_capacity = n_batteries * pack  # Max capacity for batteries
    lower_capacity = 0.1 * battery_capacity
    max_charge = 40 * n_batteries  # How much a battery can charge in an hour
    max_output = power_output.copy()
    needed = [0] * len(X)
    diesel_kwh = [0] * len(X)
    b_list = []  # Initiate list that can be used for different things
    c_list = []  # Same as above. Used mainly for plotting.
    generator_mode = False
    gen_eff = gen * 0.3
    battery = lower_capacity
    operative = 0
    on = 0
    depleted = 0
    for x in X:
        if battery > 0.8 * battery_capacity and operative > 5:
            generator_mode = False
            operative = 0
        # generator_mode, operative = gen_mode(battery, battery_capacity, operative)
        if power_output[x] > consumption[x]:
            battery, surplus = battery_charge(battery, max_charge, battery_capacity, (power_output[x] - consumption[x]))
        elif power_output[x] < consumption[x]:  # checks if output from wind does not cover consumption
            battery_old = battery
            battery, min_charge, ba_neg = battery_deplete(battery, (consumption[x] - power_output[x]), lower_capacity)
            if min_charge:
                needed[x] = consumption[x] - power_output[x] - battery_old - battery + ba_neg
                # generator_mode, operative = gen_mode(battery, battery_capacity, operative)
                if not generator_mode and needed[x] > 0:
                    generator_mode = True
            depleted = battery_old - battery
        if generator_mode:  # Checks if generator is on
            if consumption[x] > power_output[x]:
                needed[x] = consumption[x] - power_output[x] - depleted
                diesel_kwh[x], battery, missing = gen_drain(needed[x], battery, max_charge, battery_capacity, gen)
            # battery = battery_charge(battery, max_charge, battery_capacity, max_charge)
            operative += 1
            on += 1
        max_output[x] = power_output[x] + depleted + (diesel_kwh[x])
        b_list.append(battery)
        # c_list.append(depleted)
    return max_output, b_list, diesel_kwh, on, needed


def wind_bat(power_output, consumption, X):
    # Battery module
    pack = 60.00  # One module of battery in kWh
    n_batteries = 20  # Amount of modules
    battery_capacity = n_batteries * pack  # Max capacity for batteries
    lower_capacity = 0.1 * battery_capacity
    max_charge = 40 * n_batteries  # How much a battery can charge in an hour
    battery = lower_capacity
    needed = [0] * len(X)
    b_list = [0] * len(X)
    max_output = power_output.copy()
    for x in X:
        depleted = 0
        if power_output[x] > consumption[x]:
            battery, surplus = battery_charge(battery, max_charge, battery_capacity, (power_output[x] - consumption[x]))
        elif power_output[x] < consumption[x]:  # checks if output from wind does not cover consumption
            battery_old = battery
            battery, min_charge, ba_neg = battery_deplete(battery, (consumption[x] - power_output[x]), lower_capacity)
            depleted = battery_old - battery
            if min_charge:
                needed[x] = consumption[x] - power_output[x] - battery_old - battery + ba_neg
        b_list[x] = battery
        max_output[x] = power_output[x] + depleted
    return max_output, needed, b_list


def bat_gen(consumption, X, gen):
    #  Gen currently not used, introduce as a max
    # Battery module
    pack = 60.00  # One module of battery in kWh
    n_batteries = 20  # Amount of modules
    battery_capacity = n_batteries * pack  # Max capacity for batteries
    lower_capacity = 0.1 * battery_capacity
    max_charge = 40 * n_batteries  # How much a battery can charge in an hour
    battery = lower_capacity
    gen_eff = 0.3*gen
    needed = [0] * len(X)
    b_list = [0] * len(X)
    diesel_kwh = [0] * len(X)
    power_output = [0] * len(X)
    generator_mode = False
    operative = 0

    for x in X:
        battery_old = battery
        needed[x] = consumption[x] - gen_eff - battery
        # Check if battery contains enough, elif gen contains enough, elif bat + gen
        if battery > consumption[x]:
            battery, min_charge, ba_neg = battery_deplete(battery, consumption[x], lower_capacity)
        elif gen_eff > consumption[x]:
            diesel_kwh[x], battery, needed[x] = gen_drain(needed[x], battery, max_charge, battery_capacity, gen)
        if battery > 0.8 * battery_capacity and operative > 5:
            generator_mode = False
            operative = 0


        if not generator_mode:
            battery, min_charge, ba_neg = battery_deplete(battery, (consumption[x] - power_output[x]), lower_capacity)
            if min_charge:
                needed[x] = consumption[x] - power_output[x] - battery_old - battery + ba_neg
                generator_mode = True
        if generator_mode:
            needed[x] = consumption[x] - power_output[x] - battery - battery_old
            diesel_kwh[x], battery, needed[x] = gen_drain(needed[x], battery, max_charge, battery_capacity, gen)
        b_list[x] = battery
    return power_output, needed, diesel_kwh, b_list


def gen_solo(consumption, X, gen):
    power_output = [0] * len(X)
    diesel_kwh = [0] * len(X)
    needed = [0] * len(X)
    gen_eff = 0.3*gen  # Can contemplate implementing an effeciency curve based on operative power
    on = 0
    for x in X:
        power_output[x] = consumption[x]
        diesel_kwh[x] = consumption[x]
        if power_output[x] > gen_eff:
            needed[x] = gen_eff - power_output[x]
            power_output[x] = gen_eff
            diesel_kwh[x] = gen_eff
        on += 1
    return power_output, needed, diesel_kwh, on
