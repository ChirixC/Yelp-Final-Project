import functions_framework
import pandas as pd
from google.cloud import storage
from google.cloud import bigquery


# Triggered by a change in a storage bucket
@functions_framework.cloud_event
def evento_activacion(cloud_event):
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
    
    table_name = "pivotal-racer-406214.henry_main_datasets.yah-finance"


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
    if validar_df(df_test) == 1:
        cargar_df(project_id,table_name,df_test)
    else:
        print('No se logró validar los datos')

def leer_archivo(f_path):
    """
    Lee el archivo según su extensión. Disparado por la funcion "captura_evento"
    Args:
        f_path (str): Ruta del archivo en formato 'gs://bucket_name/file_name'.
    """
    # Extraer el tipo de archivo
    f_type = f_path.split('.')[-1]

    # Inicializar el cliente de Storage
    storage_client = storage.Client()

    try:              
      
        # Si es CSV, Parquet, Pickle, etc., utilizar las funciones existentes
        if f_type in ['csv', 'parquet', 'pkl']:
            df = pd.read_parquet(f_path) if f_type == 'parquet' else pd.read_csv(f_path)
        else:
            raise ValueError(f"Tipo de archivo no compatible: {f_type}")
        return df

    except Exception as e:
        print(f'Ocurrió un error cargando el archivo: {e}')
        return None

    except Exception as e:
        print(f'Ocurrió un error cargando el archivo: {e}')
        return None

def validar_df(df):

    # Listas a validar del df
    columns = ['GSPC', 'NDX', 'TXRH','DRI','BLMN']
    type_data = ['float64', 'float64', 'float64', 'float64', 'float64']

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






                
