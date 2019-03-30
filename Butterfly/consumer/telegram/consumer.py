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
    Samuele Gardin, samuelegardin1997@gmail.com
"""

from kafka import KafkaConsumer
import telepot
import pprint

from consumer.consumer import Consumer


# import webhook.webhook as GLIssueWebhook
# from webhook.redmine.RedmineIssueWebhook import RedmineIssueWebhook


class TelegramConsumer(Consumer):
    """Implementa Consumer"""

    def __init__(self, consumer: KafkaConsumer, topic: str, bot: telepot.Bot):
        # super.__init__(topics, configs)

        # self._receiver = configs['telegram']['receiver']

        #
        # self._topic = consumer

        super(TelegramConsumer, self).__init__(consumer, topic)

        self._bot = bot

    def send(self, receiver: str, msg: dict):
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
        # Warna se l'ID del destinatario non esiste,
        # e non invia nessun messaggio
        try:
            # Da modificare nel file config.json
            # 38883960 Timoty
            # 265266555 Laura
            log = self._bot.sendMessage(
                receiver,
                msg,
                parse_mode='markdown',
            )
            if log:
                print(f'Inviato il messaggio:\n{pprint.pformat(log)}')
                return log
            print('Errore: il messaggio non è stato inviato')
            return None
        except telepot.exception.TelegramError as exc:
            print(f'Nessun messaggio inviato: "{exc.description}"')
            return None

    @property
    def bold(self):
        return '*'

    def close(self):
        """Chiude la connessione del Consumer"""
        self._consumer.close()
