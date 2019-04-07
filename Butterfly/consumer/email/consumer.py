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
Creatore: Samuele Gardin, samuelegardin1997@gmail.com
Autori:
    Matteo Marchiori, matteo.marchiori@gmail.com
    Nicola Carlesso
"""

from pathlib import Path
import json
import smtplib
from email.message import EmailMessage
import os

from kafka import KafkaConsumer

from consumer.consumer import Consumer


class EmailConsumer(Consumer):
    """Implementa Consumer"""

    _CONFIG_PATH = Path(__file__).parent / 'config.json'

    def __init__(self, consumer: KafkaConsumer):
        super(EmailConsumer, self).__init__(consumer)

        with open(self._CONFIG_PATH) as file:
            configs = json.load(file)
        self._sender = configs['email']['sender']

    def send(self, receiver: str, mail_text: str):
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
                    # psw = getpass.getpass(
                    #     '\nInserisci la password '
                    #     f'di {self._sender}: '
                    # )

                    psw = os.environ['BUTTERFLY_EMAIL_PSW']
                    print(self._sender, psw)
                    mailserver.login(self._sender, psw)  # Login al server SMTP
                    break  # Login riuscito, e Filè incacchiato

                # Errore di autenticazione, riprova
                except smtplib.SMTPAuthenticationError:
                    print('Email e password non corrispondono.')

                # Interruzione da parte dell'utente della task
                except KeyboardInterrupt:
                    print('\nInvio email annullato. '
                          'In ascolto di altri messaggi ...')
                    return

            msg = EmailMessage()
            msg['Subject'] = 'lul'
            msg['From'] = self._sender
            msg['To'] = receiver
            msg.set_content(self.format(mail_text))
            msg.add_alternative(f"""\
<html>
    <body>
        {self.format_html(mail_text)}
    </body>
</html>
                """, subtype='html')

            try:  # Tenta di inviare l'Email
                mailserver.send_message(msg)
                print('\nEmail inviata. In ascolto di altri messaggi ...')
            except smtplib.SMTPException:
                print('Errore, email non inviata. '
                      'In ascolto di altri messaggi ...')
            finally:
                mailserver.quit()

    def format(self, msg):
        """Restituisce una stringa con una formattazione migliore da un
        oggetto JSON (Webhook).
        """
        res = ''
        res = self._preamble(msg['object_kind'])

        res += ''.join([
            f' nel progetto {msg["project_name"]} ',
            f'({msg["project_id"]})',
            f'\n\nSorgente: {msg["app"].capitalize()}',
            f'\nAutore: {msg["author"]}'
            f'\n\n Information: '
            f'\n - Title: \t\t{msg["title"]}',
            f'\n - Description: \n'
            f'  {msg["description"]}',
            f'\n - Action: \t{msg["action"]}'
        ])

        return res

    def format_html(self, msg):
        """Restituisce una stringa in formato HTML da un
        oggetto JSON.
        """
        res = '<p>'

        res += self._preamble(msg['object_kind'])

        res += ''.join([
            f' nel progetto <strong>{msg["project_name"]}</strong> ',
            f'(<code>{msg["project_id"]}</code>)</p>',
            '<ul>'
            f'<li><strong>Sorgente:</strong> {msg["app"].capitalize()}</li>',
            f'<li><strong>Autore:</strong> {msg["author"]}</li>'
            f'<li><strong>Title:</strong> {msg["title"]}</li>',
            f'<li><strong>Description:</strong> '
            f'{msg["description"]}</li>',
            f'<li><strong>Action:</strong> {msg["action"]}</li>'
            '</ul>'
        ])
        return res

    def _preamble(self, field):
        """Preambolo del messaggio.
        """

        res = ''
        if field == 'issue':
            res += 'È stata aperta una issue '

        elif field == 'push':
            res += 'È stata fatto un push '

        elif field == 'issue-note':
            res += 'È stata commentata una issue '

        elif field == 'commit-note':
            res += 'È stato commentato un commit '

        else:
            raise KeyError

        return res
