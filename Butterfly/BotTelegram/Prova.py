import requests
import json

token = '767404683:AAF6Fo4LP7wDWYmEbIRQ37KTX5GECMoTziA'

data = json.load(open("dati.json"))
IdUtenteProva = data["utente"][0]["telegram"]
MessaggioUtenteProva = data["utente"][0]["messaggio"]

response = requests.post(
    url='https://api.telegram.org/bot' + token + '/sendMessage?chat_id=' + IdUtenteProva + '&text=' + MessaggioUtenteProva +'',
).json()

if response != 0:
    print("Inviato")
else:
    print("Qualcosa è andato storto")
