import functions_framework
from google.cloud import bigquery
import pandas as pd
from nltk.corpus import stopwords
import nltk
from textblob import TextBlob

@functions_framework.http
def load_df(request):

    client = bigquery.Client(project='pivotal-racer-406214')

    query_job_positive = client.query("SELECT * FROM `henry_main_datasets.google-steakhouses-final` WHERE name = 'Texas Roadhouse' AND sentiment_label = 'positivo'")
    query_job_negative = client.query("SELECT * FROM `henry_main_datasets.google-steakhouses-final` WHERE name = 'Texas Roadhouse' AND sentiment_label = 'negativo'")

    df_positive = query_job_positive.result().to_dataframe()
    df_negative = query_job_negative.result().to_dataframe()

    project_id = 'pivotal-racer-406214'

    table_name_positive = 'pivotal-racer-406214.henry_main_datasets.importance-words-positive'
    table_name_negative = 'pivotal-racer-406214.henry_main_datasets.importance-words-negative'

    
    df_extracted_positive = extract_importance(df_positive,'positive')
    df_extracted_negative = extract_importance(df_negative,'negative')

    df_extracted_negative['count'] = df_extracted_negative['count'] *5
    df_extracted_negative = df_extracted_negative[df_extracted_negative['score'] < -0.2]

    cargar_df(project_id, table_name_positive, df_extracted_positive)
    cargar_df(project_id, table_name_negative, df_extracted_negative)

    print('Finalizo')

    return 'Cargamos la Dataframe'


def extract_importance(df_reviews, sentiment):

    print('Entra extract')
    nltk.download('stopwords')
    nltk.download('punkt')

    words_scores = []

    # Definir un conjunto de palabras vacías
    stopwords = set(nltk.corpus.stopwords.words('english'))

    print('Va para el for')
    for index, row in df_reviews.iterrows():
        # Obtener la reseña de la columna 'reviews'
        review = row['text']
        # Crear un objeto TextBlob a partir de la reseña
        blob = TextBlob(review)
        # Recorrer cada palabra de la reseña
        for word in blob.words:
            # Convertir la palabra a minúsculas
            word = word.lower()
            # Si la palabra no es una palabra vacía
            if word not in stopwords:
                # Crear un objeto TextBlob a partir de la palabra
                word_blob = TextBlob(word)
                # Obtener el score de sentimiento de la palabra
                score = word_blob.sentiment.polarity
                # Añadir la palabra y su score a la lista
                words_scores.append((word, score))

    print('Salio del for')
    # Crear una dataframe a partir de la lista de palabras y scores
    df_words = pd.DataFrame(words_scores, columns=['word', 'score'])

    # Agrupar la dataframe por palabra y calcular la media de los scores
    df_words = df_words.groupby('word').mean()

    if sentiment == 'positive':
        # Ordenar la dataframe por score de forma descendente
        df_words = df_words.sort_values(by='score', ascending=False)
    else:
        # Ordenar la dataframe por score de forma descendente
        df_words = df_words.sort_values(by='score', ascending=True)

    # Agregar una columna con el conteo de cada palabra en las reseñas
    df_words['count'] = df_words.index.map(lambda x: sum(review.count(x) for review in df_reviews['text']))

    # Filtrar la dataframe para quedarse solo con las palabras que aparecen al menos 10 veces en las reseñas
    df_words = df_words[df_words['count'] >= 10]

    # Obtener las 100 primeras filas de la dataframe
    df_words = df_words.head(200)
    return df_words

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