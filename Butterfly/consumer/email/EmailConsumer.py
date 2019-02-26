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

Versione: 0.2.0
Creatore: Samuele Gardin, samuelegardin@gmail.com
Autori:
    Matteo Marchiori, matteo.marchiori@gmail.com
    Nicola Carlesso
"""

from kafka import KafkaConsumer
import kafka.errors
import json
from pathlib import Path

import smtplib
import getpass

from consumer.consumer import Consumer
# import webhook.webhook as GLIssueWebhook


class EmailConsumer(Consumer):
    """Implementa Consumer"""

    def __init__(self, topics: list, configs: dict):
        self._receiver = configs['email']['receiver']
        self._subject = configs['email']['subject']
        self._sender = configs['emailSettings']['sender']
        # self._pwd = configs['emailSettings']['pwd']
        self._topics = topics

        configs = configs['kafka']

        # Converte stringa 'inf' nel relativo float
        if (configs['consumer_timeout_ms'] is not None
                and configs['consumer_timeout_ms'] == 'inf'):
            configs['consumer_timeout_ms'] = float('inf')

        notify = False
        while True:  # Attende una connessione con il Broker
            try:
                # Il parametro value_deserializer tornerà probabilmente
                # utile successivamente, per ora lasciamo il controllo
                # del tipo a listen()
                self._consumer = KafkaConsumer(
                    *topics,
                    # Deserializza i messaggi dal formato JSON a oggetti Python
                    # value_deserializer=(
                    #   (lambda m: json.loads(m.decode('utf-8'))),
                    **configs,
                )
                break
            except kafka.errors.NoBrokersAvailable:
                if not notify:
                    notify = True
                    print('Broker offline. In attesa di una connessione ...')
            except KeyboardInterrupt:
                print(' Closing Consumer ...')
                exit(1)
        print('Connessione con il Broker stabilita')

    def send(self, msg: str):
        """Manda il messaggio finale, tramite il server mail,
        all'utente finale.
        """

        with smtplib.SMTP('smtp.gmail.com', 587) as mailserver:
            mailserver.ehlo()
            mailserver.starttls()

            # Autenticazione
            while True:
                try:
                    # Prompt per l'inserimento della psw
                    psw = getpass.getpass(
                        '\nInserisci la password '
                        f'di {self._sender}: '
                    )

                    mailserver.login(self._sender, psw)  # Login al server SMTP
                    break  # Login riuscito

                # Errore di autenticazione, riprova
                except smtplib.SMTPAuthenticationError:
                    print('Email e password non corrispondono.')

                # Interruzione da parte dell'utente della task
                except KeyboardInterrupt:
                    print('\nInvio email annullato. '
                          'In ascolto di altri messaggi ...')
                    return

            text = '\n'.join([
                'From: ' + self._sender,
                'To: ' + self._receiver,
                'Subject: ' + self._subject,
                '',
                ' ',
                msg,
            ])

            try:  # Tenta di inviare la mail
                mailserver.sendmail(self._sender, self._receiver, text)
                print('\nEmail inviata. In ascolto di altri messaggi ...')
            except smtplib.SMTPException:
                print('Errore, email non inviata. '
                      'In ascolto di altri messaggi ...')

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
                # message.partition,
                # message.offset,
                '\n\n',
                message.key,
                '\n',
                value,
            )

            # Invia la richiesta per l'invio della mail
            self.send(final_msg)

            print()  # Per spaziare i messaggi sulla shell

    @classmethod
    def pretty(cls, obj: object):
        """Restituisce una stringa con una formattazione migliore da un
        oggetto JSON (Webhook).

        Arguments:
        obj -- JSON object
        """

        # Questa chiamata va bene sia per i webhook di rd che per gt
        res = "".join(
            [
                f'Provenienza: {obj["type"]}'
                '\n\nE` stata aperta una issue nel progetto: '
                f'{obj["project_name"]} ',
                f'({obj["project_id"]})',
                f'\n\nAuthor: {obj["author"]}'
                '\n\n Issue\'s information: '
                f'\n - Title: {obj["title"]}',
                f'\n - Description: {obj["description"]}',
                f'\n - Action: {obj["action"]}',
                '\n\nAssegnee\'s information:'
            ])

        # Avendo gitlab che può avere più assignees
        # e redmine che invece può averne soltanto uno
        # hanno due profondità diverse nel file json,
        # quindi vanno scorse in modo diverso
        if obj['type'] == 'Redmine':
            res += f'\n - {obj["assignees"]["firstname"]}'
        elif obj['type'] == 'Gitlab':
            for value in obj["assignees"]:
                res += f'\n - {value["name"]}'

        return res

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
        consumer = EmailConsumer(
            topiclst,
            config
        )
    except kafka.errors.KafkaConfigurationError as e:
        print(e.with_traceback())

    try:
        consumer.listen()  # Resta in ascolto del Broker
    except KeyboardInterrupt:
        consumer.close()
        print(' Closing Consumer ...')
