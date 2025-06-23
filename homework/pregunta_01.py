import os
from datetime import datetime

import pandas as pd


def corregir_fecha(fecha: str) -> str:
    """
    Normaliza fechas con formato 'YYYY/MM/DD' o 'DD/MM/YYYY'.
    Si la primera parte tiene longitud 4, asume 'YYYY/MM/DD' y la invierte.
    """
    partes = fecha.split("/")
    p1, p2, p3 = partes
    if len(p1) == 4:
        # Convierte 'YYYY/MM/DD' a 'DD/MM/YYYY'
        return "/".join(reversed(partes))
    return fecha


def pregunta_01():
    """
    Limpia y normaliza el archivo 'solicitudes_de_credito.csv':
      - Elimina filas nulas y duplicadas.
      - Normaliza texto a minúsculas y reemplaza '_' y '-' por espacios.
      - Corrige el formato de fecha.
      - Limpia y convierte 'monto_del_credito' a float.
      - Guarda el resultado en 'files/output/solicitudes_de_credito.csv'.
    """
    # Leer datos
    df = pd.read_csv("files/input/solicitudes_de_credito.csv", sep=";")

    # Eliminar filas con NA
    df = df.dropna()

    # Campos de texto a minúsculas
    df["sexo"] = df["sexo"].str.lower()
    df["tipo_de_emprendimiento"] = df["tipo_de_emprendimiento"].str.lower()
    df["idea_negocio"] = df["idea_negocio"].str.lower()
    df["barrio"] = df["barrio"].str.lower()
    df["línea_credito"] = df["línea_credito"].str.lower()

    # Reemplazar '_' y '-' por espacio en 'idea_negocio', 'barrio' y 'línea_credito'
    for campo in ["idea_negocio", "barrio", "línea_credito"]:
        df[campo] = df[campo].str.replace("_", " ", regex=False)
        df[campo] = df[campo].str.replace("-", " ", regex=False)

    # Corregir formato de fecha
    df["fecha_de_beneficio"] = df["fecha_de_beneficio"].apply(corregir_fecha)

    # Limpiar y convertir 'monto_del_credito'
    for char in [" ", "$", ","]:
        df["monto_del_credito"] = df["monto_del_credito"].str.replace(char, "", regex=False)
    df["monto_del_credito"] = df["monto_del_credito"].astype(float)

    # Eliminar duplicados según las columnas clave y filas nulas restantes
    subset_cols = [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "estrato",
        "comuna_ciudadano",
        "fecha_de_beneficio",
        "monto_del_credito",
        "línea_credito",
    ]
    df = df.drop_duplicates(subset=subset_cols).dropna()

    # Guardar resultado
    os.makedirs("files/output", exist_ok=True)
    df.to_csv(
        "files/output/solicitudes_de_credito.csv",
        sep=";",
        index=False
    )
