import functions_framework
import pandas as pd
from google.cloud import bigquery
from geopy.geocoders import Nominatim
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

    dataset = "pivotal-racer-406214.henry_main_datasets"
    
    table_name = "pivotal-racer-406214.henry_main_datasets.y-business"


    print(f"Event ID: {event_id}")
    print(f"Event type: {event_type}")
    print(f"Bucket: {bucket}")
    print(f"File: {name}")
    print(f"Metageneration: {metageneration}")
    print(f"Created: {timeCreated}")
    print(f"Updated: {updated}")
    
    full_path = 'gs://' + bucket + '/' + name
    df_test = leer_archivo(full_path)
    print(df_test.head())    
    df_transformado = transformar_df(df_test)

    # Agrega la nueva columna 'state_names' utilizando la función corregir_desconocidos
    df_transformado['state_names'] = df_transformado.apply(corregir_desconocidos, axis=1)

    cargar_df(project_id,table_name,df_transformado)    
    

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

    return df

# def validar_df(df):

#     # Listas a validar del df
#     columns = ['business_id', 'name','city', 'latitude', 'longitude','stars','review_count','categories','state_names']
#     type_data = ['object', 'object', 'object', 'float', 'float','float','int64','object','object']

#     c=0
#     # Validación de columnas
#     if set(df.columns) == set(columns):
#         c=1
#         print("Las columnas son iguales.")
#     else:
#         print("Las columnas no son iguales.")

#     t=0
#     # Validación de tipos de datos
#     tipos_de_dato_validos = all(df[col].dtype.name == tipo for col, tipo in zip(columns, type_data))
#     if tipos_de_dato_validos:
#         t=1
#         print("Los tipos de datos son correctos.")
#     else:
#         print("Los tipos de datos no son correctos.")

#     if c==1 & t==1:
#         return 1
#     else:
#         return 0

def cargar_df(project_id, table_name, df):

    print('Declara cliente')
    # Declare a BigQuery Client
    bq_client = bigquery.Client(project=project_id)

    print('Declara Job')
    # Configure the Job parameters
    job_config = bigquery.LoadJobConfig( 
    write_disposition='WRITE_TRUNCATE', 
    create_disposition='CREATE_IF_NEEDED', 
    encoding=bigquery.Encoding.UTF_8, 
    autodetect=True)

    try:
        print('Entra try')
        # Load the dataframe to the destination table using the load job
        job = bq_client.load_table_from_dataframe(df, table_name, job_config=job_config)

        print('Espera por Job')
        # Wait for the job to complete
        job.result()

        print('Cargo Archivo')
        #Print the result
        print(f"Loaded {job.output_rows} rows to {table_name}")
            
    except Exception as e:
        print("Entra Exeption")
        print(f"An error occurred: {e}")

def transformar_df(df_entrada):

    df_clean = df_entrada.drop(columns=['address', 'state', 'state_complete'])   
    return df_clean

def corregir_desconocidos(row):
    if row['state_names'] == 'Desconocido':
        latitud = row['latitude']
        longitud = row['longitude']
        estado = obtener_estado_desde_lat_long(latitud, longitud)
        return estado if estado else 'Desconocido'
    else:
        return row['state_names']

def obtener_estado_desde_lat_long(latitud, longitud):
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.reverse((latitud, longitud), language='en')
    
    if location:
        address = location.raw.get('address', {})
        state_name = address.get('state', 'Desconocido')
        return state_name
    else:
        return 'Desconocido'