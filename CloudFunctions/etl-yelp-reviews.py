import functions_framework
from google.cloud import storage
from google.cloud import bigquery

import json
import pandas as pd

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
    table_name = "pivotal-racer-406214.henry_main_datasets.y-reviews"

    print(f"Event ID: {event_id}")
    print(f"Event type: {event_type}")
    print(f"Bucket: {bucket}")
    print(f"File: {name}")
    print(f"Metageneration: {metageneration}")
    print(f"Created: {timeCreated}")
    print(f"Updated: {updated}")

    full_path = 'gs://' + bucket + '/' + name
    print('va a entrar en leer')
    df_test = leer_archivo(full_path,bucket,full_path,name)
    print('salio del leer')
    print(df_test.head())

    if validar_df(df_test) == 1:
        cargar_df(project_id,table_name,df_test)
    else:
        print('No se logró validar los datos')


def leer_archivo(f_path,bucket,full_path,file_name):
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
        print('entra en json')
        try:
            print('Entra en try Json')
            # Intentar leer el archivo json como si no tuviera saltos de linea
            # df = pd.read_json(f_path)
            # df = pd.DataFrame()
            client_ = storage.Client()
            bucket_ = client_.bucket(bucket)

            # Obtener el blob (objeto) del archivo
            print('obtiene blob')
            blob = bucket_.blob(file_name)

            # Descargar el contenido del archivo
            print('descarga b lob')
            content = blob.download_as_text()

            # Analizar el contenido JSON línea por línea
            print('analiza json')
            filas_json = [json.loads(line) for line in content.splitlines()]
            
            # Crear un DataFrame a partir de la lista de filas
            print('crea df')
            df = pd.DataFrame(filas_json)

            # print('va a hacer la conver a pandas')
            # df = pd.json_normalize(json_data)

            # lines_json = [] # Iterate over each line in the JSON file
            # for line in file_content.splitlines():
            #     # Parse the JSON string into a dictionary
            #     data = json.loads(line)
            #     lines_json.append(data)

            # df = pd.DataFrame(lines_json)
            df['date'] = pd.to_datetime(df['date'])
            print('termina try json')

        except ValueError as e:
            if 'Trailing data' in str(e):
                # Leer el archivo json conteniendo saltos de linea
                df = pd.read_json(f_path, lines = True)
            else:
                # Cualquier otro error
                print('Ocurrió un error cargando el archivo JSON:', e)

        
    return df

def validar_df(df):

    # Listas a validar del df
    columns = ['review_id', 'user_id', 'business_id', 'stars','useful', 'funny', 'cool', 'text', 'date']
    type_data = ['object', 'object', 'object', 'float64','int64','int64','int64', 'object', 'datetime64[ns]']

    c=0
    # Validación de columnas
    if set(df.columns) == set(columns):
        c=1
        print("Las columnas son iguales.")
    else:
        print("Las columnas no son iguales.")

    t=0
    # Validación de tipos de datos
    tipos_de_dato_validos = all(df[col].dtype.name == tipo for col, tipo in zip(columns, type_data))
    if tipos_de_dato_validos:
        t=1
        print("Los tipos de datos son correctos.")
    else:
        print("Los tipos de datos no son correctos.")

    if c==1 & t==1:
        return 1
    else:
        return 0

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