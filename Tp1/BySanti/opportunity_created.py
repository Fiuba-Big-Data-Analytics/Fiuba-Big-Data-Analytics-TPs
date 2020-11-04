import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import seaborn as sns

import filter
from print import *
import graph_counter

original = pd.read_csv("file.csv")

filter.full_correction(original)

filas = len(original.index)
columnas = len(original.columns)

creation = original

creation["Opportunity_Created_Year"] = creation["Opportunity_Created_Date"].apply(
    lambda x: x.year)
creation["Opportunity_Created_Month"] = creation["Opportunity_Created_Date"].apply(
    lambda x: x.month)
creation["Opportunity_Created_Day"] = creation["Opportunity_Created_Date"].apply(
    lambda x: x.day)

# sns.displot(creation["Opportunity_Created_Month"])

won = creation.loc[creation["Stage"] == "Closed Won", :]
creation["Opportunity_Created_Year_Won"] = won["Opportunity_Created_Date"].apply(
    lambda x: x.year)
creation["Opportunity_Created_Month_Won"] = won["Opportunity_Created_Date"].apply(
    lambda x: x.month)
creation["Opportunity_Created_Day_Won"] = won["Opportunity_Created_Date"].apply(
    lambda x: x.day)

# creation = creation.merge(won, left_on="ID", right_on="ID", how="left")
# print(creation["Opportunity_Created_Year"].value_counts())
# print(creation["Opportunity_Created_Year_Won"].value_counts())

# won["Won_Per_Month"] = won.groupby("Opportunity_Created_Month")["Stage"].transform("count")

# closed = creation.loc[(creation["Stage"] == "Closed Won") | (creation["Stage"] == "Closed Lost"), :]
# closed["Closed_Per_Month"] = closed.groupby("Opportunity_Created_Month")["Stage"].transform("count")

# won["Won_Per_Month_Normalized"] = won["Won_Per_Month"] / closed["Closed_Per_Month"]
# won["Won_Per_Month_Normalized"].plot(kind="hist")
# won_per_month_normalized = won.groupby("Opportunity_Created_Month")["Won_Per_Month_Normalized"]
# plt.show()
# print(won_per_month_normalized)
# plt.figure(4)
# plt.hist()
# plt.show()
# won_per_month_normalized.plot(y=)

# won_normalized = won["Won_Per_Month"].divide(closed["Closed_Per_Month"])
# print(won_normalized.value_counts().to_string())

# print(creation.groupby("Opportunity_Created_Month")["Stage"].value_counts(normalize=True).reset_index())

# creation = creation.loc[(creation["Stage"] == "Closed Won") | (creation["Stage"] == "Closed Lost"), :]
# creation = creation.groupby("Opportunity_Created_Month")["Stage"].value_counts(normalize=True)
# print(creation)


def opportunity_created(df):
    counter = graph_counter.Counter()

    opportunity_year(df, counter)
    opportunity_month(df, counter)
    opportunity_day(df, counter)
    opportunity_year_won(df, counter)
    opportunity_month_won(df, counter)
    opportunity_day_won(df, counter)


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


opportunity_created(creation)
