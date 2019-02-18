"""
File: ConsoleConsumer.py
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
# Uso: python3 -m path.to.ConsoleConsumer

from kafka import KafkaConsumer
import kafka.errors
from abc import ABC, abstractmethod
import json
import requests
from pathlib import Path
from consumer.consumer import Consumer


class ConsoleConsumer(Consumer):
    """Implementa Consumer"""

    def __init__(self, topics: list, configs: dict):

        self._token = configs['telegram']['token_bot']
        self._receiver = configs['telegram']['receiver']

        configs = configs['kafka']
        self._topics = topics

        # Converte stringa 'inf' nel relativo float
        if (configs['consumer_timeout_ms'] is not None
                and configs['consumer_timeout_ms'] == 'inf'):
            configs['consumer_timeout_ms'] = float('inf')

        self._consumer = KafkaConsumer(*topics, **configs)


    def listen(self):
        """Ascolta i messaggi provenienti dai Topic a cui il consumer è
        abbonato.
        Precondizione: i messaggi devono essere codificati in binario.
        """
        print('Listening to messages from topics:')
        for topic in self._topics:
            print(f'- {topic}')
        print()

        for message in self._consumer:
            final_msg = ('{}:{}:{}:\nkey={}\nvalue={}'
                .format(
                    message.topic,
                    message.partition,
                    message.offset,
                    message.key,
                    message.value.decode()
                )
            )

            # final_msg = (
            #     f'{message.topic}:'
            #     f'{message.partition}:'
            #     f'{message.offset}:'
            #     f'\nkey={message.key}'
            #     f'\nvalue={message.value.decode()}'
            # )

            print (final_msg)

            # print(self._token)
            # print(self._receiver)
            response = requests.post(
                url='https://api.telegram.org/bot' 
                    + self._token + '/sendMessage?chat_id=' 
                    + self._receiver + '&text=' 
                    + final_msg + ''
            ).json()

            if response['ok'] != 0:
                print('Inviato')
            else:
                print('Qualcosa è andato storto')


    @property
    def consumer(self):
        """Restituisce il KafkaConsumer"""
        return self._consumer

    def close(self):
        """Chiude la connessione del Consumer"""
        self._consumer.close()


def main():

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

    try:
        # Inizializza WebhookConsumer
        consumer = ConsoleConsumer(
            topiclst,
            config,
        )
    except kafka.errors.KafkaConfigurationError as e:
        print(e.with_traceback())

    try:
        consumer.listen() # Resta in ascolto del Broker
    except KeyboardInterrupt as e:
        consumer.close()
        print(' Closing Consumer ...')


if __name__ == '__main__':
    main()
