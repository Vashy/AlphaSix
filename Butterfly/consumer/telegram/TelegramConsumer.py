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
    Samuele Gardin, samuelegardin@gmail.com
"""

from kafka import KafkaConsumer
import kafka.errors
import telepot
from pathlib import Path
import json
import pprint  # Pretty format per oggetti Python

from consumer.consumer import Consumer
# import webhook.webhook as GLIssueWebhook
# from webhook.redmine.RedmineIssueWebhook import RedmineIssueWebhook


class TelegramConsumer(Consumer):
    """Implementa Consumer"""

    def __init__(self, topics: list, configs: dict):

        self._receiver = configs['telegram']['receiver']
        self._topics = topics

        # Converte stringa 'inf' nel relativo float
        if (configs['kafka']['consumer_timeout_ms'] is not None
                and configs['kafka']['consumer_timeout_ms'] == 'inf'):
            configs['kafka']['consumer_timeout_ms'] = float('inf')

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
                    #   lambda m: json.loads(m.decode('utf-8'))),
                    **configs['kafka'],
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

        self._bot = telepot.Bot(configs['telegram']['token_bot'])

    def send(self, msg: str):
        """Manda il messaggio finale, tramite il bot,
        all'utente finale.

        Formato: Markdown
        *bold text*
        _italic text_
        [inline URL](http://www.example.com/)
        [inline mention of a user](tg://user?id=123456789)
        `inline fixed-width code`
        ```block_language
        pre-formatted fixed-width code block
        ```
        """
        # Warn se l'ID del destinatario non esiste,
        # e non invia nessun messaggio
        try:
            log = self._bot.sendMessage(
                self._receiver,
                msg,
                parse_mode='markdown',
            )
            if log:
                print(f'Inviato il messaggio:\n{pprint.pformat(log)}')
            else:
                print('Errore: il messaggio non è stato inviato')
        except telepot.exception.TelegramError as e:
            print(f'Nessun messaggio inviato: "{e.description}"')

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

        # Linea da commentare in caso qualcun altro abbia attivo il bot
        self._bot.message_loop(self._on_chat_message)
        for message in self._consumer:
            print(f'Tipo messaggio: {type(message.value)}')

            value = message.value.decode('utf-8')
            try:
                value = self.pretty(json.loads(value))
            except json.decoder.JSONDecodeError:
                print(f'\n-----\nWarning: "{value}"'
                      'non è in formato JSON\n-----\n')

            final_msg = '{}{}{}*Key*: {}\n{}{}'.format(
                    '*Topic*: ',
                    message.topic,
                    # message.partition,
                    # message.offset,
                    '\n\n',
                    message.key,
                    '\n',
                    value,
            )

            # Invia il messaggio finale
            self.send(final_msg)

            print()  # Per spaziare i messaggi sulla shell

    def _on_chat_message(self, msg):
        # Raccoglie il messaggio
        content_type, _, chat_id = telepot.glance(msg)

        if content_type == 'text':

            # Debug info
            print('ID utente: ', chat_id)

            name = msg['from']['first_name']
            print('Nome utente: ', name)

            text = msg['text']
            print('Testo messaggio: ', text)
            print('-----------')

            final_msg = ''
            if text == '/start':
                final_msg = (
                    f'Ciao {name}, '
                    'questo è il bot che ti invierà '
                    'le segnalazioni dei topic ai quali ti sei iscritto.'
                )

            elif text == '/subscribe':  # TODO Comando /subscribe
                final_msg = (
                    f'{name}, sei stato aggiunto correttamente '
                    'al sistema *Butterfly*!'
                )

            elif text == '/unsubscribe':  # TODO Comando /unsubscribe
                final_msg = (
                    'Sei stato rimosso '
                    'dal sistema *Butterfly*! Se cambiassi idea, '
                    'fammelo sapere!'
                )
            else:
                final_msg = (
                    'Comando non riconosciuto.\n\nUso:\n'
                    '/subscribe\n/unsubscribe'
                )

            self._bot.sendMessage(
                    chat_id,
                    final_msg,
                    parse_mode='markdown',
            )

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
        if obj["type"] == 'Redmine':
            res += f'\n - {obj["assignees"]["firstname"]}'
        elif obj["type"] == 'Gitlab':
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
        consumer = TelegramConsumer(
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
