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

    def __init__(self, consumer: KafkaConsumer):
        super(TelegramConsumer, self).__init__(consumer)

        with open(self._CONFIG_PATH) as file:
            configs = json.load(file)
        self._token = configs['telegram']['token_bot']

    def send(self, receiver: str, msg: dict) -> bool:
        """Manda il messaggio finale, tramite il bot,
        all'utente finale.
        """

        # Richiesta POST per l'invio del messaggio finale
        # via Telegram API
        response = requests.post(
            'https://api.telegram.org/'
            f'bot{self._token}'
            '/sendMessage',
            data={
                'chat_id': receiver,
                'text': self.format(msg),
                'parse_mode': 'markdown',
            })
        if response.ok:
            chat = response.json()["result"]["chat"]
            print(f'({response.status_code}) Inviato un messaggio a '
                  f'{chat["username"]} ({chat["id"]})')

            return True

        print(f'({response.status_code}) '
              'Errore: il messaggio non è stato inviato')
        return False

    def format(self, msg: dict):
        """Restituisce una stringa con una formattazione migliore da un
        oggetto JSON (Webhook).

        Arguments:
        msg -- JSON object

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

        # Queste chiamate vanno bene sia per i webhook di rd che per gt

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

        emph = '`'
        bold = '**'

        res += ''.join([
            f' nel progetto {bold}{msg["project_name"]}{bold} ',
            f'({emph}{msg["project_id"]}{emph})',
            f' su {msg["app"].capitalize()}',
            f'\n\n{bold}Informazioni:{bold} '
            f'\n - {bold}Autore:{bold} {msg["author"]}'
            f'\n - {bold}Title:{bold} {msg["title"]}',
            f'\n - {bold}Description:{bold}\n'
            f'  {msg["description"]}',
            f'\n - {bold}Action:{bold} {msg["action"]}'
        ])

        return res
