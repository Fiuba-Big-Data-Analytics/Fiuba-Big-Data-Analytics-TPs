import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

import filter
from print import *

original = pd.read_csv("file.csv")

filter.full_correction(original)

filas = len(original.index)
columnas = len(original.columns)

creation = original

creation["Opportunity_Created_Year"] = creation["Opportunity_Created_Date"].apply(lambda x: x.year)
creation["Opportunity_Created_Month"] = creation["Opportunity_Created_Date"].apply(lambda x: x.month)
creation["Opportunity_Created_Day"] = creation["Opportunity_Created_Date"].apply(lambda x: x.day)

#won = creation.loc[creation["Stage"] == "Closed Won", :]
#won["Won_Per_Month"] = won.groupby("Opportunity_Created_Month")["Stage"].transform("count")

#closed = creation.loc[(creation["Stage"] == "Closed Won") | (creation["Stage"] == "Closed Lost"), :]  
#closed["Closed_Per_Month"] = closed.groupby("Opportunity_Created_Month")["Stage"].transform("count")

#won["Won_Per_Month_Normalized"] = won["Won_Per_Month"] / closed["Closed_Per_Month"]
#won["Won_Per_Month_Normalized"].plot(kind="hist")
#won_per_month_normalized = won.groupby("Opportunity_Created_Month")["Won_Per_Month_Normalized"]
#plt.show()
#print(won_per_month_normalized)
#plt.figure(4)
#plt.hist()
#plt.show()
#won_per_month_normalized.plot(y=)

#won_normalized = won["Won_Per_Month"].divide(closed["Closed_Per_Month"])
#print(won_normalized.value_counts().to_string())

#print(creation.groupby("Opportunity_Created_Month")["Stage"].value_counts(normalize=True).reset_index())

#creation = creation.loc[(creation["Stage"] == "Closed Won") | (creation["Stage"] == "Closed Lost"), :]  
#creation = creation.groupby("Opportunity_Created_Month")["Stage"].value_counts(normalize=True)
#print(creation)

def opportunity_year(df):
    print(df["Opportunity_Created_Year"].value_counts().to_string())
    values = len(df["Opportunity_Created_Year"].value_counts())
    print(f"values:{values}")
    bins = np.arange(2012, 2012 + values + 1) + 0.5
    plt.figure(3)
    plt.hist(df["Opportunity_Created_Year"], bins, ec="black")
    plt.title("Oportunidades por Año")
    plt.xlabel("Año")
    #plt.xticks([x for x in range(2013,2013+values+1)])
    #plt.xlim(2013, values+1)
    plt.ylabel("Frecuencia")
    plt.savefig("graphics/year_hist.png")

def opportunity_month(df):
    print(df["Opportunity_Created_Month"].value_counts().to_string())
    values = len(df["Opportunity_Created_Month"].value_counts())
    bins = np.arange(values + 1) + 0.5
    plt.hist(df["Opportunity_Created_Month"], bins, ec="black")
    plt.title("Oportunidades por Mes")
    plt.xlabel("Mes")
    plt.xticks([x for x in range(1,values+1)])
    plt.xlim(0, values+1)
    plt.ylabel("Frecuencia")
    plt.savefig("graphics/months_hist.png")

def opportunity_day(df):
    print(df["Opportunity_Created_Day"].value_counts().to_string())
    values = len(df["Opportunity_Created_Day"].value_counts())
    bins = np.arange(values + 1) + 0.5
    plt.figure(2)
    plt.hist(df["Opportunity_Created_Day"], bins, ec="black")
    plt.title("Oportunidades por Día")
    plt.xlabel("Día")
    plt.xticks([x for x in range(1,values+1)])
    plt.xlim(0, values+1)
    plt.ylabel("Frecuencia")
    plt.savefig("graphics/days_hist.png")

#opportunity_year(creation)
#opportunity_month(creation)
#opportunity_day(creation)