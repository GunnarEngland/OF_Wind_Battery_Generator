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


def bat_test(prev_battery, wind_output, consumption, max_charge, capacity, needed):
    lower = False
    new_battery = prev_battery - max(min(needed, max_charge), -max_charge)
    if needed > max_charge:
        needed = needed - max_charge
    if new_battery > 0.8 * capacity:
        new_battery = 0.8 * capacity
        needed = consumption - wind_output + prev_battery - new_battery
    elif new_battery < 0.2 * capacity:
        needed = needed - 0.2 * capacity + new_battery
        new_battery = 0.2 * capacity
        lower = True
    if needed > 0:
        lower = True
    delta_battery = new_battery - prev_battery
    needed = consumption - wind_output - max(delta_battery, 0)
    return new_battery, lower, needed, delta_battery

