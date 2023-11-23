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
    Evaluar estado actual de la empresa buscando oportunidades de mejora
    Evaluar estado de la competencia para ver donde se le puede robar mercado

## ¿Cómo lo haremos?

### Objetivo 1 (Comparacion del estado actual de la empresa con las reviews)
Establecer un modelo de NLP que devuelva la correlación entre palabras clave y rating a partir de las reseñas para determinar mejoras a implementar en los restaurantes.
Identificar palabras clave en los comentarios menores o igual a 3 estrellas, para detectar lo que se debe mejorar.
Identificar palabras clave en los comentarios mayores a 3 estrellas, para detectar lo que se debe mantener y potenciar.

### Objetivo 2 (Comparacion con la competencia)
Verificar los estados en dónde no estamos o los que nos va peor en comparación a la competencia para encontrar posibles oportunidades de adueñarse del mercado

### Objetivo Plus (Comparacion en la bolsa) 



# KPI


# Alcance



# Flujo de trabajo
<p align=center><img src="C:\Users\Pablo\Documents\Programacion\4 Henry\D) Proyectos Individiduales\3 - Trabajo Grupal\Trabajo\Yelp-Final-Project\img-readme\Flujo_de_Trabajo.png"><p>

En lo que se refiere al Stack tecnológico, nuestro cliente nos pidió hacer un análisis en base a las plataformas de reseñas Google Maps y Yelp. Para diagrama de Gannt, utilizamos la plataforma ClickUp, por su claridad, vistosidad y fácil repartición. En cuanto al EDA-ETL, los archivos de Google Maps están en formato JSON. Por otro lado, para los datasets de Yelp, tenemos tres archivos en formato JSON, uno en Python Pickle File (.pkl) y otro comprimido en formato parquet. Para su poder leerlos, utilizaremos al lenguaje de programación python, en un jupyer notebook. Serán usadas: la librería Pyarrow para leer el archivo parquet, la librería Pandas para convertirlo en un dataframe, Numpy para el área matemática, además de Matplotlib y Seaborn para la realización de gráficos en lo que se refiere al análisis exploratorio. Yfinance, para el análisis financiero de la empresa y su competencia. 

Para la infraestructura de datos, utilizaremos un servicio de almacenamiento en la nube. Elegimos la plataforma de Google Cloud (GCP) debido a su buena escalabilidad, rendimiento, seguridad y sus precios flexibles.

Por último, en la etapa de machine learning, utilizaremos, de nuevo, el lenguaje Python, a travez de Jupyter Notebook, Numpy y Pandas. Además, para el modelo de machine learning utilizaremos ScikitLearn.
Para todo lo que es visualizaciones de datos, usaremos PowerBI, ya que es una plataforma de la que disponemos un buen manejo y, además, es gratuita, a diferencia de otras (como por ejemplo Tableau).

# EDA
