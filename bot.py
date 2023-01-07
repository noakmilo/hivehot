import tweepy
import time
import requests
import datetime
import json

consumer_key = 'XXXXXXXXXXXXXXXXXXXXX'
consumer_secret = 'XXXXXXXXXXXXXXXXXXXXX'
access_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
access_token_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)

def obtener_precio(moneda):
    # Realiza una solicitud HTTP a la URL de la API de CryptoCompare
    url = f"https://min-api.cryptocompare.com/data/price?fsym={moneda}&tsyms=USD"
    respuesta = requests.get(url)
    # Obtiene el precio en USD de la respuesta
    precio = respuesta.json()['USD']
    return precio

# Obtiene el precio de HIVE y HBD en USD
precio_hive = obtener_precio('HIVE')
precio_hbd = obtener_precio('HBD')

# Obtiene la fecha actual en el formato "dd/mm/aaaa"
fecha = datetime.datetime.now().strftime("%d/%m/%Y")

# Crea un diccionario con los datos a escribir en el archivo
datos = {
  "fecha": fecha,
  "precio_hive": precio_hive,
  "precio_hbd": precio_hbd
}

# Abre el archivo en modo de escritura ('w')
with open("/usr/bin/hivehotbot/datos.json", "w") as archivo:
  # Usa la función json.dump() para escribir el diccionario en el archivo
  json.dump(datos, archivo)
  
def publicar_precios():
    fecha = datetime.datetime.now().strftime("%d/%m/%Y")
    mensaje = f"The Price of $HIVE and $HBD for today {fecha} is: \n\n🔴 HIVE: ${precio_hive}\n\n🟢 HBD: ${precio_hbd}\n\nJoin Hive.io to create, build and be rewarded in #Web3."
    # Publica el tweet y obtiene el objeto "Status" que representa al tweet
    tweet = api.update_status(mensaje)
    # Marca el tweet como favorito
    api.create_favorite(tweet.id)
    # Crea un diccionario con los datos a agregar al archivo
    datos = {
    'fecha': fecha,
    'precio_hive': precio_hive,
    'precio_hbd': precio_hbd
    }
    # Abre el archivo en modo de lectura ('r')
    with open("/usr/bin/hivehotbot/precios.json", "r") as archivo:
        # Usa la función json.load() para leer los datos del archivo
        datos_anteriores = json.load(archivo)

    # Asigna los datos del diccionario "datos" al diccionario "datos_anteriores"
    datos_anteriores.update(datos)

    # Abre el archivo en modo de escritura ('w')
    with open("/usr/bin/hivehotbot/precios.json", "w") as archivo:
        # Usa la función json.dump() para escribir los datos en el archivo
        json.dump(datos_anteriores, archivo)
while True:
    publicar_precios()
    time.sleep(86400)
