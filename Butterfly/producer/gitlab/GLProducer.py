"""
File: GLProducer.py
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
from abc import ABC, abstractmethod

from flask import Flask
from flask import request
from kafka import KafkaProducer
import kafka.errors

from producer.producer import Producer
# from webhook.gitlab.GLIssueWebhook import GLIssueWebhook


class ProducerCreator(ABC):
    @abstractmethod
    def create(self, configs) -> Producer:
        pass


class GitlabProducerCreator(ProducerCreator):
    """Assembler per GitlabProducer
    """
    def create(self, configs) -> Producer:
        notify = False
        while True:  # Attende una connessione con il Broker
            try:
                kafkaProducer = KafkaProducer(
                    # Serializza l'oggetto Python in un
                    # oggetto JSON, codifica UTF-8
                    value_serializer=lambda m: json.dumps(m).encode('utf-8'),
                    **configs
                )
                break
            except kafka.errors.NoBrokersAvailable:
                if not notify:
                    notify = True
                    print('Broker offline. In attesa di una connessione ...')
            except KeyboardInterrupt:
                print(' Closing Producer ...')
                exit(1)
        print('Connessione con il Broker stabilita')

        # Istanzia il Producer
        producer = GLProducer(kafkaProducer)
        return producer


class FlaskClient:  # FlaskClient
    def __init__(self, flask: Flask, producer: Producer):
        self._app: Flask = flask
        self._producer: Producer = producer

    @property
    def app(self) -> Flask:
        return self._app

    @app.route('/', methods=['GET', 'POST'])
    def api_root(self):

        if request.headers['Content-Type'] == 'application/json':

            """Fetch dei topic dal file topics.json
            Campi:
            - topics['id']
            - topics['label']
            - topics['project']
            """

            webhook = request.get_json()
            print(
                '\n\n\nMessaggio da GitLab:\n'
                f'{pprint.pformat(webhook)}\n\n\n'
                'Parsing del messaggio ...'
            )

            try:
                self._producer.produce(webhook)
                print('Messaggio inviato.\n\n')
            except KeyError:
                print('Warning: messaggio malformato. '
                      'Non è stato possibile effettuare il parsing.\n'
                      'In attesa di altri messaggi...\n\n')

            return '', 200

        else:
            return '', 400

    def run(self):
        self.app.run(
            host=self.config['gitlab']['ip'],
            port=self.config['gitlab']['port']
        )

    @staticmethod
    def initialize_app():
        configs = _open_configs(Path(__file__).parents[1] / 'config.json')

        flask = Flask(__name__, configs['gitlab'])

        creator = GitlabProducerCreator()
        producer = creator.create(configs['kafka'])  # O senza il campo

        app = FlaskClient(flask, producer)
        return app


class GLProducer(Producer):

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
            self.producer.send('gitlab', webhook)
            self.producer.flush(10)  # Attesa 10 secondi
        # Se non riesce a mandare il messaggio in 10 secondi
        except kafka.errors.KafkaTimeoutError:
            stderr.write('Errore di timeout\n')
            exit(-1)


def _open_configs(path: Path):
    with open(path) as f:
        config = json.load(f)
    return config


def main():

    app = FlaskClient.initialize_app()
    app.run()


if __name__ == '__main__':
    main()
