import pandas as pd 
import numpy as np 
import glob
import json

def merge_dataframes_ETL(ruta):

    archivos_json = glob.glob(f"{ruta}/*.json")

    df_review = pd.DataFrame()

    for archivo_json in archivos_json:
        df_review = pd.concat([df_review, pd.read_json(archivo_json, lines=True)])
    
    return df_review

def associated_values_other_columns (df, columna, valores, assosiated_values):
    lista_categoria = []
    mask = df[f"{columna}"] == f"{valores}"
    lista_valores = df[mask]
    categorias = lista_valores[f"{assosiated_values}"].values
    for categoria in categorias:
        if categoria in lista_categoria:
            pass
        else:
            lista_categoria.append(categoria)
    return lista_categoria

def filer_by_values_in_column(df, columna, lista = list):
    mask = df[f"{columna}"].isin(lista)
    meta_filtrado = df[mask]
    return meta_filtrado

def null_filter_by_columns(df,column):
    mask = df[f"{column}"].notnull()
    new_df = df[mask]
    return new_df
