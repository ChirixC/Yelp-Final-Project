# nombre de la funcion: carga-sales_count_month

import pandas as pd

def leer_archivo(f_path):
    """
    Lee el archivo según su extensión. Disparado por la funcion "captura_evento"
    Args:
        event (dict): Event payload.
        file_path (str): ruta del archivo
        file_type (str): tipo del archivo
    """
    # Extraer el tipo de archivo
    f_type = f_path.split('.')[-1]
    
    # Revisando si archivo es csv
    if f_type == 'csv':
        # Leyendo archivo en dataframe
        df = pd.read_csv(f_path)

    # Revisando si archivo es json    
    elif f_type == 'json':
        try:
            # Intentar leer el archivo json como si no tuviera saltos de linea
            df = pd.read_json(f_path)
        except ValueError as e:
            if 'Trailing data' in str(e):
                # Leer el archivo json conteniendo saltos de linea
                df = pd.read_json(f_path, lines = True)
            else:
                # Cualquier otro error
                print('Ocurrió un error cargando el archivo JSON:', e)

    # Revisar si el archivo es tipo parquet
    elif f_type == 'parquet':
        # Leyendo archivo en dataframe
        df = pd.read_parquet(f_path)

    # Revisar si el archivo es tipo pkl (Pickle)
    elif f_type == 'pkl':
        try:
            # Leyendo archivo en DataFrame desde Google Cloud Storage
            df = pd.read_pickle(f_path)
        except Exception as e:
            print(f'Ocurrió un error al leer el archivo Pickle: {e}')
    
    return df

def limpiar_df(df):
    """
    Limpia el df "sales_count_month". Disparado por la funcion "captura_evento"
    Args:
        data (DataFrame): dataframe a limpiar.
    """
    
    try:
        """BLOQUE 1: modificar el dataframe"""

        #dividir el dataframe para cambiar los nombres de las columnas
        df1=df.iloc[:,0:5].copy()
        df2=df.iloc[:,5:].copy()

        #cambiar el formato de los nombres de las columnas para que tengan formato de fecha
        df2.columns=pd.to_datetime(df2.columns).strftime('%Y-%m-%d')

        #unir los datframe para volver a tener uno solo
        df=pd.concat([df1,df2],axis=1)

        #tomar los datos desde la segunda fila para no incluir los totales
        cantidad_ventas=df.iloc[1:,:].copy()
        #df.reset_index(drop=True)

        #eliminar del datafram las columnas que no sirven
        cantidad_ventas.drop(columns=["SizeRank","RegionName","RegionType","RegionID"], inplace=True)

        #agrupar el numero de ventas por estado
        demanda=cantidad_ventas.groupby("StateName").sum().reset_index()

        #limpia el resultado
        demanda.dropna()
        demanda.drop_duplicates()

        #transporner la columna para que las fechas sean los indices
        demanda=demanda.T

        # Establecer la primera fila como nombres de columnas
        demanda.columns = demanda.iloc[0]

        # Eliminar la primera fila del DataFrame
        demanda = demanda[1:]

        #convertir el indice en datetime
        demanda.index=pd.to_datetime(demanda.index)

        demanda.to_csv("demanda_dataset.csv", index=True)

        """BLOQUE 2: Crear una tabla de groupby y terminar de limpiar"""

        #agrupar el numero de ventas por estado
        demanda=cantidad_ventas.groupby("StateName").sum().reset_index()

        #limpia el resultado
        demanda.dropna()
        demanda.drop_duplicates()

        #transporner la columna para que las fechas sean los indices
        demanda=demanda.T

        # Establecer la primera fila como nombres de columnas
        demanda.columns = demanda.iloc[0]

        # Eliminar la primera fila del DataFrame
        demanda = demanda[1:]

        #convertir el indice en datetime
        demanda.index=pd.to_datetime(demanda.index)
        
        return demanda

    except Exception as e:
        print(f"An error occurred: {e}")

def cargar_df(project, dataset, table, df):
    """
    Carga el df limpio en bigquery. Disparado por la funcion "captura_evento"
    Args:
        project_id (str): nombre del proyecto
        dataset (str): ubicacion del dataset de destino en bigquery
        table_name (str): nombre de la tabla de destino en bigquery
        data_limpia (DataFrame): dataframe limpio para cargar a bigquery
    """
    
    try:
        # convierte todo el dataset a str para almacenar
        df = df.astype(str)
        
        # guarda el dataset en una ruta predefinida y si la tabla ya está creada la reemplaza
        df.to_gbq(destination_table = dataset + table, 
                    project_id = project,
                    table_schema = None,
                    if_exists = 'replace',
                    progress_bar = False, 
                    auth_local_webserver = False, 
                    location = 'us')
            
    except Exception as e:
        print(f"An error occurred: {e}")

def captura_evento(event, context):
    """
    Triggered by a change to a Cloud Storage bucket.
    Args:
        event (dict): Event payload.
    """

    try:
        # Obteniendo ruta de archivo modificado y tipo de archivo
        file_bucket = event["bucket"]
        file_path = event['name']
        file_name = file_path.split('/')[-1].split('.')[-2]
        full_path = 'gs://' + file_bucket + '/' + file_path
        
        # Ejecuta el código si los archivos se cargan en la carpeta correcta del bukcet
        if '/' in file_path:
            main_folder = file_path.split('/')[0]

            # Especifica el conjunto de datos y la tabla donde va a almacenar en bigquery
            if main_folder == "inmobiliaria":
                
                # Especifica proyecto, conjunto de datos y tabla de bigquery a trabajar
                project_id = 'lucid-forklift-401120'
                dataset = "inmobiliaria."
                # table_name = file_name
                table_name = "demanda_dataset"
                
                # crea el df segun el tipo de archivo
                data = leer_archivo(full_path)

                # llama la funcion para limpiar el df
                data_limpia = limpiar_df(data)
                
                # llama a la funcion para cargar el df
                cargar_df(project_id, dataset, table_name, data_limpia)

    except Exception as e:
        print(f"An error occurred: {e}")