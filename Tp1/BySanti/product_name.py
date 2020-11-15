import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import seaborn as sns

import filter
from print import *
import graph_counter


def product_name(counter):
    original = pd.read_csv("file.csv")
    filter.full_correction(original)

    set_up_stats(original)

    set_output("product_name_stats.txt")
    product_name_stats(original)
    product_name_won(original, counter)

    reset_output()
    return


def set_up_stats(df):
    df["Product_Name_Won"] = df.loc[df["Stage"]
                                    == "Closed Won", :]["Product_Name"]


def product_name_stats(df):
    pd.options.mode.chained_assignment = None

    print_title("Estadística del Tipo de Producto")

    print_subtitle("Cantidad de Nombres de Productos")

    printf(len(df["Product_Name"].unique()))
    newline()

    print_subtitle("Mínimo Valor")

    printf(df["Product_Name"].min())
    newline()

    print_subtitle("Máximo Valor")

    printf(df["Product_Name"].max())
    newline()

    print_title("Estadística del Percentil 10 Superior de Frecuencia")

    percentile90 = df["Product_Name"].value_counts().quantile(0.9)
    df["Product_Name_Count"] = df.groupby(
        "Product_Name")["Product_Name"].transform("count")
    df = df.loc[df["Product_Name_Count"] > percentile90, :]

    won = df.loc[df["Stage"] == "Closed Won", :]
    won["Won_Per_Name"] = won.groupby("Product_Name")[
        "Stage"].transform("count")

    closed = df.loc[(df["Stage"] == "Closed Won") |
                    (df["Stage"] == "Closed Lost"), :]
    closed["Closed_Per_Name"] = closed.groupby("Product_Name")[
        "Stage"].transform("count")

    won["Won_Per_Name_Normalized"] = won["Won_Per_Name"].divide(
        closed["Closed_Per_Name"])
    won_per_name_normalized = won.groupby("Product_Name")[
        "Won_Per_Name_Normalized"]

    stage = df.groupby("Stage")["Product_Name"].value_counts().to_string()

    print_subtitle("Datos Incluidos")

    registers = df["Product_Name"].count()
    printt(f"Registros: {registers}")

    names = df["Product_Name"].value_counts().count()
    printt(f"Nombres Distintos: {names}")

    newline()

    print_subtitle("Cantidad de cada Tipo de Producto")
    print_series(df["Product_Name"].value_counts())

    div()

    print_subtitle("Éxito según Nombre del Producto")
    print_series(won_per_name_normalized.value_counts())

    pd.options.mode.chained_assignment = "warn"


def product_name_won(df, counter):
    percentile90 = df["Product_Name"].value_counts().quantile(0.9)

    df["Product_Name"] = df["Product_Name"].astype(str)

    df["Product_Name_Count"] = df.groupby(
        "Product_Name")["Product_Name"].transform("count")

    df = df.loc[df["Product_Name_Count"] > percentile90, :]

    values = len(df["Product_Name"].value_counts())
    bins = np.arange(values + 1) + 0.5
    patch_red = mpatches.Patch(
        color="#ff9999", label="Oportunidades en Total")
    patch_green = mpatches.Patch(
        color="#99ff99", label="Oportunidades Ganadas")

    plt.figure(counter.get_count())
    #plt.hist(df["Product_Name"], bins, ec="black", color="blue")

    # plt.hist(df["Product_Name_Won"],
    #         bins, ec="black", color="green")

    plt.bar(df["Product_Name"].value_counts().index, df["Product_Name"].value_counts(),
            width=0.7, align="center", color="#ff9999")
    # plt.bar(df["Product_Name_Won"].value_counts().index, df["Product_Name_Won"].value_counts(),
    #        width=0.7, align="center")

    df = df.loc[df["Stage"] == "Closed Won", :]

    plt.bar(df["Product_Name"].value_counts().index,
            df["Product_Name_Won"].value_counts(), width=0.7, align="center", color="#99ff99")

    plt.title("Oportunidades por Nombre de Producto Ganadas")
    plt.xlabel("Nombre Producto")
    plt.ylabel("Frecuencia")

    plt.xticks(rotation=90, size=7.5)

    plt.legend(handles=[patch_red, patch_green])

    plt.savefig("graphics/product_name_hist.png")

    counter.increase_count()


counter = graph_counter.Counter()
product_name(counter)
