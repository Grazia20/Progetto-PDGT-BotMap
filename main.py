import os
import telepot
from time import sleep
import requests
import json
from telepot.namedtuple import ReplyKeyboardRemove, ReplyKeyboardMarkup

utente = {}

# definizione della funzione on_chat_message
def on_chat_message(message):
    content_type, chat_type, chat_id = telepot.glance(message)
    name = message["from"]["first_name"]

    try:
        utente[chat_id] = utente[chat_id]
    except:
        utente[chat_id] = 0
      

    if 'text' in message and message['text'] == '/start':
        bot.sendMessage(chat_id, "Usa il menu per vedere i comandi disponibili.\n")

    elif 'text' in message and message['text'] == '/search':
        message = 'Puoi inserire il nome di una città, regione, paese, etc. Oppure cliccare sulle città suggerite'
        markup = ReplyKeyboardMarkup(
            keyboard=[["Roma", "Parigi"], ["Tokyo", "Madrid"],
                      ["Los Angeles", "San Pietroburgo", "Sidney"]])
        bot.sendMessage(chat_id, message, reply_markup=markup)
        utente[chat_id] = 1
      
    elif 'text' in message and message['text'] == '/xid':
        bot.sendMessage(chat_id,
                         "Inserisci lo xid dell'attrazione turistica scelta: \n")
        utente[chat_id] = 2
      
    elif 'text' in message and message['text'] == '/catalog':
        bot.sendMessage(chat_id,
                         "Con questo avrai disponibile un url che ti permette di visualizzare la pagina con tutte le possibili opzioni per la categoria /types \n"+"Questo è l'url per il catologo: 'https://opentripmap.io/catalog'\n")
        utente[chat_id] = 3
    elif 'text' in message and message['text'] == '/position':
        bot.sendMessage(chat_id,
                         'Condividi la tua posizione(questo è possibile solo dai dispositivi mobili): ')
        utente[chat_id] = 4
    elif 'text' in message and message['text'] == '/radius':
        bot.sendMessage(chat_id,
                         'Inserisci la longitudine, latitudine e il raggio di ricerca(in metri):\n\n Esempio: 12.51133 41.89193 100000')
        utente[chat_id] = 5
      
    elif 'text' in message and message['text'] == '/types':
        markup = ReplyKeyboardMarkup(
            keyboard=[["cultural", "natural"], ["sport", "accomodations"],
                     ["tourist_facilities", "interesting_places", "amusements"]])
        bot.sendMessage(chat_id,
                         'Inserisci la longitudine, la latitudine e il type:\nEsempio: 12.51133 41.89193 natural \n Le categorie nei bottoni sono solo dei suggerimenti per il type da scrivere con le coordinate. Se invece vuoi controllare se il tipo che vuoi inserire è disponibile, clicca su /catalog per avere il link in cui sono mostrate tutte le possibili alternative)',reply_markup= markup)
        utente[chat_id] = 6
        
       
    elif utente[chat_id] == 1:
        if content_type == 'text':
            try: 
              r = requests.get(
                    url="https://api.opentripmap.com/0.1/en/places/geoname?name={}".format(str(message['text']))+"&apikey={}".format(my_secret))
              json_data = r.json()
              if "name" in json_data:
                name = json_data["name"]
                country = json_data["country"]
                timezone = json_data["timezone"]
                population = json_data["population"] 
                latitude = json_data["lat"]
                longitude = json_data["lon"] 
                bot.sendMessage(chat_id, "Hai cercato {} \n".format(name) +"Nazione: {}\n".format(country) +"Timezone: {};".format(timezone) + "\nNumero di abitanti: {}.\n".format(population) + "Longitudine:{} \t".format(longitude) + "Latitudine: {}".format(latitude))
                bot.sendLocation(chat_id, latitude,longitude)
                lon = longitude
                lat = latitude
                r2 = requests.get(url="https://api.opentripmap.com/0.1/en/places/radius?radius=1000&lon={}".format(lon)+"&lat={}".format(lat)+"&limit=10&apikey={}".format(my_secret))
                users = r2.json()
                name = []
                xid = []
                for index in range(0,len(users['features'])):
                  xid.append(users['features'][index]['properties']['xid'])
                  name.append(users['features'][index]['properties']['name'])
                bot.sendMessage(chat_id,"\nLista delle attrazioni turistiche che si trovano in un raggio di 1000 m dalle coordinate del luogo scelto:\n")
                bot.sendMessage(chat_id," ,\n".join(name))
                bot.sendMessage(chat_id,"I rispettivi xid, che puoi utilizzare per sapere di più sul monumento/museo etc. cliccando su /xid \n" )
                bot.sendMessage(chat_id, "\n".join(xid))  
              else:
                bot.sendMessage(chat_id,"Errore! Inserisci un luogo esistente ")
              utente[chat_id] = 0
            except:
                   bot.sendMessage(chat_id,"Errore! Inserisci un luogo esistente")

    elif utente[chat_id] == 2:
        if content_type == 'text':
            try:
                 r = requests.get(url="https://api.opentripmap.com/0.1/en/places/xid/{}?".format( message['text'])+"&apikey={}".format(my_secret))
                 json_data= r.json()
                 if "xid" in json_data:
                   xid = json_data["xid"]
                   bot.sendMessage(chat_id,"Il xid {}".format(xid)+" è disponibile.")
                 else:
                   bot.sendMessage(chat_id,"Errore! Inserire xid valido.")
                 if "name" in json_data:
                   name = json_data["name"]
                   bot.sendMessage(chat_id,"Nome: {} \n".format(name))
                 else:
                   bot.sendMessage(chat_id, "Non è disponibilie")
                 if "image" in json_data:
                   image = json_data["image"]
                   bot.sendPhoto(chat_id,image)
                 else:
                   bot.sendMessage(chat_id, "Non è disponibilie")
                 if "text" in json_data["wikipedia_extracts"]:
                   text = json_data["wikipedia_extracts"]["text"]
                   bot.sendMessage(chat_id,"Descrizione:\n {}".format(text))
                 else:
                   bot.sendMessage(chat_id, "Non è disponibilie")
                 lat = json_data["point"]["lat"]
                 lon = json_data["point"]["lon"]
                 bot.sendLocation(chat_id, lat,lon)
                 utente[chat_id] = 0
            except:
                  bot.sendMessage(chat_id,"Errore!")

    elif utente[chat_id] == 3:
        if content_type == 'text':
            bot.sendMessage(chat_id, message['text'] )
            utente[chat_id] = 0
  
    elif utente[chat_id] == 4:
        if content_type == 'location':
                list_of_dict_values = list(message['location'].values())
                longitude =  list_of_dict_values[1]
                latitude =  list_of_dict_values[0]
                lon = longitude
                lat = latitude
                r2 = requests.get(url="https://api.opentripmap.com/0.1/en/places/radius?radius=1000&lon={}".format(lon)+"&lat={}".format(lat)+"&limit=10&apikey={}".format(my_secret))
                users = r2.json()
                name = []
                xid = []
                for index in range(0,len(users['features'])):
                  xid.append(users['features'][index]['properties']['xid'])
                  name.append(users['features'][index]['properties']['name']) 
                bot.sendMessage(chat_id,"Lista delle attrazioni turistiche che si trovano nel raggio dalle coordinate del luogo scelto:\n")
                bot.sendMessage(chat_id," ,\n".join(name))
                bot.sendMessage(chat_id,"I rispettivi xid, che puoi utilizzare per sapere di più sul monumento/museo etc. cliccando su /xid \n" )
                bot.sendMessage(chat_id, "\n".join(xid))    
                utente[chat_id] = 0
        elif content_type == 'text':
                bot.sendMessage(chat_id,"Errore! Devi inviare la tua posizione")
          
    elif utente[chat_id] == 5:  
        if content_type == 'text':
            try: 
                  msg = message['text'].split()
                  longitude = msg[0]
                  latitude = msg[1]
                  distance = msg[2]
                  lon = longitude
                  lat = latitude
                  radius = distance
                  r2 = requests.get(url="https://api.opentripmap.com/0.1/en/places/radius?radius={}".format(radius)+"&lon={}".format(lon)+"&lat={}".format(lat)+"&limit=10&apikey={}".format(my_secret))
                  users = r2.json()
                  name = []
                  xid = []
                  for index in range(0,len(users['features'])):
                    xid.append(users['features'][index]['properties']['xid'])
                    name.append(users['features'][index]['properties']['name'])
                  bot.sendMessage(chat_id,"Lista delle attrazioni turistiche:\n")
                  bot.sendMessage(chat_id," ,\n".join(name))
                  bot.sendMessage(chat_id,"I rispettivi xid, che puoi utilizzare per sapere di più sull'attrazione turistica cliccando su /xid \n" )
                  bot.sendMessage(chat_id, "\n".join(xid))  
                  utente[chat_id] = 0
            except:
                    bot.sendMessage(
                        chat_id,
                        "Errore!Devi inserire le coordinate e il raggio in metri!")

    
    elif utente[chat_id] == 6:
        if content_type == 'text':
            try: 
                  msg = message['text'].split()
                  longitude = msg[0]
                  latitude = msg[1]
                  type = msg[2]
                  lon = longitude
                  lat = latitude
                  kinds = type 
                  r1 = requests.get(url="https://api.opentripmap.com/0.1/en/places/radius?radius=10000&lon={}".format(lon)+"&lat={}".format(lat)+"&kinds={}".format(kinds)+"&limit=10&apikey={}".format(my_secret))
                  json_data= r1.json()
                  name = []
                  xid = []
                  kinds = []
                  for index in range(0,len(json_data['features'])):
                    xid.append(json_data['features'][index]['properties']['xid'])
                    name.append(json_data['features'][index]['properties']['name'])
                    kinds.append(json_data['features'][index]['properties']['kinds'])
                  bot.sendMessage(chat_id,"Le attrazioni turistiche ricadono sotto queste sotto-categorie:\n"+"- \n".join(kinds))
                  bot.sendMessage(chat_id,"Nomi delle attrazioni turistiche: \n"+" ,\n".join(name))
                  bot.sendMessage(chat_id,"I rispettivi xid, che puoi utilizzare per sapere di più sul monumento/museo etc. cliccando su /xid \n" )
                  bot.sendMessage(chat_id, "\n".join(xid))
                  utente[chat_id] = 0
            except:
                  bot.sendMessage(chat_id,"Errore,devi inserire la longitudine, latitudine e il type")
try:
    bot = telepot.Bot(os.environ['TOKEN'])
    my_secret = os.environ['OPENDATA']
    bot.message_loop(on_chat_message)
    while (1):
        sleep(10)
finally:
    print("Esci")
