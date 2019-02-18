#!/usr/bin/env python3

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

class WebhookConsumer(Consumer):
    """Implementa Consumer"""

    def __init__(self, topics: list, configs: dict):
        self._token = configs['telegram']['token_bot']
        self._receiver = configs['telegram']['receiver']

        configs = configs['kafka']

        # Converte stringa 'inf' nel relativo float
        if (configs['consumer_timeout_ms'] is not None
                and configs['consumer_timeout_ms'] == 'inf'):
            configs['consumer_timeout_ms'] = float('inf')

        self._consumer = KafkaConsumer(
            *topics,
            # Deserializza i messaggi dal formato JSON a oggetti Python
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            **configs
        )

    def listen(self):
        """Ascolta i messaggi provenienti dai Topic a cui il
        consumer è abbonato.

        Precondizione: i messaggi salvati nel broker devono essere
        in formato JSON, e devono contenere dei campi specifici
        definiti in nel modulo webhook
        """
        for message in self._consumer:
            final_msg = '{}:{}:{}:\tkey={}\n{}'.format(
                    message.topic,
                    message.partition,
                    message.offset,
                    message.key,
                    self.pretty(message.value),
                )

            print (final_msg)

            response = requests.post(
                url='https://api.telegram.org/bot' 
                    + self._token + '/sendMessage?chat_id=' 
                    + self._receiver + '&text=' 
                    + final_msg + '',
            ).json()

            if response['ok'] != 0:
                print('Inviato')
            else:
                print('Qualcosa è andato storto')


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
    with open(Path(__file__).parent.parent / 'topics.json') as f:
        topics = json.load(f)

    # Fetch delle configurazioni dal file config.json
    with open(Path(__file__).parent / 'config.json') as f:
        config = json.load(f)

    # Per ora, sono solo di interesse i nomi (label) dei Topic
    topiclst = []
    for topic in topics:
        # Per ogni topic, aggiunge a topiclst solo se non è già presente 
        if topic['label'] not in topiclst:
            topiclst.append(topic['label'])

    # Inizializza WebhookConsumer
    consumer = WebhookConsumer(
        topiclst,
        config
    )

    try:
        consumer.listen() # Resta in ascolto del Broker
    except KeyboardInterrupt as e:
        consumer.close()
        print(' Closing Consumer ...')
