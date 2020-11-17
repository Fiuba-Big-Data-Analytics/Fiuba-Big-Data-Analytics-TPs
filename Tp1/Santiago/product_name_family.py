import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import seaborn as sns

import filter
from print import *
import graph_counter


def product_name():
    original = pd.read_csv("file.csv")
    filter.full_correction(original)

    set_output("product_name_family_stats.txt")
    print_title("Correlación entre Familia y Nombre del Producto")
    name_to_family_correlation(original)
    family_to_name_correlation(original)

    reset_output()
    return


def name_to_family_correlation(df):
    df = df.groupby("Product_Name")

    print_subtitle("Familia según el Nombre")
    print_series(df["Product_Family"].value_counts())
    newline()

    print_subtitle("Máxima Cantidad de Familias por Nombre")
    max_cantidad = df["Product_Family"].nunique().max()
    printt(f"{max_cantidad}")
    newline()


def family_to_name_correlation(df):
    df = df.groupby("Product_Family")

    print_subtitle("Nombres según Familia")
    print_series(df["Product_Name"].value_counts())
    newline()

    print_subtitle("Máxima Cantidad de Nombres por Familia")
    max_cantidad = df["Product_Name"].nunique().max()
    printt(f"{max_cantidad}")
    newline()


product_name()
