import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import seaborn as sns

import filter
from print import *
import graph_counter


def brand():
    original = pd.read_csv("file.csv")
    filter.full_correction(original)
    set_output("brand_stats.txt")

    print_title("Estadísticas de la Marca")
    brand_basic_prestats(original)

    original = original.drop_duplicates(subset="Opportunity_Name")

    brand_basic_stats(original)
    brand_success(original)
    brand_to_product_type_correlation(original)
    product_type_to_brand_correlation(original)

    reset_output()
    return


def brand_basic_prestats(df):
    print_subtitle("Registros con Marca")
    cant_registros = df["Brand"].count()
    printt(f"{cant_registros}")
    newline()


def brand_basic_stats(df):
    print_subtitle("Oportunidades con Marca")
    cant_oport = df["Brand"].count()
    printt(f"{cant_oport}")
    newline()

    print_subtitle("Cantidad de Marcas Distintas")
    cant_marcas = len(df["Brand"].unique())
    printt(f"{cant_marcas}")
    newline()

    print_subtitle("Cantidad de Oportunidades por Marca")
    print_series(df["Brand"].value_counts())
    newline()


def brand_success(df):
    df = df.groupby("Brand")

    print_subtitle("Éxito según la Marca")
    print_series(df["Stage"].value_counts())
    newline()


def product_type_to_brand_correlation(df):
    df = df.groupby("Product_Type")

    # Convertir -1 a other
    print_subtitle("Marcas según Tipo de Producto")
    print_series(df["Brand"].value_counts())
    newline()

    print_subtitle("Máxima Cantidad de Marcas por Tipo de Producto")
    max_cantidad = df["Brand"].nunique().max()
    printt(f"{max_cantidad}")
    newline()


def brand_to_product_type_correlation(df):
    df = df.groupby("Brand")

    print_subtitle("Tipos de Producto según Marcas")
    print_series(df["Product_Type"].value_counts())
    newline()

    print_subtitle("Máxima Cantidad de Tipos de Producto por Marca")
    max_cantidad = df["Product_Type"].nunique().max()
    printt(f"{max_cantidad}")
    newline()


brand()
