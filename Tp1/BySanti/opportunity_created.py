import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import seaborn as sns

import filter
from print import *
import graph_counter


def set_up_stats(df):
    df["Opportunity_Created_Year"] = df["Opportunity_Created_Date"].apply(
        lambda x: x.year)
    df["Opportunity_Created_Month"] = df["Opportunity_Created_Date"].apply(
        lambda x: x.month)
    df["Opportunity_Created_Day"] = df["Opportunity_Created_Date"].apply(
        lambda x: x.day)

    aux = df.loc[df["Stage"] == "Closed Won", :]
    df["Opportunity_Created_Year_Won"] = aux["Opportunity_Created_Date"].apply(
        lambda x: x.year)
    df["Opportunity_Created_Month_Won"] = aux["Opportunity_Created_Date"].apply(
        lambda x: x.month)
    df["Opportunity_Created_Day_Won"] = aux["Opportunity_Created_Date"].apply(
        lambda x: x.day)


def opportunity_created(counter):
    original = pd.read_csv("file.csv")
    filter.full_correction(original)

    # filas = len(original.index)
    # columnas = len(original.columns)

    set_up_stats(original)

    set_output("opportunity_stats.txt")
    opportunity_stats(original)

    counter.increase_count()
    opportunity_year(original, counter)
    opportunity_month(original, counter)
    opportunity_day(original, counter)
    opportunity_year_won(original, counter)
    opportunity_month_won(original, counter)
    opportunity_day_won(original, counter)
    reset_output()


def opportunity_stats(df):
    pd.options.mode.chained_assignment = None

    won = df.loc[df["Stage"] == "Closed Won", :]
    won["Won_Per_Month"] = won.groupby("Opportunity_Created_Month")[
        "Stage"].transform("count")

    closed = df.loc[(df["Stage"] == "Closed Won") |
                    (df["Stage"] == "Closed Lost"), :]
    closed["Closed_Per_Month"] = closed.groupby("Opportunity_Created_Month")[
        "Stage"].transform("count")

    won["Won_Per_Month_Normalized"] = won["Won_Per_Month"].divide(
        closed["Closed_Per_Month"])
    won["Won_Per_Month_Normalized"].plot(kind="hist")
    won_per_month_normalized = won.groupby("Opportunity_Created_Month")[
        "Won_Per_Month_Normalized"]

    print_title("Estadísticas de la Fecha de Creación de las Oportunidades")

    print_subtitle("Oportunidades según el Día")
    printt(df["Opportunity_Created_Day"].value_counts().to_string())
    newline()

    print_subtitle("Oportunidades según el Mes")
    printt(df["Opportunity_Created_Month"].value_counts().to_string())
    newline()

    print_subtitle("Oportunidades según el Año")
    printt(df["Opportunity_Created_Year"].value_counts().to_string())
    newline()

    div()

    print_subtitle("Éxito según el Mes de Creación")
    printt(won_per_month_normalized.value_counts().to_string())

    pd.options.mode.chained_assignment = "warn"


def opportunity_year(df, counter):
    values = len(df["Opportunity_Created_Year"].value_counts())
    bins = np.arange(2012, 2012 + values + 1) + 0.5

    plt.figure(counter.get_count())
    plt.hist(df["Opportunity_Created_Year"], bins, ec="black")

    plt.title("Oportunidades por Año")
    plt.xlabel("Año")
    plt.ylabel("Frecuencia")

    plt.savefig("graphics/year_hist.png")

    counter.increase_count()


def opportunity_year_won(df, counter):
    values = len(df["Opportunity_Created_Year"].value_counts())
    bins = np.arange(2012, 2012 + values + 1) + 0.5
    patch_blue = mpatches.Patch(color="blue", label="Oportunidades en Total")
    patch_green = mpatches.Patch(color="green", label="Oportunidades Ganadas")

    plt.figure(counter.get_count())
    plt.hist(df["Opportunity_Created_Year"], bins, ec="black", color="blue")
    plt.hist(df["Opportunity_Created_Year_Won"],
             bins, ec="black", color="green")

    plt.title("Oportunidades por Año Ganadas")
    plt.xlabel("Año")
    plt.ylabel("Frecuencia")

    plt.legend(handles=[patch_blue, patch_green])

    plt.savefig("graphics/year_won_hist.png")

    counter.increase_count()


def opportunity_month(df, counter):
    values = len(df["Opportunity_Created_Month"].value_counts())
    bins = np.arange(values + 1) + 0.5

    plt.figure(counter.get_count())
    plt.hist(df["Opportunity_Created_Month"], bins, ec="black")
    plt.title("Oportunidades por Mes")
    plt.xlabel("Mes")
    plt.ylabel("Frecuencia")

    plt.xticks([x for x in range(1, values+1)])
    plt.xlim(0, values+1)

    plt.savefig("graphics/months_hist.png")

    counter.increase_count()


def opportunity_month_won(df, counter):
    values = len(df["Opportunity_Created_Month"].value_counts())
    bins = np.arange(values + 1) + 0.5

    patch_blue = mpatches.Patch(color="blue", label="Oportunidades en Total")
    patch_green = mpatches.Patch(
        color="green", label="Oportunidades Ganadas")

    plt.figure(counter.get_count())
    plt.hist(df["Opportunity_Created_Month"], bins, ec="black")
    plt.hist(df["Opportunity_Created_Month_Won"],
             bins, ec="black", color="green")

    plt.title("Oportunidades por Mes")
    plt.xlabel("Mes")
    plt.ylabel("Frecuencia")

    plt.xticks([x for x in range(1, values+1)])
    plt.xlim(0, values+1)

    plt.legend(handles=[patch_blue, patch_green])

    plt.savefig("graphics/months_won_hist.png")

    counter.increase_count()


def opportunity_day(df, counter):
    values = len(df["Opportunity_Created_Day"].value_counts())
    bins = np.arange(values + 1) + 0.5

    plt.figure(counter.get_count())
    plt.hist(df["Opportunity_Created_Day"], bins, ec="black")

    plt.title("Oportunidades por Día")
    plt.xlabel("Día")
    plt.ylabel("Frecuencia")

    plt.xticks([x for x in range(1, values+1)])
    plt.xlim(0, values+1)

    plt.savefig("graphics/days_hist.png")

    counter.increase_count()


def opportunity_day_won(df, counter):
    values = len(df["Opportunity_Created_Day"].value_counts())
    bins = np.arange(values + 1) + 0.5

    patch_blue = mpatches.Patch(color="blue", label="Oportunidades en Total")
    patch_green = mpatches.Patch(
        color="green", label="Oportunidades Ganadas")

    plt.figure(counter.get_count())
    plt.hist(df["Opportunity_Created_Day"], bins, ec="black")
    plt.hist(df["Opportunity_Created_Day_Won"],
             bins, ec="black", color="green")

    plt.title("Oportunidades por Día")
    plt.xlabel("Día")
    plt.ylabel("Frecuencia")

    plt.xticks([x for x in range(1, values+1)])
    plt.xlim(0, values+1)

    plt.legend(handles=[patch_blue, patch_green])

    plt.savefig("graphics/days_won_hist.png")

    counter.increase_count()


counter = graph_counter.Counter()
opportunity_created(counter)
