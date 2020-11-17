import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import seaborn as sns

import filter
from print import *
import graph_counter


def billing_country(counter):
    original = pd.read_csv("file.csv")
    filter.full_correction(original)

    original = original.drop_duplicates(subset="Opportunity_Name")

    # Codigo extraído de Lean. Regenerado con unas modificaciones
    facturacion_por_pais = original[['Billing_Country', 'ID']].groupby('Billing_Country').count().rename(columns={'ID': 'Total_Facturas'})\
        .sort_values(by=['Total_Facturas'], ascending=False)
    facturacion_por_pais = facturacion_por_pais.reset_index()

    opportunity_owner_top5(facturacion_por_pais, counter)

    return


def opportunity_owner_top5(df, counter):
    colores = ["#ff9999", "#66b3ff", "#ffcc99", "#dfa7f2", "#99ff99"]
    df.rename(
        columns={"Billing_Country": "País", "Total_Facturas": "Frecuencia"}, inplace=True)
    df.replace(
        {"United States of America": "USA"}, inplace=True)

    plt.figure(counter.get_count())

    df.head(5).plot(
        x='País', y='Frecuencia', kind='barh', color=colores, legend=None)

    plt.title('Países con más Oportunidades', pad=10)
    plt.ylabel("")
    plt.xlabel("Frecuencia")
    plt.xticks(rotation=0)
    plt.xlim(0, 3000)
    plt.tight_layout()

    for i, v in enumerate(df["Frecuencia"]):
        if i > 4:
            break
        plt.text(v + 20, i-0.05, str(v), color=colores[i], fontweight='bold')
    plt.savefig("../BySanti/graphics/billing_country.png")


counter = graph_counter.Counter()
billing_country(counter)
