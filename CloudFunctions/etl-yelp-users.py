import functions_framework
import pandas as pd
from google.cloud import bigquery
import pyarrow.parquet as pq
import numpy as np

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
    table_name = "pivotal-racer-406214.henry_main_datasets.y-user"

    print(f"Event ID: {event_id}")
    print(f"Event type: {event_type}")
    print(f"Bucket: {bucket}")
    print(f"File: {name}")
    print(f"Metageneration: {metageneration}")
    print(f"Created: {timeCreated}")
    print(f"Updated: {updated}")

    full_path = 'gs://' + bucket + '/' + name
    df_test = leer_archivo(full_path,project_id,table_name)
    print(df_test)
    print('va a entrar transformado')
    df_transformado = transformar_df(df_test)
    print('va a entrar cargar')
    if validar_df(df_transformado) == 1:
        cargar_df(project_id,table_name,df_test)
    else:
        print('No se logró validar los datos')


def leer_archivo(f_path,project_id,table_name):
    """
    Lee el archivo según su extensión. Disparado por la funcion "captura_evento"
    Args:
        event (dict): Event payload.
        file_path (str): ruta del archivo
        file_type (str): tipo del archivo
    """
    # Extraer el tipo de archivo
    f_type = f_path.split('.')[-1]

    print(f_type)

    # Revisar si el archivo es tipo parquet
    if f_type == 'parquet':

        parquet_file = pq.ParquetFile(f_path)

        dataframes = []

        print('Entrando en el for:')
        for batch in parquet_file.iter_batches(batch_size=20000):
            dataframe_batch = batch.to_pandas()
            dataframes.append(dataframe_batch)

        df = pd.concat(dataframes, ignore_index=True)

    return df

def transformar_df(df):
    columns_to_save = ['user_id', 'name', 'review_count', 'useful', 'friends', 'fans', 'average_stars']
    df = df.loc[:, columns_to_save]

    # Eliminar duplicados
    df = df.drop_duplicates()
    return df

def validar_df(df):

    # Listas a validar del df
    columns = ['user_id', 'name','review_count','useful', 'friends','fans', 'average_stars']
    type_data = ['object', 'object','int64','int64', 'object','int64', 'float64']

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

    print('Declara Job1')
    # Configure the Job parameters
    job_config1 = bigquery.LoadJobConfig( 
    write_disposition='WRITE_TRUNCATE', 
    create_disposition='CREATE_IF_NEEDED', 
    encoding=bigquery.Encoding.UTF_8, 
    autodetect=True)

    print('Declara Job2')
    # Configure the Job parameters
    job_config2 = bigquery.LoadJobConfig( 
    write_disposition='WRITE_APPEND', 
    create_disposition='CREATE_IF_NEEDED', 
    encoding=bigquery.Encoding.UTF_8, 
    autodetect=True)

    try:
        print('Entra try')

        print('Divide')
        chunks = np.array_split(df,4)

        # Load the dataframe to the destination table using the load job
        print('sube job 1')
        job1 = bq_client.load_table_from_dataframe(chunks[0], table_name, job_config=job_config1)
        job1.result()
        print(f"Loaded {job1.output_rows} rows to {table_name}")

        print('sube job 2')
        job2 = bq_client.load_table_from_dataframe(chunks[1], table_name, job_config=job_config2)
        job2.result()
        print(f"Loaded {job2.output_rows} rows to {table_name}")

        print('sube job 3')
        job3 = bq_client.load_table_from_dataframe(chunks[2], table_name, job_config=job_config2)
        job3.result()
        print(f"Loaded {job3.output_rows} rows to {table_name}")

        print('sube job 4')
        job4 = bq_client.load_table_from_dataframe(chunks[3], table_name, job_config=job_config2)
        job4.result()
        print(f"Loaded {job4.output_rows} rows to {table_name}")

        print('Espera por Job')
        # Wait for the job to complete
        # job1.result()

        print('Cargo Archivo')
        #Print the result
        # print(f"Loaded {job1.output_rows} rows to {table_name}")
            
    except Exception as e:
        print("Entra Exeption")
        print(f"An error occurred: {e}")