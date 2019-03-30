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

import json
from pathlib import Path

from kafka import KafkaConsumer
import requests

from consumer.consumer import Consumer


class TelegramConsumer(Consumer):
    """Implementa Consumer"""
    _CONFIG_PATH = Path(__file__).parent / 'config.json'

    def __init__(self, consumer: KafkaConsumer, topic: str):
        super(TelegramConsumer, self).__init__(consumer, topic)

        with open(self._CONFIG_PATH) as file:
            configs = json.load(file)

        self._token = configs['telegram']['token_bot']

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

        # Da modificare nel file config.json
        # 38883960 Timoty
        # 265266555 Laura
        log = requests.post(
            'https://api.telegram.org/'
            f'bot{self._token}'
            '/sendMessage',
            data={
                'chat_id': receiver,
                'text': msg,
                'parse_mode': 'markdown',
            })
        if log.ok:
            chat = log.json()["result"]["chat"]
            print(f'({log.status_code}) Inviato un messaggio a '
                  f'{chat["username"]} ({chat["id"]})')  # ["result"]["text"]

            return True

        print(f'({log.status_code}) '
              'Errore: il messaggio non è stato inviato')
        return False

    @property
    def bold(self):
        return '*'

    @property
    def emph(self):
        return '`'

    def close(self):
        """Chiude la connessione del Consumer"""
        self._consumer.close()
