# Module for charging the battery
# Siemens battery
# Tesvolt for solutions


def battery_charge(battery, max_charge, capacity, charge, charged):
    if charged > 0:  # If the battery has been charged earlier, will decrease max_charge capacity by said amount
        max_charge = max_charge - charged
    charge = min(charge, max_charge)
    battery = battery + max_charge
    surplus = charge - max_charge
    if battery > capacity:  # Prevents battery from exceeding max
        surplus = surplus + battery - capacity
        battery = capacity
    return battery, charged + charge, surplus


def battery_deplete(battery, depletion, lower_capacity, upper_capacity):
    ba_neg = 0.0
    max_depletion = 0.1 * upper_capacity
    needed = 0
    lower = False
    if depletion > max_depletion:
        needed = depletion - max_depletion
        depletion = max_depletion
    battery = battery - depletion
    if battery < lower_capacity:
        ba_neg = lower_capacity - battery  # If the battery lacks capacity to cover depletion
        battery = lower_capacity
        lower = True
    elif battery > upper_capacity:
        wasted = battery - upper_capacity
        battery = upper_capacity
    ba_neg = ba_neg + needed
    if ba_neg > 0:
        lower = True
    return battery, lower, ba_neg


def bat_test(battery, output, consumption, max_charge, capacity):
    lower = False
    needed = 0
    battery_old = battery
    if output > consumption:
        battery = battery + min(output-consumption, max_charge)
    elif output < consumption:
        battery = battery - min(consumption-output, max_charge)
        if consumption-output > max_charge:
            needed = consumption-output - max_charge
    change = battery - battery_old
    if battery > 0.8 * capacity:
        change = change - (battery - 0.8 * capacity)
        battery = 0.8 * capacity

    elif battery < 0.2 * capacity:
        needed = battery - 0.2 * capacity + needed
        change = change + (0.2 * capacity - battery)
        battery = 0.2 * capacity
        lower = True
    if needed > 0:
        lower = True
    return battery, lower, needed, change
# max = 1200, 1100 +120 = 1220,
# min = 120, 200 - 120 = 80, -120 + (0.2*capacity - battery) = -120 + (120 -80) = -120 + 40 = -80

