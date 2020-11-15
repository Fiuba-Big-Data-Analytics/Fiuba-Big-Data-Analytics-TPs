import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import seaborn as sns

import filter
from print import *
import graph_counter


def asp():
    original = pd.read_csv("file.csv")
    original = original[original["Total_Amount"].notna()]
    filter.full_correction(original)
    original = original.loc[(original["Stage"] == "Closed Won")
                            | (original["Stage"] == "Closed Lost")]

    # set_up_stats(original)

    set_output("asp_stats.txt")
    #original = original.drop_duplicates(subset="Opportunity_Name")
    asp_basic_stats(original)

    reset_output()
    return


def asp_basic_stats(df):
    print_title("Estadística del Precio Promedio de Venta")
    print(df.groupby("Opportunity_ID")["ASP_Currency"].nunique().max())


asp()
