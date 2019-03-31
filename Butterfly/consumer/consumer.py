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
import json
from pprint import pprint

from kafka import KafkaConsumer


class Consumer(ABC):
    """Interfaccia Consumer"""

    def __init__(self, consumer: KafkaConsumer, topic: str):

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

        print('Listening to messages from topic:')
        print(f'- {self._topic}')
        print()

        self.prelisten_hook()  # Hook!

        # Si mette in ascolto dei messsaggi dal Broker
        for message in self._consumer:

            value = message.value
            try:
                receiver, value = self.format(value)

                # Invia il messaggio al destinatario finale
                self.send(receiver, value)

            except json.decoder.JSONDecodeError:
                print(f'\n-----\nLa stringa "{value}" non è in formato JSON\n-----\n')
            except Exception:
                print('Errore nella formattazione del messaggio finale')


    @abstractmethod
    def send(self, receiver: str, msg: dict) -> bool:
        """Invia il messaggio all'utente finale."""

    def format(self, msg: dict):
        """Restituisce una stringa con una formattazione migliore da un
        oggetto JSON (Webhook).

        Arguments:
        msg -- JSON object
        """
        # Queste chiamate vanno bene sia per i webhook di rd che per gt

        emph = self.emph
        bold = self.bold

        res = ''

        if msg['object_kind'] == 'issue':
            res += f'È stata aperta una issue '

        elif msg['object_kind'] == 'push':
            res += f'È stata fatto un push '

        elif msg['object_kind'] == 'issue-note':
            res += f'È stata commentata una issue '

        elif msg['object_kind'] == 'commit-note':
            res += f'È stato commentato un commit '

        else:
            raise KeyError

        res += ''.join([
            f'{bold}{msg["project_name"]}{bold} ',
            f'({emph}{msg["project_id"]}{emph})',
            f'\n\n{bold}Sorgente:{bold} {msg["app"]}',
            f'\n{bold}Autore:{bold} {msg["author"]}'
            f'\n\n {bold}Information:{bold} '
            f'\n - {bold}Title:{bold} \t\t{msg["title"]}',
            f'\n - {bold}Description:{bold} \n'
            f'  {msg["description"]}',
            f'\n - {bold}Action:{bold} \t{msg["action"]}'
        ])

        # Avendo gitlab che può avere più assignees e redmine
        # che invece può averne soltanto uno
        # hanno due profondità diverse nel file json,
        # quindi vanno scorse in modo diverso
        # if msg["app"] == 'redmine':
        #     res += f'\n - {msg["assignees"]["firstname"]}'
        # elif msg["app"] == 'gitlab':
        #     for value in msg["assignees"]:
        #         res += f'\n - {value["name"]}'

        return msg['receiver'], res

    @property
    @abstractmethod
    def bold(self):
        pass


    @property
    @abstractmethod
    def emph(self):
        pass
