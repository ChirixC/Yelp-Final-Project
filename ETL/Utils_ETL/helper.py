import pandas as pd 
import numpy as np 
import glob

def merge_dataframes_ETL(ruta):

    archivos_json = glob.glob(f"{ruta}/*.json")

    df_review = pd.DataFrame()

    for archivo_json in archivos_json:
        df_review = pd.concat([df_review, pd.read_json(archivo_json, lines=True)])
    
    return df_review