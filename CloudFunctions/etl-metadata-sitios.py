import functions_framework
import pandas as pd
from google.cloud import storage
from google.cloud import bigquery
import json

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
    
    table_name = "pivotal-racer-406214.henry_main_datasets.metadata-sitios"

    print(f"Event ID: {event_id}")
    print(f"Event type: {event_type}")
    print(f"Bucket: {bucket}")
    print(f"File: {name}")
    print(f"Metageneration: {metageneration}")
    print(f"Created: {timeCreated}")
    print(f"Updated: {updated}")

    full_path = 'gs://' + bucket + '/' + name
    df_test = leer_archivo(full_path)

    # Funcion para que la DF solo tenga los restaurants
    df_test = extract_restaurants(df_test)

    if df_test is not None:
        print(df_test)
        #df_clean = transformar_df(df_test)
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
        # Si es JSON, leer el archivo desde Google Cloud Storage
        if f_type == 'json':
            # Extraer el bucket y el nombre del archivo desde la ruta de Google Cloud Storage
            bucket_name, file_name = f_path.replace('gs://', '').split('/', 1)

            # Obtener el bucket
            bucket = storage_client.bucket(bucket_name)
            lista_dataframes = []

            for blob in bucket.list_blobs():
                # blob = bucket.blob(file_name)
                content = blob.download_as_text()

                rows_json = []
                for line in content.splitlines():
                    row = json.loads(line)

                    # Elimina las columnas no deseadas
                    for key in ['address', 'description', 'MISC', 'relative_results', 'hours', 'price', 'url', 'state']:
                        row.pop(key, None)

                    if "category" in row and isinstance(row["category"], list):
                        row["category"] = ", ".join(row["category"])
                    rows_json.append(row)

                # Se va a crear la lista de los que se van a concatenar
                df_temp = pd.DataFrame(rows_json)
                lista_dataframes.append(df_temp)

            df = pd.concat(lista_dataframes, axis=0, ignore_index=True)

        # Si es CSV, Parquet, Pickle, etc., utilizar las funciones existentes
        elif f_type in ['csv', 'parquet', 'pkl']:
            df = pd.read_parquet(f_path) if f_type == 'parquet' else pd.read_csv(f_path)

        else:
            raise ValueError(f"Tipo de archivo no compatible: {f_type}")

        return df

    except Exception as e:
        print(f'Ocurrió un error cargando el archivo: {e}')
        return None

def validar_df(df):

    # Listas a validar del df
    columns = ['name', 'gmap_id', 'latitude', 'longitude','category', 'avg_rating','num_of_reviews']
    type_data = ['object', 'object', 'float64','float64', 'object','float64', 'int64']

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
        autodetect=True
    )

    try:
        print('Entra try')
        # Load the dataframe to the destination table using the load job
        job = bq_client.load_table_from_dataframe(df, table_name, job_config=job_config)

        print('Espera por Job')
        # Wait for the job to complete
        job.result()

        print('Cargo Archivo')
        # Print the result
        print(f"Loaded {job.output_rows} rows to {table_name}")

    except Exception as e:
        print("Entra Exeption")
        print(f"An error occurred: {e}")

#def transformar_df(df_entrada):

    #df_sitios = df_entrada.drop(columns=['address', 'description', 'MISC', 'relative_results', 'hours', 'price', 'url', 'state'])
    #df_sitios = df_entrada.explode('category')
    #df_sitios = df_sitios.dropna(subset=['category'])

    #return df_sitios

def extract_restaurants(df):

    print("Entra en extract")
    storage_client = storage.Client()
    bucket = storage_client.get_bucket("henry-fp-data")
    blob = bucket.blob("ml-data/restaurant_categories.txt")

    file_content = blob.download_as_text()

    file_list = file_content.split("\n")

    file_list = [item.rstrip() for item in file_list]

    df.dropna(axis=0, subset=['category'], inplace=True)

    df['categories_set'] = df['category'].str.split(', ').apply(set)

    df['match'] = df['categories_set'].apply(lambda x: any(c in x for c in file_list))

    df_filtered = df[df['match']]

    df_filtered = df_filtered.drop(['categories_set', 'match'], axis=1)

    
    print(f"Salió de extract" )
    
    return df_filtered