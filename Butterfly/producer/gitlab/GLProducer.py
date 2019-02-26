"""
File: GLProducer.py
Data creazione: 2019-02-18

<descrizione>

Licenza: Apache 2.0

Copyright 2019 AlphaSix

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Versione: 0.3.1
Creatore: Timoty Granziero, timoty.granziero@gmail.com
Autori:
    Laura Cameran, lauracameran@gmail.com
    Samuele Gardin, samuelegardin@gmail.com
"""

# import argparse
import json
from pathlib import Path
import pprint
from sys import stderr

from flask import Flask
from flask import request
from kafka import KafkaProducer
import kafka.errors

from producer.producer import Producer
from webhook.gitlab.GLIssueWebhook import GLIssueWebhook

# Parsing dei parametri da linea di comando
# parser = argparse.ArgumentParser(description='Crea messaggi su Kafka')
# parser.add_argument('-t', '--topic', type=str,
#                     help='topic di destinazione')
# args = parser.parse_args()

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def api_root():

    # Percorso fino a webhook.json
    # webhook_path = (
    #     Path(__file__).parents[2] /
    #     'webhook' /
    #     'webhook.json'
    # )

    if request.headers['Content-Type'] == 'application/json':

        # Configurazione da config.json
        with open(Path(__file__).parents[1] / 'config.json') as f:
            config = json.load(f)

        """Fetch dei topic dal file topics.json
        Campi:
        - topics['id']
        - topics['label']
        - topics['project']
        """
        with open(Path(__file__).parents[2] / 'topics.json') as f:
            topics = json.load(f)

        # Istanzia il Producer
        producer = GLProducer(config)

        webhook = request.get_json()
        print(
            '\n\n\nMessaggio da GitLab:\n'
            f'{pprint.pformat(webhook)}\n\n\n'
            'Parsing del messaggio ...'
        )

        # if args.topic:  # Topic passato con la flag -t
        #     # #producer.produce(args.topic, webhook_path)
        #     # producer.produce(args.topic, webhook)
        # else:  # Prende come Topic di default il primo del file webhook.json

        try:
            producer.produce(topics[0]['label'], webhook)
            print('Messaggio inviato.\n\n')
        except KeyError:
            print('Warning: messaggio malformato. '
                  'Non è stato possibile effettuare il parsing.\n'
                  'In attesa di altri messaggi...\n\n')

        return '', 200

    else:
        return '', 400


class GLProducer(Producer):

    def __init__(self, config):
        notify = False
        while True:  # Attende una connessione con il Broker
            try:
                self._producer = KafkaProducer(
                    # Serializza l'oggetto Python
                    # in un oggetto JSON, codifica UTF-8
                    value_serializer=lambda m: json.dumps(m).encode('utf-8'),
                    **config
                )
                break
            except kafka.errors.NoBrokersAvailable:
                if not notify:
                    notify = True
                    print('Broker offline. In attesa di una connessione ...')
            except KeyboardInterrupt:
                print(' Closing Producer ...')
                exit(1)
        print('Connessione con il Broker stabilita')

    def produce(self, topic: str, whook: object):
        """Produce il messaggio in Kafka.

        Arguments:
        topic -- il topic dove salvare il messaggio.
        path -- percorso fino al json
        """

        # assert isinstance(path, Path), 'path non è di tipo Path'

        webhook = GLIssueWebhook(whook)

        # Parse del JSON associato al webhook ottenendo un oggetto Python
        webhook.parse()
        try:
            # Inserisce il messaggio in Kafka, serializzato in formato JSON
            self.producer.send(topic, webhook.webhook)
            self.producer.flush(10)  # Attesa 10 secondi
        # Se non riesce a mandare il messaggio in 10 secondi
        except kafka.errors.KafkaTimeoutError:
            stderr.write('Errore di timeout\n')
            exit(-1)

    @property
    def producer(self):
        """Restituisce il KafkaProducer"""
        return self._producer

    # def close(self):
    #    """Rilascia il Producer associato"""
    #    self._producer.close()


def main():
    app.run(host='0.0.0.0', port='5004')


if __name__ == '__main__':
    main()
