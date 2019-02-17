#!/usr/bin/env python3

# Uso: python3 path/to/prova.py "messaggio da inviare"
# Dando chmod+x sullo script è possibile omettere python3

import requests, json, argparse
from pathlib import Path

# Permette l'avvio dello script da qualsiasi posizione
with open(Path(__file__).parent / "dati.json") as f:
    data = json.load(f)

parser = argparse.ArgumentParser(description="Invia un messaggio all\'utente con l\'ID")
parser.add_argument('message', type=str, nargs='+',
                    help='messaggio da inviare')

args = parser.parse_args()

token = '767404683:AAF6Fo4LP7wDWYmEbIRQ37KTX5GECMoTziA'
# id_utente = data["utente"][0]["telegram"]
#id_utente = "38883960" #TIM Inserire il proprio ID Telegram ottenibile da @myidbot
id_utente = "265266555" #Laura

# messaggio = data["utente"][0]["messaggio"]
messaggio = ''.join(args.message)

response = requests.post(
    url='https://api.telegram.org/bot' + token + '/sendMessage?chat_id=' + id_utente + '&text=' + messaggio + ''
).json()

if response != 0:
    print("Inviato")
else:
    print("Qualcosa è andato storto")
