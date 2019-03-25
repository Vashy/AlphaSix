"""
File: consumer.py
Data creazione: 2019-02-13

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

from abc import ABC, abstractmethod

from kafka import KafkaConsumer
# import kafka.errors
import json
# from pathlib import Path


class Consumer(ABC):
    """Interfaccia Consumer"""
    
    def __init__(self, consumer: KafkaConsumer):
        # Configs ...

        self._consumer = consumer

    def prelisten_hook(self):
        pass

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

        self.prelisten_hook()  # Hook!

        # Si mette in ascolto dei messsaggi dal Broker
        for message in self._consumer:
            print(f'Tipo messaggio: {type(message.value)}')

            value = message.value.decode('utf-8')
            try:
                value = self.pretty(json.loads(value))
            except json.decoder.JSONDecodeError:
                print(f'\n-----\nLa stringa "{value}" non è un JSON\n-----\n')

            final_msg = '{}{}{}Key: {}\n{}{}'.format(
                'Topic: ',
                message.topic,
                '\n\n',
                message.key,
                '\n',
                value,
            )

            # Invia la richiesta per l'invio della mail
            self.send(final_msg)

            print()  # Per spaziare i messaggi sulla shell

    @abstractmethod
    def send(self, msg: dict):
        """Invia il messaggio all'utente finale."""
        pass

    @staticmethod
    def prettyprint(obj: dict):
        """Restituisce una stringa con una formattazione migliore da un
        oggetto JSON (Webhook).

        Arguments:
        obj -- JSON object
        """

        # Questa chiamata va bene sia per i webhook di rd che per gt
        res = "".join(
            [
                f'*Provenienza*: {obj["type"]}'
                '\n\n*È stata aperta una issue nel progetto*: '
                f'{obj["project_name"]} ',
                f'({obj["project_id"]})',
                f'\n\n*Author*: {obj["author"]}'
                '\n\n *Issue\'s information: *'
                f'\n - *Title*: \t\t{obj["title"]}',
                f'\n - *Description*: \t\t{obj["description"]}',
                f'\n - *Action*: \t{obj["action"]}',
                '\n\n*Assegnee\'s information:*'
            ]
        )

        # Avendo gitlab che può avere più assignees e redmine
        # che invece può averne soltanto uno
        # hanno due profondità diverse nel file json,
        # quindi vanno scorse in modo diverso
        if obj["type"] == 'redmine':
            res += f'\n - {obj["assignees"]["firstname"]}'
        elif obj["type"] == 'gitlab':
            for value in obj["assignees"]:
                res += f'\n - {value["name"]}'

        return res
