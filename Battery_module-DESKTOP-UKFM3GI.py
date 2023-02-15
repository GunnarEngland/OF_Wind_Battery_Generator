# Module for charging the battery
# Siemens battery
# Tesvolt for solutions


def battery_charge(battery, max_charge, capacity, charge):
    surplus = 0
    if charge > max_charge:
        battery = battery + max_charge  # implement max charge per hour
    else:
        battery = battery + charge
    if battery > capacity:  # Prevents battery from exceeding max, is there a better way?
        surplus = battery - capacity
        battery = capacity
    return battery, surplus


def battery_deplete(battery, depletion, lower_capacity):
    ba_neg = 0.0
    battery = battery - depletion
    if battery < lower_capacity:
        ba_neg = lower_capacity - battery
        battery = lower_capacity
        return battery, True, ba_neg
    return battery, False, ba_neg
