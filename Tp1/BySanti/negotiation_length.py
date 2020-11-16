import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import seaborn as sns

import filter
from print import *
import graph_counter


def negotiation_length(counter):
    original = pd.read_csv("file.csv")
    filter.full_correction(original)

    original = original.loc[(original["Stage"] == "Closed Won") | (
        original["Stage"] == "Closed Lost"), :]
    original = original.drop_duplicates(subset="Opportunity_Name")

    set_up_stats(original)

    set_output("negotiation_length_stats.txt")
    negotiation_length_stats(original)
    negotiation_length_won(original, counter)

    reset_output()


def set_up_stats(df):
    df["Negotiation_Length"] = df["Last_Modified_Date"] - \
        df["Opportunity_Created_Date"]
    df["Negotiation_Length"] = df["Negotiation_Length"].apply(lambda x: x.days)
    df["Negotiation_Length_Won"] = df.loc[df["Stage"]
                                          == "Closed Won", :]["Negotiation_Length"]
    df["Negotiation_Length_Lost"] = df.loc[df["Stage"]
                                           == "Closed Lost", :]["Negotiation_Length"]


def negotiation_length_stats(df):
    print_title("Estadística General de la Duración")
    print_subtitle("Medidas Estadísticas Generales")

    amount = df["Negotiation_Length"].count()
    avg = df["Negotiation_Length"].mean()
    minimum = df["Negotiation_Length"].min()
    maximum = df["Negotiation_Length"].max()
    std_dev = df["Negotiation_Length"].std()
    median = df["Negotiation_Length"].median()

    printt(f"Cantidad de Datos & {amount}")
    printt(f"Promedio de los Valores & {pretty_f(avg)}")
    printt(f"Valor Mínimo & {minimum}")
    printt(f"Valor Máximo & {maximum}")
    printt(f"Desviación Estándar & {pretty_f(std_dev)}")
    printt(f"Mediana & {median}")

    newline()

    print_subtitle("Medidas Estadísticas de las Oportunidades Ganadas")
    amount_won = df["Negotiation_Length_Won"].count()
    avg_won = df["Negotiation_Length_Won"].mean()
    minimum_won = df["Negotiation_Length_Won"].min()
    maximum_won = df["Negotiation_Length_Won"].max()
    std_dev_won = df["Negotiation_Length_Won"].std()
    median_won = df["Negotiation_Length_Won"].median()

    printt(f"Cantidad de Datos & {amount_won}")
    printt(f"Promedio de los Valores & {pretty_f(avg_won)}")
    printt(f"Valor Mínimo & {minimum_won}")
    printt(f"Valor Máximo & {maximum_won}")
    printt(f"Desviación Estándar & {pretty_f(std_dev_won)}")
    printt(f"Mediana & {median_won}")

    newline()

    print_subtitle("Medidas Estadísticas de las Oportunidades Perdidas")
    amount_lost = df["Negotiation_Length_Lost"].count()
    avg_lost = df["Negotiation_Length_Lost"].mean()
    minimum_lost = df["Negotiation_Length_Lost"].min()
    maximum_lost = df["Negotiation_Length_Lost"].max()
    std_dev_lost = df["Negotiation_Length_Lost"].std()
    median_lost = df["Negotiation_Length_Lost"].median()

    printt(f"Cantidad de Datos & {amount_lost}")
    printt(f"Promedio de los Valores & {pretty_f(avg_lost)} ")
    printt(f"Valor Mínimo & {minimum_lost}")
    printt(f"Valor Máximo & {maximum_lost}")
    printt(f"Desviación Estándar & {pretty_f(std_dev_lost)}")
    printt(f"Mediana & {median_lost}")

    newline()


def negotiation_length_won(df, counter):
    q1 = df["Negotiation_Length"].quantile(0.25)
    q3 = df["Negotiation_Length"].quantile(0.75)
    ric = q3 - q1
    li = q1 - 1.5 * ric
    ls = q3 + 1.5 * ric
    df = df.loc[df["Negotiation_Length"] > li, :]
    df = df.loc[df["Negotiation_Length"] < ls, :]
    max_value = df["Negotiation_Length"].max()

    patch_red = mpatches.Patch(color="#ff9999", label="Oportunidades en Total")
    patch_green = mpatches.Patch(
        color="#99ff99", label="Oportunidades Ganadas")

    plt.figure(counter.get_count())
    sns.set_style("whitegrid")
    sns.histplot(df["Negotiation_Length"], binwidth=10,
                 color="#ff9999", kde=True, line_kws={"alpha": 1}, alpha=1)
    sns.histplot(df["Negotiation_Length_Won"],
                 binwidth=10, color="#99ff99", kde=True, line_kws={"alpha": 1}, alpha=1)

    plt.title("Oportunidades Ganadas según Duración de la Negociación ")
    plt.xlabel("Duración de la Negociación")
    plt.ylabel("Frecuencia")

    plt.legend(handles=[patch_red, patch_green])
    plt.xlim(0, 610)

    plt.savefig("graphics/negotiation_length.png")

    counter.increase_count()


counter = graph_counter.Counter()
negotiation_length(counter)
