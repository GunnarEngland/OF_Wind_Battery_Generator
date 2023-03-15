from math import log10
h = 101  # Reference height of wind data
z0 = 0.001  # Roughness of surface, current value equals rough seas


def c_height(wind, hub_height):
    #if hub_height < h:  # Function cannot calculate wind at lower than reference.
    #    raise Exception('Hub height cannot be lower than reference height.')
        #h_0 = 0.01
        #wind_0 = [0.01] * len(wind)
        #for x in wind:
        #    h_changed = (log10(hub_height / z0) / log10(h_0 / z0)) * wind_0[x]
        #print(f'Height lower than reference, reference height set to 0')
    #    return h_changed, False
    if hub_height == h:  # Skip calculating the same wind speed.
        print('Height is the same, returned input.')
        return wind, True
    for x in wind:
        h_changed = (log10(hub_height / z0) / log10(h / z0)) * wind[x]
    print('Height for wind changed to ' + str(hub_height))
    return h_changed, False
