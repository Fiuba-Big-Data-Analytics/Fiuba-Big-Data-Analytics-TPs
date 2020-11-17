import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import seaborn as sns

import filter
from print import *
import graph_counter


def burocratic_code(counter):
    original = pd.read_csv("file.csv")
    filter.full_correction(original)

    original = original.drop_duplicates(subset="Opportunity_Name")

    set_up_stats(original)

    set_output("burocratic_code_stats.txt")
    burocratic_code_stats(original)
    burocratic_code_won(original, counter)
    reset_output()


def set_up_stats(df):
    df["Bureaucratic_Code_Won"] = df.loc[df["Stage"]
                                         == "Closed Won", :]["Bureaucratic_Code"]


def burocratic_code_stats(df):
    pd.options.mode.chained_assignment = None

    print_title("Estadística del Código Burocrático")

    print_subtitle("Cantidad de Códigos Burocráticos")

    printf(len(df["Bureaucratic_Code"].unique()))
    newline()

    print_subtitle("Mínimo Valor")

    printf(df["Bureaucratic_Code"].min())
    newline()

    print_subtitle("Máximo Valor")

    printf(df["Bureaucratic_Code"].max())
    newline()

    won = df.loc[df["Stage"] == "Closed Won", :]
    won["Won_Per_Code"] = won.groupby("Bureaucratic_Code")[
        "Stage"].transform("count")

    closed = df.loc[(df["Stage"] == "Closed Won") |
                    (df["Stage"] == "Closed Lost"), :]
    closed["Closed_Per_Code"] = closed.groupby("Bureaucratic_Code")[
        "Stage"].transform("count")

    won["Won_Per_Code_Normalized"] = won["Won_Per_Code"].divide(
        closed["Closed_Per_Code"])
    won_per_code_normalized = won.groupby("Bureaucratic_Code")[
        "Won_Per_Code_Normalized"]

    newline()

    print_subtitle("Cantidad de cada Código Burocrático")
    print_series(df["Bureaucratic_Code"].value_counts())

    div()

    print_subtitle("Éxito según el Código Burocrático")
    print_series(won_per_code_normalized.value_counts())

    pd.options.mode.chained_assignment = "warn"


def burocratic_code_won(df, counter):
    df["Bureaucratic_Code"] = df["Bureaucratic_Code"].astype(str)

    df["Bureaucratic_Code_Count"] = df.groupby(
        "Bureaucratic_Code")["Bureaucratic_Code"].transform("count")

    patch_blue = mpatches.Patch(
        color="#ff9999", label="Oportunidades en Total")
    patch_green = mpatches.Patch(
        color="#99ff99", label="Oportunidades Ganadas")

    plt.figure(counter.get_count())

    plt.bar(df["Bureaucratic_Code"].value_counts().index, df["Bureaucratic_Code"].value_counts(),
            width=0.7, align="center", color="#ff9999")

    df = df.loc[df["Stage"] == "Closed Won", :]

    plt.bar(df["Bureaucratic_Code"].value_counts().index,
            df["Bureaucratic_Code_Won"].value_counts(), width=0.7, align="center", color="#99ff99")

    plt.title("Oportunidades por Código Burocrático", pad=10)
    plt.xlabel("Código Burocrático")
    plt.ylabel("Frecuencia")

    plt.xticks(rotation=90, size=7.5)

    plt.legend(handles=[patch_blue, patch_green])

    plt.savefig("graphics/burocratic_code_bar.png")

    counter.increase_count()


counter = graph_counter.Counter()
burocratic_code(counter)
