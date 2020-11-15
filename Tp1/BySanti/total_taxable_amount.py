import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math
import numpy as np
import seaborn as sns

import filter
from print import *
import graph_counter


def total_taxable_amount(counter):
    original = pd.read_csv("file.csv")
    original = original[original["Total_Amount"].notna()]
    filter.full_correction(original)
    original = original.loc[(original["Stage"] == "Closed Won")
                            | (original["Stage"] == "Closed Lost")]

    set_up_stats(original)

    set_output("total_taxable_amount_stats.txt")

    original = original.drop_duplicates(subset="Opportunity_Name")

    tot_sum_compare(original)
    tot_tax_basic_stats(original)
    tot_tax_success(original, counter)
    benford(original, counter)

    reset_output()
    return


def set_up_stats(df):
    df["Total_Taxable_Amount_Won"] = df.loc[df["Stage"]
                                            == "Closed Won", :]["Total_Taxable_Amount"]
    df["Total_Taxable_Amount_Lost"] = df.loc[df["Stage"]
                                             == "Closed Lost", :]["Total_Taxable_Amount"]

    df["Total_Amount_Manual"] = df.groupby("Opportunity_ID")[
        "Total_Amount"].transform("sum")
    df["Amounts_Equal"] = df["Total_Amount_Manual"] == df["Total_Taxable_Amount"]


def tot_sum_compare(df):
    print_title("Comparación con Columna Total Amount")
    print_subtitle("Suma de Precios de Productos Igual a Total")
    print_series(df["Amounts_Equal"].value_counts())
    newline()


def tot_tax_basic_stats(df):
    print_title("Estadística Básica de Total Taxable Amount por Moneda")
    for currency in df["Total_Taxable_Amount_Currency"].unique():
        print_title(f"{currency}")
        cut_df = df.loc[df["Total_Taxable_Amount_Currency"]
                        == currency, :]
        _tot_tax_basic_stats(cut_df, currency)
        newline()


def _tot_tax_basic_stats(df, currency):
    print_subtitle("Medidas Estadísticas de las Oportunidades")
    amount = df["Total_Taxable_Amount"].count()
    uniques = len(df["Total_Taxable_Amount"].unique())
    avg = df["Total_Taxable_Amount"].mean()
    minimum = df["Total_Taxable_Amount"].min()
    maximum = df["Total_Taxable_Amount"].max()
    std_dev = df["Total_Taxable_Amount"].std()
    median = df["Total_Taxable_Amount"].median()

    printt(f"Cantidad de Datos: {amount}")
    printt(f"Cantidad de Valores Únicos: {uniques}")
    printt(f"Promedio de los Valores: {pretty_f(avg)}")
    printt(f"Valor Mínimo: {minimum}")
    printt(f"Valor Máximo: {maximum}")
    printt(f"Desviación Estándar: {pretty_f(std_dev)}")
    printt(f"Mediana: {median}")

    newline()

    print_subtitle("Medidas Estadísticas de las Oportunidades Ganadas")
    amount_won = df["Total_Taxable_Amount_Won"].count()
    uniques_won = len(df["Total_Taxable_Amount_Won"].unique())
    avg_won = df["Total_Taxable_Amount_Won"].mean()
    minimum_won = df["Total_Taxable_Amount_Won"].min()
    maximum_won = df["Total_Taxable_Amount_Won"].max()
    std_dev_won = df["Total_Taxable_Amount_Won"].std()
    median_won = df["Total_Taxable_Amount_Won"].median()

    printt(f"Cantidad de Datos: {amount_won}")
    printt(f"Cantidad de Valores Únicos: {uniques_won}")
    printt(f"Promedio de los Valores: {pretty_f(avg_won)}")
    printt(f"Valor Mínimo: {minimum_won}")
    printt(f"Valor Máximo: {maximum_won}")
    printt(f"Desviación Estándar: {pretty_f(std_dev_won)}")
    printt(f"Mediana: {median_won}")

    newline()

    print_subtitle("Medidas Estadísticas de las Oportunidades Perdidas")
    amount_lost = df["Total_Taxable_Amount_Lost"].count()
    uniques_lost = len(df["Total_Taxable_Amount_Lost"].unique())
    avg_lost = df["Total_Taxable_Amount_Lost"].mean()
    minimum_lost = df["Total_Taxable_Amount_Lost"].min()
    maximum_lost = df["Total_Taxable_Amount_Lost"].max()
    std_dev_lost = df["Total_Taxable_Amount_Lost"].std()
    median_lost = df["Total_Taxable_Amount_Lost"].median()

    printt(f"Cantidad de Datos: {amount_lost}")
    printt(f"Cantidad de Valores Únicos: {uniques_lost}")
    printt(f"Promedio de los Valores: {pretty_f(avg_lost)}")
    printt(f"Valor Mínimo: {minimum_lost}")
    printt(f"Valor Máximo: {maximum_lost}")
    printt(f"Desviación Estándar: {pretty_f(std_dev_lost)}")
    printt(f"Mediana: {median_lost}")


