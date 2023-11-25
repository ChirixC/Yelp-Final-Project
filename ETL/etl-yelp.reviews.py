import pandas as pd
import os

YELP_REVIEWS_PATH = '../Yelp-Data/review.parquet'   # Modificarlo para correrlo desde la carpeta inicial
YELP_BUSINESS_PATH = '../Yelp-Data/business-fixed.parquet'

def load_files(yelp_reviews_file, yelp_business_file): # Ahora lee archivos parquet, esto se debería modificar para leer los json
    yelp_reviews_df = pd.read_parquet(yelp_reviews_file)
    yelp_business_df = pd.read_parquet(yelp_business_file)
    return yelp_reviews_df, yelp_business_df

# Nota si queremos otra categoría desde el business.pkl debería tener una entrada del tipo de negocio al q pertenece el negocio entrante
def merge_dfs(yelp_reviews_df, yelp_business_df): # Aquí se unen TODAS las reviews con la Dataframe de TODOS los negocios de esa categoria
    merged_df = yelp_reviews_df.merge(yelp_business_df, on='business_id', how='inner')
    return merged_df

# Debería haber una función para encontrar el business id del negocio
def find_buisness_id(business_name):
    # Definir
    return None

def select_business(merged_df, business_name):
    selected_df = merged_df[merged_df['name'].str.contains(business_name)]
    return selected_df

def main():
    business_name = 'Texas Roadhouse' # Podría ser un INPUT del nombre del negocio para que nos devuelva métricas diferentes
    # Este nombre sirve para cualquier negocio en esta categoria, o sea principal y competencias
    # Tal vez deberían haber dos retornos uno para el principal y otro para todas las competencias
    # O uno para cada top de la competencia
    yelp_reviews_df, yelp_business_df = load_files(YELP_REVIEWS_PATH,YELP_BUSINESS_PATH)
    merged_dfs = merge_dfs(yelp_reviews_df, yelp_business_df)

    selected_business = select_business(merged_dfs, business_name)
    selected_info = selected_business.info()

    print(f'Si está correcto en el .info debería dar 5402 seleccionados {selected_info}')

if __name__ == "__main__":
    main()
    # os.getcwd()
