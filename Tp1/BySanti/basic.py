import pandas as pd
import matplotlib.pyplot as plt

import filter
from format import *

original = pd.read_csv("file.csv")

filas = len(original.index)
columnas = len(original.columns)

print_title("Estadística Básica")

printt(f"Cantidad de datos: {original.size}")
printt(f"Cantidad de filas: {original.shape[0]}")
printt(f"Cantidad de columnas: {original.shape[1]}")

print_title("Completitud del Set")

for col in original:
    cant = original[col].isnull().value_counts().tolist()
    if cant[0] == filas: continue

    nulos = cant[1]
    porcentaje = cant[1] /filas
    
    printt(f"{col}: {pretty_f(porcentaje, 3)}% - {nulos}/{filas}")

print(original["Sales_Contract_No"].isnull().value_counts())
filter.full_correction(original)
print(original.dtypes)
print(original.shape[0])

