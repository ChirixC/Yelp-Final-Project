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

    dataset = "pivotal-racer-406214.carlos_prueba"
    
    table_name = "pivotal-racer-406214.carlos_prueba.tabla_demo"


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

        # Si es CSV, Parquet, Pickle, etc., utilizar las funciones existentes
        #elif f_type in ['csv', 'parquet', 'pkl']:
        #    df = pd.read_parquet(f_path) if f_type == 'parquet' else pd.read_csv(f_path)

        #else:
        #    raise ValueError(f"Tipo de archivo no compatible: {f_type}")

        return df

    except Exception as e:
        print(f'Ocurrió un error cargando el archivo: {e}')
        return None

    except Exception as e:
        print(f'Ocurrió un error cargando el archivo: {e}')
        return None


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

        
 ###############################################################################3       
        
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
                print(blob)   ### cada blob es un archivo

                # Obtener el blob (objeto) del archivo
                blob = bucket.blob(file_name)

                # Descargar el contenido del archivo
                content = blob.download_as_text()

                # Analizar el contenido JSON línea por línea
                filas_json = [json.loads(line) for line in content.splitlines()]
                
                # Se va a crear la lista de los que se van a concatenar
                df_temp = pd.DataFrame(filas_json)
                lista_dataframes.append(df_temp)

            # Crear un DataFrame a partir de la lista de dataframes
            df = pd.concat(lista_dataframes, ignore_index=True)

        # Si es CSV, Parquet, Pickle, etc., utilizar las funciones existentes
        elif f_type in ['csv', 'parquet', 'pkl']:
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