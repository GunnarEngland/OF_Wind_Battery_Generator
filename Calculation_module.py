from Battery_module import battery_charge, battery_deplete, bat
from diesel_aggregate import gen_drain, efficiency_curve, co2_emission


def wind_bat_gen(power_output, consumption, X, gen, n_batteries):
    # Battery module
    pack = 60.00  # One module of battery in kWh
    battery_capacity = n_batteries * pack  # Max capacity for batteries
    battery = 0.2 * battery_capacity
    max_charge = 0.25*pack * n_batteries  # How much a battery can charge in an hour
    max_output = power_output.copy()
    needed = [0] * len(X)
    diesel_kwh = [0] * len(X)
    emission = [0] * len(X)
    b_list = []  # Initiate list used for the battery values.
    operative = 0
    on = 0
    f = efficiency_curve()
    not_enough = 0
    where = []
    powbat = []
    wasted = [0] * len(X)
    generator_mode = False
    for x in X:
        if battery > 0.5 * battery_capacity or operative > 3:
            generator_mode = False
        needed[x] = consumption[x] - power_output[x]  # needed > 0 means energy deficit
        if power_output[x] > consumption[x]:
            chargeable = min(power_output[x] - consumption[x], max_charge)
            powbat.append(chargeable)
        battery_old = battery
        battery, min_charge, needed[x], change = bat(battery, max_charge, battery_capacity, needed[x])
        new_charge = min(max_charge, max_charge - abs(change))
        #if battery > battery_old:
        #    chargedbywind = battery - battery_old
        #    powbat.append(chargedbywind)
        if min_charge:
            generator_mode = True
        if needed[x] > 0 and power_output[x] < consumption[x]:  # check if there is not enough wind power and battery is not charged enough
            if battery < 0.8 * battery_capacity:  # check if battery is not almost fully charged
                generator_mode = True
        if generator_mode:  # Checks if generator is on
            diesel_kwh[x], battery, needed[x], change = gen_drain(needed[x], battery, new_charge, battery_capacity,
                                                                  change, gen)
            operative += 1
            on += 1
        depleted = battery_old - battery
        if needed[x] > 0:
            not_enough += 1
            where.append(x)
        elif needed[x] < 0:
            needed[x] = 0
        wasted[x] = power_output[x] + diesel_kwh[x] - consumption[x]
        max_output[x] = power_output[x] + depleted + diesel_kwh[x]
        b_list.append(battery)
        emission[x] = co2_emission(f, diesel_kwh[x], 0.25)
    return max_output, b_list, diesel_kwh, on, needed, emission, not_enough, wasted, where, powbat


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
    wasted = [0] * len(X)
    gen_eff = 0.3 * gen  # Can contemplate implementing an efficiency curve based on operative power
    on = 0
    f = efficiency_curve()
    not_enough = 0
    for x in X:
        power_output[x] = consumption[x]
        diesel_kwh[x] = consumption[x]
        if power_output[x] > gen_eff:
            needed[x] = gen_eff - power_output[x]
            power_output[x] = gen_eff
            diesel_kwh[x] = gen_eff
            not_enough += 1
        on += 1
        emission[x] = co2_emission(f, power_output[x], diesel_per_kWh=0.25)
    return power_output, needed, diesel_kwh, on, emission, not_enough, wasted
