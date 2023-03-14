#  Should have three different if not more def() that depend on inputs
from Battery_module import battery_charge, battery_deplete
from diesel_aggregate import gen_drain, efficiency_curve, co2_emission


def wind_bat_gen(power_output, consumption, X, gen, n_batteries):
    # Battery module
    pack = 60.00  # One module of battery in kWh
    battery_capacity = n_batteries * pack  # Max capacity for batteries
    lower_capacity = 0.1 * battery_capacity
    max_charge = 6 * n_batteries  # How much a battery can charge in an hour
    max_output = power_output.copy()
    needed = [0] * len(X)
    diesel_kwh = [0] * len(X)
    emission = [0] * len(X)
    b_list = []  # Initiate list used for the battery values.
    generator_mode = False
    battery = lower_capacity
    operative = 0
    on = 0
    f = efficiency_curve()
    for x in X:
        drained = False  # If the battery has been drained, then True
        depleted = 0  # How much the battery has been drained this hour
        charged = 0  # How much the battery has been charged this hour
        if battery > 0.6 * battery_capacity and operative > 5:
            generator_mode = False
            operative = 0
        # generator_mode, operative = gen_mode(battery, battery_capacity, operative)
        if power_output[x] > consumption[x]:
            battery, charged, surplus = battery_charge(battery, max_charge, battery_capacity,
                                                       (power_output[x] - consumption[x]), charged)
            needed[x] = 0
        elif power_output[x] < consumption[x]:  # checks if output from wind does not cover consumption
            battery_old = battery
            battery, min_charge, ba_neg = battery_deplete(battery,
                                                          (consumption[x] - power_output[x]), lower_capacity,
                                                          battery_capacity)
            drained = True
            needed[x] = ba_neg
            if min_charge:
                # generator_mode, operative = gen_mode(battery, battery_capacity, operative)
                if not generator_mode and needed[x] > 0:
                    generator_mode = True
            # elif not min_charge:
            depleted = battery_old - battery
        if generator_mode:  # Checks if generator is on
            if consumption[x] > power_output[x]:
                needed[x] = consumption[x] - power_output[x] - depleted
                diesel_kwh[x], battery, missing = gen_drain(needed[x], battery, max_charge,
                                                            battery_capacity, drained, charged, gen, f)
                # battery = battery_charge(battery, max_charge, battery_capacity, max_charge)
                needed[x] = consumption[x] - power_output[x] - diesel_kwh[x] - depleted + missing

            #  Not sure if this elif is needed? battery_charge is already embedded in gen_drain if surplus > 0.
            #  Also embedded above in elif power_output > consumption outside gen_mode
            #  Little to no change in removing both the charge below and inside gen_drain for scenario 0,1
            elif power_output[x] > consumption[x]:
                if not drained:
                    battery, charged, surplus = battery_charge(battery, max_charge, battery_capacity,
                                                               0.3*gen, charged)
            operative += 1
            on += 1
        if needed[x] < 0:
            needed[x] = 0
        if diesel_kwh[x] < 0:
            diesel_kwh[x] = 0
        max_output[x] = power_output[x] + depleted + (diesel_kwh[x])
        b_list.append(battery)
        emission[x] = co2_emission(f, diesel_kwh[x], 0.25)

        # c_list.append(depleted)
    return max_output, b_list, diesel_kwh, on, needed, emission


def wind_bat(power_output, consumption, X):
    # Battery module
    pack = 60.00  # One module of battery in kWh
    n_batteries = 10  # Amount of modules
    battery_capacity = n_batteries * pack  # Max capacity for batteries
    lower_capacity = 0.1 * battery_capacity
    max_charge = 6 * n_batteries  # How much a battery can charge in an hour
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
            battery, min_charge, ba_neg = battery_deplete(battery,
                                                          (consumption[x] - power_output[x]),
                                                          lower_capacity, battery_capacity)
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
    n_batteries = 10  # Amount of modules
    battery_capacity = n_batteries * pack  # Max capacity for batteries
    lower_capacity = 0.1 * battery_capacity
    max_charge = 6 * n_batteries  # How much a battery can charge in an hour
    battery = lower_capacity
    needed = [0] * len(X)
    b_list = [0] * len(X)
    diesel_kwh = [0] * len(X)
    power_output = [0] * len(X)
    emission = [0] * len(X)
    generator_mode = False
    operative = 0
    on = 0
    f = efficiency_curve()

    for x in X:
        min_charge = True
        drained = False
        depleted = 0.0
        if battery >= 0.8 * battery_capacity and operative > 5:
            generator_mode = False
            operative = 0
        if generator_mode:
            on += 1
        battery_old = battery
        needed[x] = consumption[x]
        if battery > lower_capacity:
            battery, min_charge, ba_neg = battery_deplete(battery, consumption[x], lower_capacity, battery_capacity)
            depleted = battery_old - battery
            needed[x] = needed[x] - depleted + ba_neg
            drained = True
        if min_charge:
            generator_mode = True
            diesel_kwh[x], battery, needed[x] = gen_drain(needed[x], battery, max_charge, battery_capacity, drained,
                                                          gen)
        power_output[x] = diesel_kwh[x] + depleted
        b_list[x] = battery
        emission[x] = co2_emission(f, diesel_kwh[x], diesel_per_kWh=0.25)
    return power_output, needed, diesel_kwh, b_list, on, emission


def gen_solo(consumption, X, gen):
    power_output = [0] * len(X)
    diesel_kwh = [0] * len(X)
    needed = [0] * len(X)
    emission = [0] * len(X)
    gen_eff = 0.3 * gen  # Can contemplate implementing an efficiency curve based on operative power
    on = 0
    f = efficiency_curve()
    for x in X:
        power_output[x] = consumption[x]
        diesel_kwh[x] = consumption[x]
        if power_output[x] > gen_eff:
            needed[x] = gen_eff - power_output[x]
            power_output[x] = gen_eff
            diesel_kwh[x] = gen_eff
        on += 1
        emission[x] = co2_emission(f, power_output[x], diesel_per_kWh=0.25)
    return power_output, needed, diesel_kwh, on, emission
