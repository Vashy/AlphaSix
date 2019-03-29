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

# Posizione: Butterfly/
# Uso: python3 -m path.to.WebhookConsumer

from kafka import KafkaConsumer

import smtplib

from consumer.consumer import Consumer


class EmailConsumer(Consumer):
    """Implementa Consumer"""

    def __init__(self, consumer: KafkaConsumer, topic: str):
        # self._sender = configs['emailSettings']['sender']
        super(EmailConsumer, self).__init__(consumer, topic)

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
                    # psw = getpass.getpass(
                    #     '\nInserisci la password '
                    #     f'di {self._sender}: '
                    # )

                    mailserver.login(self._sender, 'VOLEVI')  # Login al server SMTP
                    break  # Login riuscito, e Filè incacchiato

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

            try:  # Tenta di inviare l'Email
                mailserver.sendmail(self._sender, self._receiver, text)
                print('\nEmail inviata. In ascolto di altri messaggi ...')
            except smtplib.SMTPException:
                print('Errore, email non inviata. '
                      'In ascolto di altri messaggi ...')

    def bold(self):
        return ''

    def close(self):
        """Chiude la connessione del Consumer"""
        self._consumer.close()
