import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import seaborn as sns

import filter
from print import *
import graph_counter


def opportunity_owner(counter):
    original = pd.read_csv("file.csv")
    filter.full_correction(original)

    original = original.drop_duplicates(subset="Opportunity_Name")

    set_up_stats(original)

    set_output("opportunity_owner_stats.txt")
    opportunity_owner_stats(original)
    opportunity_owner_won(original, counter)

    reset_output()
    return


def set_up_stats(df):
    df["Opportunity_Owner_Won"] = df.loc[df["Stage"]
                                         == "Closed Won", :]["Opportunity_Owner"]
    df["Opportunity_Created_Month"] = df["Opportunity_Created_Date"].apply(
        lambda x: x.month)


def opportunity_owner_stats(df):
    print_title("Estadística del Tipo de Producto")

    print_subtitle("Rango de Identificadores")
    min_val = df["Opportunity_Owner"].min()
    max_val = df["Opportunity_Owner"].max()
    printt(f"{min_val} - {max_val}")

    newline()

    print_subtitle("Cantidad de Vendedores Totales")
    vendedores = df["Opportunity_Owner"].nunique()
    printt(f"{vendedores}")

    newline()

    print_subtitle("Cantidad de Vendedores Máximo en un Mes")
    max_vendedores = df.groupby("Opportunity_Created_Month")[
        "Opportunity_Owner"].nunique().max()
    printt(f"{max_vendedores}")

    newline()

    print_subtitle("Cantidad de Oportunidades Máxima por un Vendedor")
    opors = df.groupby("Opportunity_Owner")["Opportunity_ID"].nunique().max()
    printt(f"{opors}")

    newline()

    print_subtitle(
        "Cantidad de Oportunidades Máxima por un Vendedor en un Mes")
    max_opors = df.groupby(["Opportunity_Owner", "Opportunity_Created_Month"])[
        "Opportunity_ID"].nunique().max()
    printt(f"{max_opors}")

    newline()

    print_subtitle("Cantidad de Oportunidades Exitosas Máxima por un Vendedor")
    opors = df.groupby("Opportunity_Owner_Won")[
        "Opportunity_ID"].nunique().max()
    printt(f"{opors}")

    newline()

    print_subtitle(
        "Cantidad de Oportunidades Exitosas Máxima por un Vendedor en un Mes")
    max_opors = df.groupby(["Opportunity_Owner_Won", "Opportunity_Created_Month"])[
        "Opportunity_ID"].nunique().max()
    printt(f"{max_opors}")

    newline()


def opportunity_owner_won(df, counter):
    df["Opportunity_Owner"] = df["Opportunity_Owner"].astype(str)

    df["Opportunity_Owner_Count"] = df.groupby(
        "Opportunity_Owner")["Opportunity_ID"].transform("count")

    patch_red = mpatches.Patch(
        color="#ff9999", label="Oportunidades en Total")
    patch_green = mpatches.Patch(
        color="#99ff99", label="Oportunidades Ganadas")

    plt.figure(counter.get_count())

    plt.bar(df["Opportunity_Owner"].value_counts().index, df["Opportunity_Owner"].value_counts(),
            width=0.7, align="center", color="#ff9999")

    df = df.loc[df["Stage"] == "Closed Won", :]

    plt.bar(df["Opportunity_Owner"].value_counts().index,
            df["Opportunity_Owner_Won"].value_counts(), width=0.7, align="center", color="#99ff99")

    plt.title("Oportunidades por Vendedor", pad=10)
    plt.xlabel("Número de Vendedor")
    plt.ylabel("Frecuencia")

    plt.xticks(rotation=90, size=7.5)
    plt.xlim(-1, 53)
    plt.grid(b=True, axis="y")
    plt.legend(handles=[patch_red, patch_green])
    plt.tight_layout()
    plt.savefig("graphics/opportunity_owner_hist.png")

    counter.increase_count()


counter = graph_counter.Counter()
opportunity_owner(counter)
