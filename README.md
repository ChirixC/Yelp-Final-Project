<h1 align=center> <strong>Proyecto Grupal</strong> </h1>
<h2 align="center">Data Science</h2>

# Introducción

Estados Unidos es un país que cuenta con una gran oferta y diversidad gastronomica que reflejan las 
diversas comunidades y culturas del país.

Uno de los principales rubros y de los más tradicionales del país son las llamadas steakhouses, restaurantes especializados en servir filetes de carne de vacuno.

En este proyecto nos enfocaremos en este rubro, siendo nuestro empleador una cadena de restaurantes, con el objetivo general de brindar oportunidades de mejora y permitirle sobrezalir por encima la competencia.

# Sobre nosotros

Somos Data Finance, una empresa consultora que se especializa en el análisis de datos, donde fusionamos la potencia del Data Science con la precisión financiera y brinda posibles soluciones, mejoras de mercado. Aquí la innovación y la analítica avanzada convergen para optimizar sus operaciones y maximizar sus resultados. Incorporamos lo último en lo que refiere al análisis de datos, machine learning y tecnologias de vanguardia.

# Nuestro Cliente

<p align=center><img src="https://upload.wikimedia.org/wikipedia/en/thumb/b/b0/Texas_Roadhouse.svg/1200px-Texas_Roadhouse.svg.png"><p>

Texas Rodhouse Es de las más grandes steakhouse de los Estados Unidos, trabaja desde hace treinta años, ubicado en 49  estados y en 10 paises, con tantos 627 establecimientos, 29 de ellos internacionales. Siendo de los más grandes en su rubro, sus mas grandes competidores son LongHorn Steakhouse Saltgrass Steak House y Logan's Roadhouse Las acciones de Texas Rodhouse tienen un valor de 111.93 dolares en la bolsa.

# Nuestros Objetivos

## Objetivo General

-	El objetivo principal es extraer conocimientos significativos a partir de una extensa base de datos de reviews de restaurantes. Mediante técnicas de minería de datos y análisis estadístico, buscaremos identificar patrones, tendencias y factores clave que influyan en la satisfacción del cliente y en la reputación de nuestro cliente, la cadena Texas Rodhouse. El propósito es proporcionar insights valiosos para mejorar la calidad de sus servicios, optimizar la experiencia del cliente y fortalecer la posición competitiva de los establecimientos gastronómicos, identificando posibles localidades con potencial para expandir el negocio. 
¿Cómo lo haremos?

### Objetivo 1 (Identificar fortalezas en los mercados más pujantes)

1.	Segmentación Geográfica: Identificar aquellos Estados donde los clientes tienen una mejor valoración de los servicios del cliente. Segmentar nuestros 10 mercados más pujantes a partir de las calificaciones y la valoración de los clientes.

2.	Sentimiento del Cliente: Crear un modelo de procesamiento de lenguaje natural (NLP) que muestre la relación entre palabras clave y calificaciones basándose en las reseñas, en los Estados ya filtrados anteriormente. 

3.	Factores de Influencia: Detectar las palabras clave presentes en los comentarios con calificaciones superiores a 3 estrellas para identificar aspectos que deben ser preservados y fortalecidos.

### Objetivo 2 (Identificar futuros mercados)

1.	Evaluación de Mercados Competitivos: Analizar e identificar Estados en los que la competencia presente un desempeño sólido. Realizar un mapeo detallado de las ubicaciones donde los competidores tienen presencia exitosa.

2.	Comparación con Presencia Actual: Contrastar la información obtenida con la presencia actual de sucursales en esos Estados. Identificar brechas geográficas donde la empresa no tiene presencia pero donde la competencia demuestra éxito.

3.	Propuesta de Nuevas Sucursales: Formular recomendaciones estratégicas para la apertura de nuevas sucursales en aquellos Estados y localidades donde la competencia prospera y la empresa aún no tiene una presencia establecida. Evaluar el potencial de crecimiento y la viabilidad de expansión en estas áreas.

### Objetivo Plus (Financiero) 

1.	Evaluación del Desempeño en el Contexto del NASDAQ: Analizar el rendimiento financiero de la empresa en relación con el índice NASDAQ y el S&P 500. Comparar las tendencias y variaciones del valor de las acciones de la empresa con el comportamiento general del NASDAQ para entender la posición relativa en el mercado y la influencia de factores macroeconómicos en su desempeño. Esto proporcionará una perspectiva adicional para la toma de decisiones financieras y estratégicas.

2.	Proyección de Ingresos: Estimar los ingresos potenciales derivados de la apertura de nuevas sucursales en los mercados seleccionados. Utilizar datos históricos y proyecciones de crecimiento para calcular posibles flujos de ingresos.

# KPI


# Alcance



# Flujo de trabajo
<p align=center><img src="img-readme\Flujo_de_Trabajo.png"><p>


En lo que se refiere al Stack tecnológico, nuestro cliente nos pidió hacer un análisis en base a las plataformas de reseñas Google Maps y Yelp. Para diagrama de Gannt, utilizamos la plataforma ClickUp, por su claridad, vistosidad y fácil repartición. En cuanto al EDA-ETL, los archivos de Google Maps están en formato JSON. Por otro lado, para los datasets de Yelp, tenemos tres archivos en formato JSON, uno en Python Pickle File (.pkl) y otro comprimido en formato parquet. Para su poder leerlos, utilizaremos al lenguaje de programación python, en un jupyer notebook. Serán usadas: la librería Pyarrow para leer el archivo parquet, la librería Pandas para convertirlo en un dataframe, Numpy para el área matemática, además de Matplotlib y Seaborn para la realización de gráficos en lo que se refiere al análisis exploratorio. Yfinance, para el análisis financiero de la empresa y su competencia. 

Para la infraestructura de datos, utilizaremos un servicio de almacenamiento en la nube. Elegimos la plataforma de Google Cloud (GCP) debido a su buena escalabilidad, rendimiento, seguridad y sus precios flexibles.

Por último, en la etapa de machine learning, utilizaremos, de nuevo, el lenguaje Python, a travez de Jupyter Notebook, Numpy y Pandas. Además, para el modelo de machine learning utilizaremos ScikitLearn.
Para todo lo que es visualizaciones de datos, usaremos PowerBI, ya que es una plataforma de la que disponemos un buen manejo y, además, es gratuita, a diferencia de otras (como por ejemplo Tableau).

# EDA
