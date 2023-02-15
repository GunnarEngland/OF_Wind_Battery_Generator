# Module for charging the battery
# Siemens battery
# Tesvolt for solutions


def battery_charge(battery, max_charge, capacity, charge):
    surplus = 0
    charge = min(charge, max_charge)
    if charge > max_charge:
        battery = battery + max_charge  # implement max charge per hour
        surplus = charge - max_charge
    else:
        battery = battery + charge
    if battery > capacity:  # Prevents battery from exceeding max, is there a better way?
        surplus = surplus + battery - capacity
        battery = capacity
    return battery, surplus


def battery_deplete(battery, depletion, lower_capacity, upper_capacity):
    ba_neg = 0.0
    max_depletion = 0.1 * upper_capacity
    if depletion > max_depletion:
        depletion = max_depletion
    battery = battery - depletion
    if battery < lower_capacity:
        ba_neg = lower_capacity - battery
        battery = lower_capacity
        return battery, True, ba_neg
    elif battery > upper_capacity:
        battery = upper_capacity
    return battery, False, ba_neg
