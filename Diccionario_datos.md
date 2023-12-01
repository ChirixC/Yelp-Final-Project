<h1 align=center> <strong>Diccionario de datos</strong> </h1>

# Google Maps

## Google-metadata-sitios

La carpeta tiene 11 archivos .json donde se dispone la metadata contiene información del comercio, incluyendo localización, atributos y categorías.

Como ejemplo, tenemos:

- Str, nombre del comercio
    - 'name: 'Walgreens Pharmacy', 

- Id en Google Maps
    - 'gmap_id': '0x881614ce7c13acbb:0x5c7b18bbf6ec4f7e', 

- Float, latitud
    - 'latitude': 41.451859999999996, 

- Float, longitud
    - 'longitude': -85.2666757, 

- Str, categoria del comercio
    - 'category': ['Pharmacy'], 

- Int, promedio del puntaje de los comercios
    - 'avg_rating': 4.2, 
- Int, cantidad de reviews
    - 'num_of_reviews': 5,

## Google-reviews-estados

<p align="center">
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Google_Maps_Logo_2020.svg/512px-Google_Maps_Logo_2020.svg.png"  height="200">

Los archivos donde se disponibiliza las reviews de los usuarios (51 carpetas, 1 por cada estado de USA, con varios archivos .json cada uno) se conforman de la siguiente manera

Como ejemplo, tomemos un estado al azar:

- String, id del usuario que hace la review
    - 'user_id': '101463350189962023774',

- String, nombre del usuario
    - 'name': 'Jordan Adams',

- Datetime, momento de cuando se hizo la review
    - 'time': 2021-07-04T20:48:54.826000,

- Entero, puntaje del usuario
    - 'rating': 5,

- Str, texto de la review
    - 'text': 'Cool place, great people, awesome dentist!' ,

- Str, id en google maps
    - 'gmap_id': '0x87ec2394c2cd9d2d:0xd1119cfbee0da6f3',

# Dataset de Yelp!

## Yelp-business.pkl

<p align="center">
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Yelp_Logo.svg/2560px-Yelp_Logo.svg.png"  height="200">

Contiene información del comercio, incluyendo localización, atributos y categorías.

- String, 22 caracteres id del negocio, refiere al negocio en   business.    json
    - "business_id": "tnhfDv5Il8EaGSXZGiuQGg",

- String, nombre del negocio
    - "name": "Garaje",

- String, direccion completa del negocio
    - "address": "475 3rd St",

- String, ciudad
    - "city": "San Francisco",

- String, codigo de 2 letras del Estado donde se ubica el negocio
    - "state": "CA",

- Float, latitud
    - "latitude": 37.7817529521,

- Float, longitud
    - "longitude": -122.39612197,

- Float, rating en estrellas, redondeado a 0 o 0.5
    - "stars": 4.5,

- Entero, numero de reseñas
    - "review_count": 1198,

- Lista de categorias de los negocios
    - "categories": 
    "Mexican",
    "Burgers",
    "Gastropubs",

## Yelp-review.json

Contiene las reseñas completas, incluyendo el user_id que escribió el review y el business_id por el cual se escribe la reseña

- String, 22 caracteres id de reseña
    - "review_id": "zdSx_SD6obEhz9VrW9uAWA",

- String, 22 caracteres id único de usuario, refiere al usuario en user.json
    - "user_id": "Ha3iJu77CxlrFm-vQRs_8g",

- String, 22 caracteres id del negocio, refiere al negocio en business.json
    - "business_id": "tnhfDv5Il8EaGSXZGiuQGg",

- Entero, puntaje en estrellas de 1 al 5
    - "stars": 4,

- String, fecha formato YYYY-MM-DD
    - "date": "2016-03-09",

- String, la reseña en inglés
    - "text": "Great place to hang out after work: the prices are decent, and the ambience is fun. It's a bit loud, but very lively. The staff is friendly, and the food is good. They have a good selection of drinks.",

- Entero, números de votos como reseña útil
    - "useful": 0,

- Entero, número de votos como reseña graciosa
    - "funny": 0,

- Entero, número de votos como reseña cool.
    - "cool": 0

## Yelp-user.parquet
 Data del usuario incluyendo referencias a otros usuarios amigos y a toda la metadata asociada al usuario.

- String, 22 caracteres, id de usuario que refiere al usuario en user.json
    - "user_id": "Ha3iJu77CxlrFm-vQRs_8g",

- String, nombre del usuario
    - "name": "Sebastien",

- Entero, numero de reseñas escritas
    - "review_count": 56,

- String, fecha de creacion del usuario en Yelp en formato YYYY-MM-DD
    - "yelping_since": "2011-01-01",

- Lista con los id de usuarios que son amigos de ese usuario
    - "friends": 
    "wqoXYLWmpkEH0YvTmHBsJQ",
    "KUXLLiJGrjtSsapmxmpvTA",
    "6e9rJKQC3n0RSKyHLViL-Q"
,

- Entero, número de votos marcados como útiles por el usuario
    - "useful": 21,

- Entero, número de votos marcados como graciosos por el usuario
    - "funny": 88,

- Entero, número de votos marcados como cool por el usuario
    - "cool": 15,

- Entero, número de fans que tiene el usuario
    - "fans": 1032,

- Lista de enteros, años en los que el usuario fue miembro elite
    - "elite": 
    2012,
    2013
,

- Float, promedio del valor de las reseñas
    - "average_stars": 4.31,

- Entero, total de cumplidos 'hot' recibidos por el usuario
    - "compliment_hot": 339,

- Entero, total de cumplidos varios recibidos por el usuario
    - "compliment_more": 668,

- Entero, total de cumplidos por el perfil recibidos por el usuario
    - "compliment_profile": 42,

- Entero, total de cumplidos 'cute' recibidos por el usuario
    - "compliment_cute": 62,

- Entero, total de listas de cumplidos recibidos por el usuario
    - "compliment_list": 37,

- Entero, total de cumplidos como notas recibidos por el usuario
    - "compliment_note": 356,

- Entero, total de cumplidos planos recibidos por el usuario
    - "compliment_plain": 68,

- Entero, total de cumplidos 'cool' recibidos por el usuario
    - "compliment_cool": 91,

- Entero, total de cumplidos graciosos recibidos por el usuario
    - "compliment_funny": 99,

- Entero, número de complidos escritos recibidos por el usuario
    - "compliment_writer": 95,

- Entero, número de cumplidos en foto recibidos por el usuario
    - "compliment_photos": 50

## Yelp-tip.json
 Tips (consejos) escritos por el usuario. Los tips son más cortas que las reseñas y tienden a dar sugerencias rápidas.

- String, texto del tip
    - "text": "Secret menu - fried chicken sando is da bombbbbbb Their zapatos are good too.",

- Datetime, fecha cuando se escribio el tip
    - "date": 2021-12-03T18:35:53,

- Entero, cuantos cumplidos totales tiene
    - "compliment_count": 172,

- String, 22 caracteres, id del negocio que se refiere al negocio en business.json
    - "business_id": "tnhfDv5Il8EaGSXZGiuQGg",

- String, 22 caracteres de id de usuario, que se refieren al usuario en user.json
    - "user_id": "49JhAJh8vSQ-vM4Aourl0g"