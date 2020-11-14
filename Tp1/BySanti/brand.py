import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import seaborn as sns

import filter
from print import *
import graph_counter


def brand():
    original = pd.read_csv("file.csv")
    filter.full_correction(original)

    set_output("brand_stats.txt")
    print_series(original["Brand"].value_counts())

    reset_output()
    return


brand()
