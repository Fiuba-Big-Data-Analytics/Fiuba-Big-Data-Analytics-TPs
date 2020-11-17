import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import seaborn as sns

import filter
from print import *
import graph_counter


def opportunity_id(counter):
    original = pd.read_csv("file.csv")
    filter.full_correction(original)

    set_output("opportunity_id.txt")

    opportunity_id_stats(original)

    reset_output()


def opportunity_id_stats(df):
    print_title("Estadística de los ID de las Oportunidades")

    filas = len(df.index)
    valores_unicos = len(df["Opportunity_ID"].unique())

    print_subtitle("Cantidad de ID distintos")
    printt(f"{valores_unicos}")
    newline()

    print_subtitle("Cantidad Promedio de Registros por ID")
    printt(f"{filas / valores_unicos}")
    newline()

    print_subtitle("ID Mínimo")
    min_id = df["Opportunity_ID"].min()
    printt(f"{min_id}")
    newline()

    print_subtitle("ID Máximo")
    max_id = df["Opportunity_ID"].max()
    printt(f"{max_id}")
    newline()

    print_subtitle("Nombre Mínimo")
    min_name = df["Opportunity_Name"].min()
    printt(f"{min_name}")
    newline()

    print_subtitle("Nombre Máximo")
    max_name = df["Opportunity_Name"].max()
    printt(f"{max_name}")
    newline()

    print_subtitle("Cantidad Máxima de Registros Para Oportunidad")
    df["Opportunity_Register_Count"] = df.groupby(
        "Opportunity_ID")["ID"].transform("count")
    max_reg = df["Opportunity_Register_Count"].max()
    printt(f"{max_reg}")
    newline()

    print_subtitle("Cantidad Máxima de Contratos por Oportunidad")

    max_contracts = df.groupby("Opportunity_ID")[
        "Sales_Contract_No"].nunique().max()
    printt(f"{max_contracts}")
    newline()

    print_subtitle("Cantidad Máxima de Oportunidades por Contrato")

    max_oppor = df.groupby("Sales_Contract_No")[
        "Opportunity_ID"].nunique().max()
    printt(f"{max_oppor}")
    newline()

    print_subtitle("Máximo Valor de Sales Contract Number")
    max_contract = df["Sales_Contract_No"].max()
    printt(f"{max_contract}")
    newline()

    print_subtitle("Mínimo Valor de Sales Contract Number")
    min_contract = df["Sales_Contract_No"].min()
    printt(f"{min_contract}")
    newline()

    print_subtitle("Números de Contrato Diferentes")
    diff_contract = df["Sales_Contract_No"].nunique()
    printt(f"{diff_contract}")
    newline()


counter = graph_counter.Counter()
opportunity_id(counter)
