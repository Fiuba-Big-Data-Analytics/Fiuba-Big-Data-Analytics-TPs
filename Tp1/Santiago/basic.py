import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import filter
from print import *


def basic_analysis(df):
    original = pd.read_csv("file.csv")

    filter.full_correction(original)

    basic_stats(df)
    null_stats(df)
    var_stats(df)
    value_counts_stats(df)
    return


def basic_stats(df):
    set_output("basic_stats.txt")

    print_title("Estadística Básica")

    printt(f"Cantidad de datos: {df.size}")
    printt(f"Cantidad de filas: {df.shape[0]}")
    printt(f"Cantidad de columnas: {df.shape[1]}")

    reset_output()


def null_stats(df):
    filas = len(df.index)
    columnas = len(df.columns)

    set_output("null_stats.txt")
    print_title("Completitud del Set")

    for col in df:
        cant = df[col].isnull().value_counts().tolist()
        if cant[0] == filas:
            continue

        nulos = cant[1]
        porcentaje = cant[1] / filas

        printt(f"{col}: {pretty_f(porcentaje, 3)}% - {nulos}/{filas}")

    reset_output()


def var_stats(df):
    set_output("var_stats.txt")
    print_title("Estadísitca de las Variables")

    types = df.dtypes

    for col in df:
        if types[col] not in {np.dtype('float64'), np.dtype('int64')}:
            continue

        print_subtitle(col)
        print_series(df[col].describe())
        div()

    reset_output()


def value_counts_stats(df):
    set_output("value_counts.txt")
    print_title("Value Counts por Variable")

    for col in df:
        print_subtitle(col)
        printf(df[col].value_counts())
        div()

    reset_output()
