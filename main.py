# Importamos las herramientas necesarias para crear la API
from fastapi import FastAPI, HTTPException  # FastAPI nos ayuda a crear una API, y HTTPException maneja errores
import pandas as pd  # Pandas nos permite trabajar con archivos de datos como CSV

# Creamos una aplicación FastAPI con un título y una versión
app = FastAPI(title="API de Radiación Solar en Colombia", version="1.0.0")

# Función para cargar los datos desde un archivo CSV
def load_data():
    try:
        # Cargamos los datos desde un archivo llamado "radiacion_solar_colombia.csv"
        df = pd.read_csv("radiacion_solar_colombia.csv")  
        
        # Eliminamos espacios innecesarios en los nombres de las columnas
        df.columns = df.columns.str.strip()  

        # Mostramos los nombres de las columnas en la consola para verificar que se cargaron correctamente
        print("Nombres de columnas en el CSV:", df.columns)  

        # Verificamos que la columna "Ciudad" exista en el archivo
        if "Ciudad" not in df.columns:
            raise Exception("No se encontró la columna 'Ciudad' en el archivo CSV.")
        
        # Convertimos el nombre de la ciudad a texto, eliminamos espacios y lo ponemos en minúsculas para evitar errores
        df["Ciudad"] = df["Ciudad"].astype(str).str.strip().str.lower()  

        # Mostramos en la consola las ciudades que aparecen en los datos
        print("Ciudades en el CSV:", df["Ciudad"].unique())  

        # Convertimos los datos en una lista de diccionarios para que sean fáciles de usar en la API
        return df.to_dict(orient="records")  

    # Si el archivo no existe, mostramos un error
    except FileNotFoundError:
        raise Exception("No se encontró el archivo 'radiacion_solar_colombia.csv'.")
    # Si ocurre otro error, mostramos un mensaje con la descripción del problema
    except Exception as e:
        raise Exception(f"Error al cargar el archivo CSV: {str(e)}")

# Llamamos a la función para cargar los datos y los guardamos en una variable llamada "data"
data = load_data()

# Definimos la ruta principal de la API
@app.get("/", tags=["Inicio"])  # Cuando alguien visite la dirección principal de la API, verá este mensaje
def home():
    return {"mensaje": "Bienvenido a la API de Radiación Solar en Colombia"}

# Ruta para obtener todos los datos
@app.get("/data", tags=["Datos"])  # Al visitar "/data", se mostrarán todos los datos disponibles
def get_all_data():
    return data

# Ruta para obtener los datos de una ciudad específica
@app.get("/data/city/{city_name}", tags=["Datos por Ciudad"])  # Aquí el usuario puede buscar por ciudad
def get_data_by_city(city_name: str):
    city_name = city_name.strip().lower()  # Limpiamos la entrada del usuario para evitar errores
    
    # Buscamos los datos de la ciudad ingresada por el usuario
    results = [row for row in data if row.get('Ciudad', '').strip().lower() == city_name]
    
    # Si encontramos datos de la ciudad, los mostramos
    if results:
        return results
    else:
        # Si la ciudad no está en los datos, mostramos un error con el código 404 (No encontrado)
        raise HTTPException(status_code=404, detail=f"No se encontraron datos para la ciudad: {city_name}")
