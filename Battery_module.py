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
        ba_neg = lower_capacity - battery
        battery = lower_capacity
        lower = True
    elif battery > upper_capacity:
        wasted = battery - upper_capacity
        battery = upper_capacity
    ba_neg = ba_neg + needed
    return battery, lower, ba_neg
