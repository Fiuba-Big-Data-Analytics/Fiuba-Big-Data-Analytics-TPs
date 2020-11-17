import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import seaborn as sns

import filter
from print import *
import graph_counter


def stage(counter):
    original = pd.read_csv("file.csv")
    filter.full_correction(original)

    set_output("stage_stats.txt")

    stage_stats(original)
    stage_graph(original, counter)

    original = original.loc[original["Stage"] == "Closed Won", :]

    reset_output()


def stage_stats(df):
    df = df.drop_duplicates(subset="Opportunity_ID")
    print_title("Estadísticas de Stage")

    print_subtitle("Cantidad de cada Valor")

    print_series(df["Stage"].value_counts())
    newline()

    print_subtitle("Cantidad Relativa de cada Valor")
    print_series(df["Stage"].value_counts(normalize=True))
    newline()

    print_subtitle("Porcentaje de Éxito")
    df = df.loc[(df["Stage"] == "Closed Won") |
                (df["Stage"] == "Closed Lost"), :]
    print_series(df["Stage"].value_counts(normalize=True))


def stage_graph(df, counter):
    df = df.drop_duplicates(subset="Opportunity_ID")

    df = df.loc[(df["Stage"] == "Closed Won") |
                (df["Stage"] == "Closed Lost"), :]
    plt.figure(counter.get_count())
    plt.pie(df["Stage"].value_counts(normalize=True),
            labels=df["Stage"].value_counts().index,
            colors=["#99ff99", "#ff9999"],
            autopct='%2.2f%%',
            pctdistance=0.80,
            startangle=30,
            explode=[0.05, 0.05])

    plt.title("Oportunidades Ganadas vs Perdidas")

    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    plt.gcf().gca().add_artist(centre_circle)

    plt.savefig("graphics/stage.png")
    counter.increase_count()


counter = graph_counter.Counter()
stage(counter)
