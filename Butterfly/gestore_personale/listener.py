"""
File: listener.py
Data creazione: 2019-03-28

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
Creatore: Samuele Gardin, samuelegardin1997@gmail.com
Autori:

"""
import telepot

token = "767404683:AAF6Fo4LP7wDWYmEbIRQ37KTX5GECMoTziA"


class BotListener:

    def __init__(self, bot: telepot.Bot):
        self._bot = bot

    def listen(self):
        self._bot.message_loop(self._on_chat_message)
        try:
            print(' Listening to messages...')
            while True:
                pass
        except KeyboardInterrupt:
            print(' Closing listener...')

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


if __name__ == '__main__':
    listener = BotListener(telepot.Bot(token))
    listener.listen()
