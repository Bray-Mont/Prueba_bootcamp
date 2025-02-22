import pandas as pd
from fastapi.responses import JSONResponse  # Importamos la clase JSONResponse
from fastapi import FastAPI, HTTPException, Query  # Importamos la clase FastAPI y HTTPException     
               


def cargar_dataset():
    try:
        # Cargar el archivo CSV
        df = pd.read_csv("radiacion_solar_colombia.csv", delimiter=";", quotechar='"', on_bad_lines="skip")

        # Mostrar nombres de las columnas para verificar
        print("Columnas del archivo CSV:", df.columns)

        # Verificar si todas las columnas existen
        columnas_deseadas = [
            'Departamento', 'Ciudad', 'Latitud', 'Longitud', 'Altitud (m)',
            'Fecha y Hora', 'Radiación Solar (W/m²)', 'Temperatura (°C)',
            'Humedad (%)', 'Velocidad del Viento (m/s)', 'Cobertura Nubosa (%)',
            'Viabilidad Energética (%)'
        ]
        columnas_existentes = [col for col in columnas_deseadas if col in df.columns]

        if not columnas_existentes:
            raise ValueError("Ninguna de las columnas requeridas está en el archivo CSV.")

        # Filtrar solo las columnas existentes
        df = df[columnas_existentes]

        # Rellenar valores nulos con una cadena vacía
        return df.fillna('').to_dict(orient="records")
    
    except Exception as e:
        print("Error al cargar el dataset:", e)
        return []

# Cargar y mostrar los primeros 5 registros
dataset = cargar_dataset()
print(dataset[:5])

