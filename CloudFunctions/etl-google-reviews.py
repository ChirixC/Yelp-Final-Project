import functions_framework
import pandas as pd
import json
from google.cloud import storage
from google.cloud import bigquery
from textblob import TextBlob

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

    file_path = 'gs://' + bucket + '/' + name

    # Extract the folder name from the file path
    folder_name = file_path.split("/")[-2]
    state = folder_name.split('-')[-1]

    project_id = 'pivotal-racer-406214'

    dataset = "pivotal-racer-406214.henry_main_datasets"

    table_name = f"pivotal-racer-406214.henry_main_datasets.google-reviews-{state}"

    # Initialize the Storage client
    storage_client = storage.Client()

    # Get the bucket
    bucket = storage_client.bucket(bucket)

    # Filter the list of blobs based on the folder name
    blobs = [blob for blob in bucket.list_blobs() if blob.name.startswith(folder_name)]

    # Initialize an empty list to store the dataframes
    dataframes = []

    # Read and merge dataframes from the filtered blobs
    for blob in blobs:
        df_temp = leer_archivo(blob,bucket)
        print(df_temp.head())
        dataframes.append(df_temp)

    # Concatenate the dataframes
    df = pd.concat(dataframes, ignore_index=True)

    # Transform the dataframe
    df_transformado = transformar_df(df,folder_name)

    print(df_transformado.info())

    if validar_df(df_transformado) == 1:
        cargar_df(project_id,table_name,df_transformado)
    else:
        print('No se logró validar los datos')

    print(f"Event ID: {event_id}")
    print(f"Event type: {event_type}")
    print(f"Bucket: {bucket}")
    print(f"File: {name}")
    print(f"Metageneration: {metageneration}")
    print(f"Created: {timeCreated}")
    print(f"Updated: {updated}")

# Función para leer el archivo JSON
def leer_archivo(blob, bucket):
    # Extraer el tipo de archivo
    f_type = blob.name.split('.')[-1]

    # Inicializar el cliente de Storage
    storage_client = storage.Client()

    try:
        # Si es JSON, leer el archivo desde Google Cloud Storage
        if f_type == 'json':

            # Descargar el contenido del archivo
            content = blob.download_as_text()

            # Analizar el contenido JSON línea por línea
            filas_json = [json.loads(line) for line in content.splitlines()]

            # Crear un DataFrame a partir de las filas JSON
            df = pd.DataFrame(filas_json)

        else:
            raise ValueError(f"Tipo de archivo no compatible: {f_type}")

        return df

    except Exception as e:
        print(f'Ocurrió un error cargando el archivo: {e}')
        return None
    
def transformar_df(df_test,folder):

    state = folder.split('-')[-1]
    state = state.replace('_', ' ')

    df_test['state'] = state
    df_test.fillna("Sin Datos", inplace=True)
    df_mask = df_test[['user_id', 'name', 'time', 'rating', 'text', 'gmap_id','state']]
    df_mask.drop_duplicates(inplace=True)
    df_mask['time'] = pd.to_datetime(df_test['time'], unit='ms')

    return df_mask

def validar_df(df):

    # Listas a validar del df
    columns = ['user_id', 'name', 'time', 'rating','text','gmap_id', 'state']
    type_data = ['object', 'object', 'datetime64[ns]', 'int64','object','object', 'object']

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