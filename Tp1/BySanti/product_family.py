import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import seaborn as sns

import filter
from print import *
import graph_counter


def product_family(counter):
    original = pd.read_csv("file.csv")
    filter.full_correction(original)

    set_up_stats(original)

    set_output("product_family_stats.txt")
    product_family_stats(original)
    product_family_won(original, counter)

    reset_output()
    return


def set_up_stats(df):
    df["Product_Family_Won"] = df.loc[df["Stage"]
                                      == "Closed Won", :]["Product_Family"]


def product_family_stats(df):
    pd.options.mode.chained_assignment = None

    print_title("Estadística del Tipo de Producto")

    print_subtitle("Cantidad de Familias de Productos")

    printf(len(df["Product_Family"].unique()))
    newline()

    print_subtitle("Mínimo Valor")

    printf(df["Product_Family"].min())
    newline()

    print_subtitle("Máximo Valor")

    printf(df["Product_Family"].max())
    newline()

    print_title("Estadística del Percentil 10 Superior de Frecuencia")

    percentile90 = df["Product_Family"].value_counts().quantile(0.9)
    df["Product_Family_Count"] = df.groupby(
        "Product_Family")["Product_Family"].transform("count")
    df = df.loc[df["Product_Family_Count"] > percentile90, :]

    won = df.loc[df["Stage"] == "Closed Won", :]
    won["Won_Per_Family"] = won.groupby("Product_Family")[
        "Stage"].transform("count")

    closed = df.loc[(df["Stage"] == "Closed Won") |
                    (df["Stage"] == "Closed Lost"), :]
    closed["Closed_Per_Family"] = closed.groupby("Product_Family")[
        "Stage"].transform("count")

    won["Won_Per_Family_Normalized"] = won["Won_Per_Family"].divide(
        closed["Closed_Per_Family"])
    won_per_family_normalized = won.groupby("Product_Family")[
        "Won_Per_Family_Normalized"]

    stage = df.groupby("Stage")["Product_Family"].value_counts().to_string()

    print_subtitle("Datos Incluidos")

    registers = df["Product_Family"].count()
    printt(f"Registros: {registers}")

    families = df["Product_Family"].value_counts().count()
    printt(f"Familias Distintas: {families}")

    newline()

    print_subtitle("Cantidad de cada Tipo de Producto")
    print_series(df["Product_Family"].value_counts())

    div()

    print_subtitle("Éxito según la Familia del Producto")
    print_series(won_per_family_normalized.value_counts())

    pd.options.mode.chained_assignment = "warn"


def product_family_won(df, counter):
    percentile90 = df["Product_Family"].value_counts().quantile(0.9)

    df["Product_Family"] = df["Product_Family"].astype(str)

    df["Product_Family_Count"] = df.groupby(
        "Product_Family")["Product_Family"].transform("count")

    df = df.loc[df["Product_Family_Count"] > percentile90, :]

    values = len(df["Product_Family"].value_counts())
    bins = np.arange(values + 1) + 0.5
    patch_blue = mpatches.Patch(
        color="#3333ff", label="Oportunidades en Total")
    patch_green = mpatches.Patch(
        color="#00bb00", label="Oportunidades Ganadas")

    plt.figure(counter.get_count())
    #plt.hist(df["Product_Family"], bins, ec="black", color="blue")

    # plt.hist(df["Product_Family_Won"],
    #         bins, ec="black", color="green")

    plt.bar(df["Product_Family"].value_counts().index, df["Product_Family"].value_counts(),
            width=0.7, align="center", color="#3333ff")
    # plt.bar(df["Product_Family_Won"].value_counts().index, df["Product_Family_Won"].value_counts(),
    #        width=0.7, align="center")

    df = df.loc[df["Stage"] == "Closed Won", :]

    plt.bar(df["Product_Family"].value_counts().index,
            df["Product_Family_Won"].value_counts(), width=0.7, align="center", color="#00bb00")

    plt.title("Oportunidades por Familia de Producto Ganadas")
    plt.xlabel("Familia Producto")
    plt.ylabel("Frecuencia")

    plt.xticks(rotation=90, size=7.5)

    plt.legend(handles=[patch_blue, patch_green])

    plt.savefig("graphics/product_family_hist.png")

    counter.increase_count()


counter = graph_counter.Counter()
product_family(counter)
