import functions_framework
from google.cloud import bigquery
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

@functions_framework.http
def load_df(request):

    client = bigquery.Client(project='pivotal-racer-406214')

    query_google_restaurants = client.query("SELECT * FROM `pivotal-racer-406214.henry_main_datasets.google-steakhouses-final`")    
    df_google = query_google_restaurants.result().to_dataframe() 

    #Preparación para K-Means (ya habiendo elegido valor de K en el EDA)
    df_model = df_google[['gmap_id','name','avg_rating','state','sentiment_label','latitude','longitude','num_of_reviews']]
   
    # Crear un nuevo DataFrame con gmap_id únicos
    df_unique = df_model.drop_duplicates(subset='gmap_id')

    # Filtrar solo las reviews positivas
    df_positive_reviews = df_model[df_model['sentiment_label'] == 'positivo']

    # Contar el número de reviews positivas por gmap_id
    positive_reviews_count = df_positive_reviews.groupby('gmap_id')['sentiment_label'].count().reset_index()
    positive_reviews_count.columns = ['gmap_id', 'positive_reviews_count']

    # Fusionar los DataFrames para agregar la columna de conteo de reviews positivas
    df_result = pd.merge(df_unique, positive_reviews_count, on='gmap_id', how='left')

    # Rellenar NaN con 0, ya que algunos lugares pueden no tener reviews positivas
    df_result['positive_reviews_count'] = df_result['positive_reviews_count'].fillna(0).astype(int)

    # Escala las columnas relevantes del nuevo DataFrame df_result
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_result[['positive_reviews_count', 'avg_rating', 'latitude', 'longitude']])

    # K-Means clustering con K=5
    num_clusters = 5
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    df_result['cluster'] = kmeans.fit_predict(X_scaled)

    project_id = 'pivotal-racer-406214'
    
    table_locations = 'pivotal-racer-406214.henry_main_datasets.google-new-locations'
    
    cargar_df(project_id, table_locations, df_result)

    print('Finalizo')

    return 'Cargamos la Dataframe'

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
        print(df)
        print(table_name)
        
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