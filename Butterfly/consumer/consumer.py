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
            # print(f'Tipo messaggio: {type(message.value)}')

            value = message.value.decode('utf-8')
            try:
                receiver, value = self.format(json.loads(value))
                # Invia il messaggio al destinatario finale
                self.send(receiver, value)
                print()  # Per spaziare i messaggi sulla shell
            except json.decoder.JSONDecodeError:
                print(f'\n-----\nLa stringa "{value}" non è un JSON\n-----\n')
            except KeyError:
                print('Errore nella formattazione del messaggio finale')

            # final_msg = '{}{}{}Key: {}\n{}{}'.format(
            #     'Topic: ',
            #     message.topic,
            #     '\n\n',
            #     message.key,
            #     '\n',
            #     value,
            # )


    @abstractmethod
    def send(self, receiver: str, msg: dict):
        """Invia il messaggio all'utente finale."""

    def format(self, msg: dict):
        """Restituisce una stringa con una formattazione migliore da un
        oggetto JSON (Webhook).

        Arguments:
        msg -- JSON object
        """
        # Queste chiamate vanno bene sia per i webhook di rd che per gt

        bold = self.bold
        res = f'{bold}Provenienza{bold}: {msg["app"]}'

        if msg['object_kind'] == 'issue':
            res += f'\n\n{bold}È stata aperta una issue nel progetto{bold}: '

        elif msg['object_kind'] == 'push':
            res += f'\n\n{bold}È stata fatto un push nel progetto{bold}: '

        elif msg['object_kind'] == 'issue-note':
            res += f'\n\n{bold}È stata commentata una issue nel progetto{bold}: '

        elif msg['object_kind'] == 'commit-note':
            res += f'\n\n{bold}È stato commentato un commit nel progetto{bold}: '

        res += "".join(
            [
                f'{msg["project_name"]} ',
                f'({msg["project_id"]})',
                f'\n\n{bold}Author{bold}: {msg["author"]}'
                f'\n\n {bold}Information: {bold}'
                f'\n - {bold}Title{bold}: \t\t{msg["title"]}',
                f'\n - {bold}Description{bold}: \
                    \t\t{msg["description"]}',
                f'\n - {bold}Action{bold}: \t{msg["action"]}'
            ]
        )

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
