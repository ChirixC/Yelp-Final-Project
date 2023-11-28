import os
from google.cloud import bigquery
from google.cloud import storage

def cargar_a_bigquery(data, context):
    # Extrae la información del evento de Cloud Storage
    bucket = data['bucket']
    file_name = data['name']

    # Configura tus valores específicos
    project_id = 'pivotal-racer-406214'
    dataset_id = 'pivotal-racer-406214.prueba_pablo'
    table_id = 'prueba_json'

    # Inicializa el cliente de BigQuery y Cloud Storage
    bq_client = bigquery.Client(project=project_id)
    gcs_client = storage.Client(project=project_id)

    # Define la ubicación del archivo en Cloud Storage
    gcs_uri = f'gs://{bucket}/{file_name}'

    # Configura la referencia a la tabla de BigQuery
    table_ref = bq_client.dataset(dataset_id).table(table_id)

    # Configura las opciones de carga
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,  # Ajusta según el formato de tu archivo
        skip_leading_rows=1,  # Si hay encabezados en el archivo, ajusta esta opción
        autodetect=True,  # Deja que BigQuery detecte automáticamente el esquema
    )

    # Inicia el trabajo de carga
    load_job = bq_client.load_table_from_uri(
        gcs_uri, table_ref, job_config=job_config
    )

    # Espera a que el trabajo de carga se complete
    load_job.result()

    print(f'Carga completada en la tabla {project_id}.{dataset_id}.{table_id}')

# Nota: En Google Cloud Functions, la autenticación se maneja automáticamente si el servicio tiene los permisos adecuados.
