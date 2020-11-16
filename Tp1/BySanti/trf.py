import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import seaborn as sns

import filter
from print import *
import graph_counter


def trf(counter):
    original = pd.read_csv("file.csv")
    filter.full_correction(original)

    set_up_stats(original)

    set_output("trf_stats.txt")
    trf_stats(original)
    trf_won(original, counter)
    trf_cut_won(original, counter)

    reset_output()


def set_up_stats(df):
    df.rename(columns={"Total_Power": "TRF"}, inplace=True)
    df["TRF_Won"] = df.loc[df["Stage"] == "Closed Won", :]["TRF"]
    df["TRF_Lost"] = df.loc[df["Stage"] == "Closed Lost", :]["TRF"]


def trf_stats(df):
    print_title("Estadística de Toneladas de Refrigeración")

    print_subtitle("Valores Únicos")
    val_unicos = df["TRF"].nunique()
    printt(f"{val_unicos}")

    newline()

    print_subtitle("Medidas Estadísticas")

    avg = df["TRF"].mean()
    minimum = df["TRF"].min()
    maximum = df["TRF"].max()
    std_dev = df["TRF"].std()
    median = df["TRF"].median()

    printt(f"Promedio & {pretty_f(avg)}")
    printt(f"Mínimo & {minimum}")
    printt(f"Máximo & {maximum}")
    printt(f"Desviación Estándar & {pretty_f(std_dev)}")
    printt(f"Mediana & {median}")

    newline()

    print_subtitle("Medidas Estadísticas de las Oportunidades Ganadas")
    avg_won = df["TRF_Won"].mean()
    minimum_won = df["TRF_Won"].min()
    maximum_won = df["TRF_Won"].max()
    std_dev_won = df["TRF_Won"].std()
    median_won = df["TRF_Won"].median()

    printt(f"Promedio de los Valores & {pretty_f(avg_won)}")
    printt(f"Valor Mínimo & {minimum_won}")
    printt(f"Valor Máximo & {maximum_won}")
    printt(f"Desviación Estándar & {pretty_f(std_dev_won)}")
    printt(f"Mediana & {median_won}")

    newline()

    print_subtitle("Medidas Estadísticas de las Oportunidades Perdidas")
    avg_lost = df["TRF_Lost"].mean()
    minimum_lost = df["TRF_Lost"].min()
    maximum_lost = df["TRF_Lost"].max()
    std_dev_lost = df["TRF_Lost"].std()
    median_lost = df["TRF_Lost"].median()

    printt(f"Promedio de los Valores & {pretty_f(avg_lost)} ")
    printt(f"Valor Mínimo & {minimum_lost}")
    printt(f"Valor Máximo & {maximum_lost}")
    printt(f"Desviación Estándar & {pretty_f(std_dev_lost)}")
    printt(f"Mediana & {median_lost}")

    newline()


def trf_won(df, counter):
    percentile90 = df["TRF"].value_counts().quantile(0.75)

    df["TRF"] = df["TRF"].astype(str)

    df["TRF_Count"] = df.groupby(
        "TRF")["TRF"].transform("count")

    df = df.loc[df["TRF_Count"] > percentile90, :]

    print_subtitle("Percentil 25 Superior")
    datos = df["TRF"].count()
    printt(f"Datos: {datos}")

    values = len(df["TRF"].value_counts())
    bins = np.arange(values + 1) + 0.5
    patch_red = mpatches.Patch(
        color="#ff9999", label="Oportunidades en Total")
    patch_green = mpatches.Patch(
        color="#99ff99", label="Oportunidades Ganadas")

    plt.bar(df["TRF"].value_counts().index, df["TRF"].value_counts(),
            width=0.7, align="center", color="#ff9999")

    df = df.loc[df["Stage"] == "Closed Won", :]

    plt.bar(df["TRF"].value_counts().index,
            df["TRF_Won"].value_counts(), width=0.7, align="center", color="#99ff99")

    plt.title("Oportunidades por Potencia del Producto")
    plt.xlabel("Potencia (TRF)")
    plt.ylabel("Frecuencia")
    plt.xticks(rotation=90, size=7.5)
    plt.legend(handles=[patch_red, patch_green])

    plt.savefig("graphics/trf_hist.png")

    counter.increase_count()


def trf_cut_won(df, counter):
    df["TRF"] = pd.to_numeric(df["TRF"])
    df = df.loc[(df["Stage"] == "Closed Won") |
                (df["Stage"] == "Closed Lost"), :]

    q1 = df["TRF"].quantile(0.25)
    q3 = df["TRF"].quantile(0.75)
    ric = q3 - q1
    li = q1 - 1.5 * ric
    ls = q3 + 1.5 * ric
    df.loc[df["TRF"] > ls, "TRF"] = -1

    df["TRF"] = df["TRF"].astype(str)
    df["TRF"].replace({"-1": "Otro"}, inplace=True)

    # df = df.loc[df["TRF"] > li, :]

    labels = []
    sizes = []
    labels_stage = []
    sizes_stage = []
    colors = ["#66b3ff", "#ffcc99",   "#dfa7f2", "#ffb3e6", ]
    stages = ["Closed Won", "Closed Lost"]
    colors_stage_values = {"Closed Won": "#99ff99", "Closed Lost": "#ff9999"}
    colors_stage = []

    for value in df["TRF"].unique():
        labels.append(f"{value} TRF")
        cut = df.loc[df["TRF"] == value, :]
        sizes.append(cut["TRF"].count())

        for stage in stages:
            labels_stage.append(stage)
            cut2 = cut.loc[cut["Stage"] == stage, :]
            sizes_stage.append(cut2["Stage"].count())
            colors_stage.append(colors_stage_values[stage])

    labels[0] = "Otros"

    patch_red = mpatches.Patch(color="#ff9999", label="Oportunidades Fallidas")
    patch_green = mpatches.Patch(
        color="#99ff99", label="Oportunidades Exitosas")

    plt.figure(counter.get_count())
    plt.title("Oportunidades según Toneladas de Refrigeración", pad=20)
    plt.pie(sizes, labels=labels, colors=colors, startangle=60,
            frame=True, autopct='%2.2f%%', pctdistance=0.87)
    plt.pie(sizes_stage, colors=colors_stage, radius=0.75, startangle=60)
    centre_circle = plt.Circle(
        (0, 0), 0.5, color='black', fc='white', linewidth=0)
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    plt.axis('equal')
    plt.tight_layout()
    plt.legend(handles=[patch_red, patch_green])

    plt.savefig("graphics/trf_pie.png")
    counter.increase_count()


counter = graph_counter.Counter()
trf(counter)
