import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import filter
from format import *

original = pd.read_csv("file.csv")

filter.full_correction(original)

filas = len(original.index)
columnas = len(original.columns)

def basic_analysis(df):

    basic_stats(df)
    null_stats(df)
    #var_stats(df)
    #value_counts_stats(df)

def basic_stats(df):
    print_title("Estadística Básica")

    printt(f"Cantidad de datos: {original.size}")
    printt(f"Cantidad de filas: {original.shape[0]}")
    printt(f"Cantidad de columnas: {original.shape[1]}")

def null_stats(df):
    print_title("Completitud del Set")

    for col in original:
        cant = original[col].isnull().value_counts().tolist()
        if cant[0] == filas: continue

        nulos = cant[1]
        porcentaje = cant[1] /filas
        
        printt(f"{col}: {pretty_f(porcentaje, 3)}% - {nulos}/{filas}")

def var_stats(df):
    print_title("Estadísitca de las Variables")

    types = df.dtypes

    for col in df:
        if types[col] not in {np.dtype('float64'), np.dtype('int64')}: continue

        print_subtitle(col)
        print_series(df[col].describe())
        print()

def value_counts_stats(df):
    for col in df:
        print_subtitle(col)
        print(df[col].value_counts())
        print()

basic_analysis(original)

