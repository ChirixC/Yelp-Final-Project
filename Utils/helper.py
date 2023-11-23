import pandas as pd
import json

def data_overview(df_Accesos_Cien):
    '''    
    Devuelve:
        un dataframe de pandas que tiene lo siguiente: 
        ** nombre_campo, tipo_datos,no_nulos_%,nulos_%,nulos(cantidad)
    '''

    result_dict = {"nombre_campo": [], "tipo_datos": [], "NO_nulos_%": [], "nulos_%": [], "nulos_cantidad": []}

    for column in df_Accesos_Cien.columns:
        porcentaje_no_nulos = (df_Accesos_Cien[column].count() / len(df_Accesos_Cien)) * 100
        result_dict["nombre_campo"].append(column)
        result_dict["tipo_datos"].append(df_Accesos_Cien[column].apply(type).unique())
        result_dict["NO_nulos_%"].append(round(porcentaje_no_nulos, 2))
        result_dict["nulos_%"].append(round(100-porcentaje_no_nulos, 2))
        result_dict["nulos_cantidad"].append(df_Accesos_Cien[column].isnull().sum())

    df_Accesos_Cien_output = pd.DataFrame(result_dict)
        
    return df_Accesos_Cien_output


def outliers_percentage(df, column_outlier):
    '''
        Esta funcion retorna el numero de outliers y el porcentaje que representan del total de registros
    '''
    column_outlier = column_outlier

    # Calcular la media y la desviación estándar de la column
    mean = df[column_outlier].mean()
    std_dev = df[column_outlier].std()

    # Definir un umbral (por ejemplo, 3 desviaciones estándar)
    threshold = 3

    # Identificar outliers por encima y por debajo del umbral
    outliers_above = df[df[column_outlier] > (mean + threshold * std_dev)]
    outliers_below = df[df[column_outlier] < (mean - threshold * std_dev)]

    # Combinar outliers por encima y por debajo
    outliers = pd.concat([outliers_above, outliers_below])

    total_outliers = len(outliers)
    total_records = len(df)

    return print(f"Total de outliers en {column_outlier}: {total_outliers} de {total_records} registros -- {round((total_outliers/total_records)*100,2)} %")


def calculate_outliers(df, column_outlier):

    column_outlier = column_outlier

    # Calcular la media y la desviación estándar de la column
    mean = df[column_outlier].mean()
    std_dev = df[column_outlier].std()

    # Definir un umbral (por ejemplo, 3 desviaciones estándar)
    threshold = 3

    # Identificar outliers por encima y por debajo del umbral
    outliers_above = df[df[column_outlier] > (mean + threshold * std_dev)]
    outliers_below = df[df[column_outlier] < (mean - threshold * std_dev)]

    # Combinar outliers por encima y por debajo
    outliers = pd.concat([outliers_above, outliers_below])

    return outliers

def merge_dataframes(ruta, rango):
    '''
    Recibe como parametro la ruta sin el nombre del archivo, solo la ruta
    Recibe el rango que es el numero de archivos a concatenar
    '''
    # Lista para almacenar todos los dataframes
    lista_dataframes = []
    # Iterar sobre los archivos del 1 al valor total de archivos
    for i in range(1, rango+1):
        # Construir la ruta del archivo JSON
        ruta_archivo = f'{ruta}/{i}.json'

        # Leer el archivo JSON línea por línea
        filas_json = []
        with open(ruta_archivo) as f:
            for line in f.readlines():
                data = json.loads(line)
                filas_json.append(data)

        # Crear un dataframe a partir del JSON y agregarlo a la lista
        df_temp = pd.DataFrame(filas_json)
        lista_dataframes.append(df_temp)
    df_state = pd.concat(lista_dataframes, ignore_index=True)
    return df_state
