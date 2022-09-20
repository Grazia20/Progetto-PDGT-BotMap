
## Progetto Piattaforme digitali per la gestione del territorio

### secondo appello sessione autunnale a.a. 21/22
#### Cossu Grazia, numero maricola: 300240

## Titolo: BotMap

#### Scopo del progetto:

Il progetto si pone come obiettivo il saper fornire informazioni all'utente riguardanti un determinato luogo basandosi quasi del tutto sulle coordinate geografiche, con l'utilizzo di un bot Telegram (BotMap) e un insieme di dati reperiti attraverso il sito "https://opentripmap.io/product".

#### Scelte implementative:

Ho voluto realizzare il progetto utilizzando il linguaggio Python e lo sviluppato attraverso l'utilizzo della piattaforma "Replit.com". Ho dovuto installare i packager: pyTelegramBotAPI,telepot e json per leggeri la documentazione dell'API di OpenTripMap.

#### API utilizzate:

Mi sono servita delle API fornite dal sito OpenTripMap e dal Bot di Telegram .La prima consente di ottenere i dati degli oggetti dal database OpenTenipMap utilizzando le richieste HTTP.
OpentripMap é basato sull'elaborazione cooperativa di diverse fonti di dati aperti (OpenStreetMap, Wikidata, Wikipedia, Ministero della cultura e Ministero delle risorse naturali e dell'ambiente della Federazione Russa) e comprende oltre 10 milioni di attrazioni turistiche e strutture in tutto il mondo.
La seconda è un'interfaccia basata su HTTP. I Bot non sono altro che utenti artificiali di Telegram e, composti soltanto da stringhe di codice, sono programmati per interagire nelle chat singole (ma anche in quelle di gruppo) con altri utenti dell’applicazione di messaggistica. Non sono utenti reali, sebbene siano creati per svolgere azioni e interagire.

#### Documentazione dell'API:

Di seguito sono riportate tutte le richieste dell' API che il servizio fornisce con una descrizione dettagliata del loro funzionamento. Per entrambe servono delle API key; in Replit, le chiavi vengono salvate in Secrets(System environment variables.) e posso utilizzarle in questo modo:

.![Screenshot secrets](https://user-images.githubusercontent.com/62015297/191298891-11c9a097-79c8-4aae-9fd8-4f2ac69aa670.png)


Da *OpenTripMap*:

**GET**:

 * Coordinate geografiche di un posto:
            - https://api.opentripmap.com/0.1/en/places/geoname?name=

 * Lista di oggetti:
       - https://api.opentripmap.com/0.1/en/places/radius?radius=
      A questa aggiungo i seguenti parametri:
          - longitudine
          - latitudine
          - limite
          - kinds
  
 * Proprietà dell'oggetto:
        - https://api.opentripmap.com/0.1/en/places/xid/{xid}

Da *Telegram*:

Per visualizzare sul bot i risultati e per interagire con l'utente, utilizzo i seguenti metodi:

**POST**:

 * bot.send_message - Restitusce messaggi di testo.  Nei due comandi /search e /types, utilizzo il parametro reply_markup che mi permette di inserire un'interfaccia aggiuntiva. Nel primo caso, la tastiera ReplyKeyboard permette di ottenere i risultati cliccandoci, nel secondo,invece, sono dei suggerimenti sulla tipologia che si può inserire insieme alle coordinate.
 
 * bot.send_photo - Restituisce una foto.
 
 * bot.send_location - ritorna un punto nella mappa.


### Comandi disponibili nel BotMap:

 * /start - Restituisce "Usa il menu per vedere i commandi disponibili."
 * /search - Restituisce le coordinate geografiche per il toponimo dato (regione, città, villaggio, ecc.).
 
 * /xid - Restituisce informazioni dettagliate sull'oggetto. Gli oggetti possono contenere:
          - nome
          - immagine
          - posizione
          - breve descrizione
 
 * /types - Il metodo restituisce gli oggetti più vicini al punto selezionato filtrati attraverso la tipologia scelta.
 
  * /catalog - Metodo che ritorna una mappa sulle varie tipologie che si possono usare nel metodo /types.
 
 * /radius - Il metodo restituisce un numero di oggetti nel riquadro di delimitazione specificato.
 
 * /position - Metodo che in base alla tua posizione restituisce una lista di oggetti con i loro identificativi.

### Test del sistema:
Il server non è sempre attivo. Per accedere al servizio è necessario accedere al client tramite il seguente endpoint "https://replit.com/@IHTL00/BotMap#main.py".

Esecuzione di alcuni dei comandi disponibili:

![Screenshot catalog](https://user-images.githubusercontent.com/62015297/191299157-ea1a1d04-cc9e-4d91-8bcb-95f48bc92564.png)

![Screenshot position0](https://user-images.githubusercontent.com/62015297/191299928-1832d35c-ae92-4782-899c-e43b0b947b6f.png)
![Screenshot position1](https://user-images.githubusercontent.com/62015297/191300024-b1380782-23a3-4f9b-9d23-36c57de6286b.png)

![Screenshot search0](https://user-images.githubusercontent.com/62015297/191300273-34204ac3-6e11-43e9-8f6c-1812776336cb.png)
![Screenshot search1](https://user-images.githubusercontent.com/62015297/191301027-d0743949-5d81-4a25-9ddc-0fc6eeabd9b0.png)
