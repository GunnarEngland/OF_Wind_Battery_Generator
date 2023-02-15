# Program to split the dataframe object into a list of floats.
import pandas as pd


def string_to_float(item):
    for c in item:
        tmp = (c.strip('[').strip(']').split(', '))

    floats = [float(x) for x in tmp]
    return floats
