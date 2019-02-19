"""
File: TelegramConsumer.py
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

Versione: 0.1.0
Creatore: Timoty Granziero, timoty.granziero@gmail.com
Autori:
    <nome cognome, email>
    <nome cognome: email>
    ....
"""

# Posizione: Butterfly/
# Uso: python3 -m path.to.WebhookConsumer

from kafka import KafkaConsumer
import kafka.errors
from abc import ABC, abstractmethod
import json
import requests
from pathlib import Path
from consumer.consumer import Consumer
import webhook.webhook as GLIssueWebhook

class TelegramConsumer(Consumer):
    """Implementa Consumer"""

    def __init__(self, topics: list, configs: dict):
        self._token = configs['telegram']['token_bot']
        self._receiver = configs['telegram']['receiver']
        self._topics = topics

        configs = configs['kafka']

        # Converte stringa 'inf' nel relativo float
        if (configs['consumer_timeout_ms'] is not None
                and configs['consumer_timeout_ms'] == 'inf'):
            configs['consumer_timeout_ms'] = float('inf')

        # Il parametro value_deserializer tornerà probabilmente
        # utile successivamente, per ora lasciamo il controllo
        # del tipo a listen()
        self._consumer = KafkaConsumer(
            *topics,
            # Deserializza i messaggi dal formato JSON a oggetti Python
            # value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            **configs,
        )

    def send(self, msg: str):
        """Manda il messaggio finale, tramite il bot,
        all'utente finale.
        """
        response = requests.post(
                url='https://api.telegram.org/bot' 
                    + self._token + '/sendMessage?chat_id=' 
                    + self._receiver + '&text=' 
                    + msg + '',
        ).json()

        print (msg)

        if response['ok'] != 0:
            print('Inviato')
        else:
            print('Qualcosa è andato storto')

    def listen(self):
        """Ascolta i messaggi provenienti dai Topic a cui il
        consumer è abbonato.

        Precondizione: i messaggi salvati nel broker devono essere
        in formato JSON, e devono contenere dei campi specifici
        definiti in nel modulo webhook
        """
        print('Listening to messages from topics:')
        for topic in self._topics:
            print(f'- {topic}')
        print()

        for message in self._consumer:
            print(f'Tipo messaggio: {type(message.value)}')

            value = message.value.decode('utf-8')
            try:
                value = self.pretty(json.loads(value))
            except json.decoder.JSONDecodeError:
                print(f'\n-----\nLa stringa "{value}" non è un JSON\n-----\n')

            final_msg = '{}:{}:{}:\tkey={}\n{}'.format(
                    message.topic,
                    message.partition,
                    message.offset,
                    message.key,
                    value,
            )

            # Invia la richiesta post per l'invio del messaggio
            self.send(final_msg)

            print() # Per spaziare i messaggi sulla shell


    def pretty(self, obj: object):
        """Restituisce una stringa con una formattazione migliore da un
        oggetto JSON (Webhook).

        Arguments:
        obj -- JSON object
        """

        return "".join(
            [
                f'Type: \t\t{obj["object_kind"]}',
                f'\nTitle: \t\t{obj["title"]}',
                f'\nProject ID: \t{obj["project"]["id"]}',
                f'\nProject name: \t{obj["project"]["name"]}',
                f'\nAction: \t{obj["action"]}\n ... ',
            ]
        )


    def close(self):
        """Chiude la connessione del Consumer"""
        self._consumer.close()


if __name__ == '__main__':

    """Fetch dei topic dal file topics.json
    Campi:
    - topics['id']
    - topics['label']
    - topics['project']
    """
    with open(Path(__file__).parents[2] / 'topics.json') as f:
        topics = json.load(f)

    # Fetch delle configurazioni dal file config.json
    with open(Path(__file__).parents[1] / 'config.json') as f:
        config = json.load(f)

    # Per ora, sono solo di interesse i nomi (label) dei Topic
    topiclst = []
    for topic in topics:
        # Per ogni topic, aggiunge a topiclst solo se non è già presente 
        if topic['label'] not in topiclst:
            topiclst.append(topic['label'])

    # Inizializza WebhookConsumer
    try:
        consumer = TelegramConsumer(
            topiclst,
            config
        )
    except kafka.errors.KafkaConfigurationError as e:
        print(e.with_traceback())

    try:
        consumer.listen() # Resta in ascolto del Broker
    except KeyboardInterrupt as e:
        consumer.close()
        print(' Closing Consumer ...')
