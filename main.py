from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from typing import List
import csv
import pandas as pd
import numpy as np
# Cargar los datos desde el archivo CSV

df = pd.read_csv('conteo_peliculas_por_idioma.csv', encoding='utf-8')
df1 = pd.read_csv('duracion_peliculas.csv', encoding='utf-8')
df2 = pd.read_csv('franquicia.csv', encoding='utf-8')
df3 = pd.read_csv('conteo_paises.csv', encoding='utf-8')
df4 = pd.read_csv('moviesclean.csv', encoding='utf-8')
df5 = pd.read_csv('dir_pel.csv', encoding='utf-8')
# Convertir los datos a un diccionario para acceder fácilmente a ellos

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/peliculas_idioma/{idioma}")
def peliculas_idioma(idioma: str):
    resultado = df.loc[df['idioma'] == idioma, 'cantidad_peliculas']
    if len(resultado) > 0:
        cantidad_peliculas = resultado.values[0]
        cantidad_peliculas = int(cantidad_peliculas)  # Convertir a entero nativo de Python
        return {f"{cantidad_peliculas} películas fueron estrenadas en el idioma {idioma}"}
    else:
        return {f"No se encontraron películas en el idioma {idioma}"}

@app.get("/peliculas_duracion/{title}")
def obtener_pelicula(title: str):
    resultado = df1.loc[df1['title'] == title]
    if not resultado.empty:
        titulo = resultado['title'].values[0]
        duracion = resultado['runtime'].values[0]
        year = resultado['release_year'].values[0]
        return {"titulo": titulo, "Duracion": duracion, "Año": year}
    else:
        return {f"No se encontró la película con el título '{title}'"}

@app.get("/franquicia/{belongs_to_collection_name}")
def obtener_datos_franquicia(belongs_to_collection_name: str):
    resultado = df2.loc[df2['belongs_to_collection_name'] == belongs_to_collection_name]
    if not resultado.empty:
        peliculas = resultado['peliculas'].values[0]
        ganancia_total = resultado['revenue'].sum()
        ganancia_promedio = resultado['promedio'].values[0]
        return {f"La franquicia {belongs_to_collection_name} posee {peliculas} peliculas, una ganancia total de {ganancia_total} y una ganancia promedio de {ganancia_promedio}"}
    else:
        return {f"No se encontró la franquicia '{belongs_to_collection_name}'"}

@app.get("/peliculas_pais/{countries}")
def obtener_cantidad_peliculas_pais(countries: str):
    resultado = df3.loc[df3['countries'] == countries]
    if not resultado.empty:
        peliculas = resultado['peliculas'].values[0]
        return {f"Se produjeron {peliculas} películas en el país {countries}"
        }
    else:
        return {f"No se encontraron películas producidas en el país {countries}"}

@app.get("/productoras_exitosas/{Productora}")
def obtener_datos_productora(Productora: str):
    mask = df4['companies'].str.contains(Productora, case=False) & df4['companies'].notna()
    resultado = df4[mask]
    if not resultado.empty:
        revenue_total = resultado['revenue'].sum()
        peliculas = resultado.shape[0]
        return {
            f"La productora {Productora} ha tenido un revenue de {revenue_total} y ha realizado {peliculas} películas"
        }
    else:
        return {f"No se encontró la productora {Productora}"}

@app.get("/get_director/{director}")
def obtener_datos_director(director: str):
    resultado = df5.loc[df5['director'] == director]
    if not resultado.empty:
        datos_peliculas = []
        for index, row in resultado.iterrows():
            pelicula = {
                "title": row['title'],
                "year": str(row['year']),
                "return": str(row['return']),
                "budget": str(row['budget']),
                "revenue": str(row['revenue'])
            }
            datos_peliculas.append(pelicula)
        return datos_peliculas
    else:
        return {"mensaje": f"No se encontraron películas del director {director}"}


