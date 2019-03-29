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
    Samuele Gardin, samuelegardin1997@gmail.com
"""

from abc import ABC, abstractmethod

from kafka import KafkaConsumer
import json


class Consumer(ABC):
    """Interfaccia Consumer"""
    
    def __init__(self, consumer: KafkaConsumer, topic):
        # Configs ...

        self._consumer = consumer
        self._topic = topic

    def prelisten_hook(self):
        """Metodo ridefinibile dalle sotto classi per effettuare
        operazioni prima dell'avvio dell'ascolto dei messaggi.
        """

    def listen(self):
        """Ascolta i messaggi provenienti dai Topic a cui il
        consumer è abbonato.

        Precondizione: i messaggi salvati nel broker devono essere
        in formato JSON, e devono contenere dei campi specifici
        definiti in nel modulo webhook
        """

        print('Listening to messages from topics:')

        print(f'- {self._topic}')
        print()

        self.prelisten_hook()  # Hook!

        # Si mette in ascolto dei messsaggi dal Broker
        for message in self._consumer:
            print(f'Tipo messaggio: {type(message.value)}')

            value = message.value.decode('utf-8')
            try:
                value = self.prettyprint(json.loads(value))
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

            # Invia il messaggio al destinatario finale
            self.send(final_msg)

            print()  # Per spaziare i messaggi sulla shell

    @abstractmethod
    def send(self, msg: dict):
        """Invia il messaggio all'utente finale."""
        pass

    def prettyprint(self, obj: dict):
        """Restituisce una stringa con una formattazione migliore da un
        oggetto JSON (Webhook).

        Arguments:
        obj -- JSON object
        """

        # Questa chiamata va bene sia per i webhook di rd che per gt
        res = "".join(
            [
                f'{self.bold}Provenienza{self.bold}: {obj["type"]}'
                f'\n\n{self.bold}È stata aperta una issue nel progetto{self.bold}: '
                f'{obj["project_name"]} ',
                f'({obj["project_id"]})',
                f'\n\n{self.bold}Author{self.bold}: {obj["author"]}'
                f'\n\n {self.bold}Issue\'s information: {self.bold}'
                f'\n - {self.bold}Title{self.bold}: \t\t{obj["title"]}',
                f'\n - {self.bold}Description{self.bold}: \t\t{obj["description"]}',
                f'\n - {self.bold}Action{self.bold}: \t{obj["action"]}',
                f'\n\n{self.bold}Assegnee\'s information:{self.bold}'
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

    @property
    @abstractmethod
    def bold(self):
        pass
