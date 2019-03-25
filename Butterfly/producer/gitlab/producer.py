"""
File: gitlab_producer.py
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

Versione: 0.3.1
Creatore: Timoty Granziero, timoty.granziero@gmail.com
Autori:
    Laura Cameran, lauracameran@gmail.com
    Samuele Gardin, samuelegardin@gmail.com
"""

import json
from pathlib import Path
import pprint
from sys import stderr

from flask import Flask
from flask import request
from kafka import KafkaProducer
import kafka.errors

from producer.producer import Producer
# from webhook.gitlab.GLIssueWebhook import GLIssueWebhook


class GitlabProducer(Producer):

    def __init__(
                self,
                kafkaProducer: KafkaProducer,
                webhook_factory: WebhookFactory,
            ):

        self._webhook_factory = webhook_factory
        self._producer = kafkaProducer

    def produce(self, whook: dict):
        """Produce il messaggio in Kafka.

        Arguments:
        topic -- il topic dove salvare il messaggio.
        whook -- il file json
        """

        webhook = self._webhook_factory.createWebhook(whook['object_kind'])

        # Parse del JSON associato al webhook ottenendo un oggetto Python
        webhook = webhook.parse(whook)
        
        try:
            # Inserisce il messaggio in Kafka, serializzato in formato JSON
            self.producer.send(webhook['app'], webhook)
            self.producer.flush(10)  # Attesa 10 secondi
        # Se non riesce a mandare il messaggio in 10 secondi
        except kafka.errors.KafkaTimeoutError:
            stderr.write('Impossibile inviare il messaggio\n')
            exit(-1)


def main():

    app = FlaskClient.initialize_app()
    app.run()


if __name__ == '__main__':
    main()