def tot_tax_success(df, counter):
    # Borro valores anómalos con un método estadístico
    q1 = df["Total_Taxable_Amount"].quantile(0.25)
    q3 = df["Total_Taxable_Amount"].quantile(0.75)
    ric = q3 - q1
    li = q1 - 1.5 * ric
    ls = q3 + 1.5 * ric
    df = df.loc[df["Total_Taxable_Amount"] < ls, :]
    df = df.loc[df["Total_Taxable_Amount"] > li, :]

    # max_value = df["Total_Taxable_Amount"].max()  # 1892975
    yticks = [x for x in range(0, 2000001, 2000000//8)]  # Rounded up, manually

    df = df.rename(columns={"Total_Taxable_Amount": "Precio Total (millones)",
                            "Total_Taxable_Amount_Currency": "Moneda", "Stage": "Resultado"})
    df["Resultado"] = df["Resultado"].replace(
        {"Closed Won": "Éxito", "Closed Lost": "Fracaso"})

    plt.figure(num=counter.get_count(), figsize=(6, 5))

    sns.set_theme(style="whitegrid")
    plt.title("Éxito de las Oportunidades según Precio y Moneda", pad=20)
    sns.violinplot(data=df, x="Moneda", y="Precio Total (millones)", hue="Resultado",
                   split=True, inner="quartile", linewidth=1, bw=0.1, palette=["#99ff99", "#ff9999"])

    plt.yticks(yticks)
    plt.ylim(-1000, 2000000)
    plt.tight_layout()
    plt.savefig("graphics/total_taxable_amount.png")

    # For some reason it is not needed
    counter.increase_count()


def benford(df, counter):
    digits = np.array([n for n in range(1, 10)])
    benford_values = np.array([(1 + 1/n) for n in range(1, 10)])
    benford_values = np.log(benford_values) / np.log(10)

    bins = np.arange(10) + 0.5
    patch_orange = mpatches.Patch(color="#ffcc99", label="Ley de Benford")
    patch_blue = mpatches.Patch(
        color="#66b3ff", label="Precio Total")

    df = df.loc[df["Total_Taxable_Amount"] != 0, :]
    df["TXA_First_Digit"] = df["Total_Taxable_Amount"].apply(
        lambda n: int(str(int(n))[:1]))

    plt.figure(counter.get_count(), facecolor="white")
    plt.title("Ley de Benford vs Precio Total", pad=15, size=15)

    plt.plot(digits, benford_values, color="#ffcc99")
    plt.hist(df["TXA_First_Digit"], bins, color="#66b3ff", density=True)

    plt.xticks(digits)
    plt.xlabel("Primer Dígito")
    plt.ylabel("Frecuencia Relativa")

    plt.legend(handles=[patch_blue, patch_orange])

    plt.grid(b=None)

    plt.tight_layout()
    plt.savefig("graphics/benford.png")
    counter.increase_count()


counter = graph_counter.Counter()
total_taxable_amount(counter)
