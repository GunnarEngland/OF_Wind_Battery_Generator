import numpy as np


def average_plot(X, chosen_average, window):
    ave = []
    for x in range(len(X) - window + 1):
        ave.append(np.mean(chosen_average[x:x+window]))
    for x in range(window - 1):
        ave.insert(0, np.nan)
    return ave