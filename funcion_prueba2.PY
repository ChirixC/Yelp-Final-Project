import functions_framework
import pandas as pd
from google.cloud import storage
import json

# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def hello_gcs(cloud_event):
    data = cloud_event.data

    event_id = cloud_event["id"]
    event_type = cloud_event["type"]

    bucket = data["bucket"]
    name = data["name"]
    metageneration = data["metageneration"]
    timeCreated = data["timeCreated"]
    updated = data["updated"]

    project_id = 'pivotal-racer-406214'

    dataset = "pivotal-racer-406214.prueba_pablo"
    
    table_name = "pivotal-racer-406214.prueba_pablo.tips"


    print(f"Event ID: {event_id}")
    print(f"Event type: {event_type}")
    print(f"Bucket: {bucket}")
    print(f"File: {name}")
    print(f"Metageneration: {metageneration}")
    print(f"Created: {timeCreated}")
    print(f"Updated: {updated}")

    
    full_path = 'gs://' + bucket + '/' + name
    df_test = leer_archivo(full_path)
    print(df_test)
    cargar_df(project_id,table_name,table_name,df_test)

def leer_archivo(f_path):
    """
    Lee el archivo según su extensión. Disparado por la funcion "captura_evento"
    Args:
        event (dict): Event payload.
        file_path (str): ruta del archivo
        file_type (str): tipo del archivo
    """
    # Extraer el tipo de archivo
    f_type = f_path.split('.')[-1]
    
    # Revisando si archivo es csv
    #if f_type == 'csv':
        # Leyendo archivo en dataframe
        #df = pd.read_csv(f_path)

    # Revisando si archivo es json    
    if f_type == 'json':
        try:
            # Intentar leer el archivo json como si no tuviera saltos de linea
            df = pd.read_json(f_path)
        except ValueError as e:
            if 'Trailing data' in str(e):
                # Leer el archivo json conteniendo saltos de linea
                df = pd.read_json(f_path, lines = True)
            else:
                # Cualquier otro error
                print('Ocurrió un error cargando el archivo JSON:', e)

    # Revisar si el archivo es tipo parquet
    #elif f_type == 'parquet':
        # Leyendo archivo en dataframe
        #df = pd.read_parquet(f_path)

    # Revisar si el archivo es tipo pkl (Pickle)
    #elif f_type == 'pkl':
        #try:
            # Leyendo archivo en DataFrame desde Google Cloud Storage
            #df = pd.read_pickle(f_path)
        #except Exception as e:
            #print(f'Ocurrió un error al leer el archivo Pickle: {e}')
    
    return df

def cargar_df(project, dataset, table, df):
    try:
        # convierte todo el dataset a str para almacenar
        df = df.astype(str)
        
        # guarda el dataset en una ruta predefinida y si la tabla ya está creada la reemplaza
        df.to_gbq(destination_table = dataset, 
                    project_id = project,
                    table_schema = None,
                    if_exists = 'replace',
                    progress_bar = False, 
                    auth_local_webserver = False, 
                    location = 'us')
            
    except Exception as e:
        print(f"An error occurred: {e}")