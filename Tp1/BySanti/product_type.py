import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import seaborn as sns

import filter
from print import *
import graph_counter


def product_type(counter):
    original = pd.read_csv("file.csv")
    filter.full_correction(original)

    set_output("product_type_stats.txt")
    product_type_stats(original)

    reset_output()
    return


def product_type_stats(df):
    pd.options.mode.chained_assignment = None

    won = df.loc[df["Stage"] == "Closed Won", :]
    won["Won_Per_Type"] = won.groupby("Product_Type")[
        "Stage"].transform("count")

    # print(won["Won_Per_Type"].value_counts().to_string())

    closed = df.loc[(df["Stage"] == "Closed Won") |
                    (df["Stage"] == "Closed Lost"), :]
    # closed["Closed_Per_Type"] = closed.groupby("Product_Type")[
    #    "Stage"].transform("count")

    # won["Won_Per_Type_Normalized"] = won["Won_Per_Type"].divide(
    #    closed["Closed_Per_Type"])
    # won_per_type_normalized = won.groupby("Product_Type")[
    #    "Won_Per_Type_Normalized"]

    stage = df.groupby("Stage")["Product_Type"].value_counts().to_string()

    print_title("Estadística del Tipo de Producto")

    print_subtitle("Cantidad de cada Tipo de Producto")
    printt(df["Product_Type"].value_counts().to_string())

    div()

    print_subtitle("Casos Cerrados según Tipo de Producto")
    printt(closed["Product_Type"].value_counts().to_string())

    newline()

    print_subtitle("Casos Ganados según Tipo de Producto")
    if (won["Product_Type"].count() == 0):
        printt("0 para todos los Productos")

    newline()

    print_subtitle("Etapa según Tipo de Producto")
    printf(stage)

    pd.options.mode.chained_assignment = "warn"


counter = graph_counter.Counter()
product_type(counter)
