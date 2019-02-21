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

Versione: 0.1.0
Creatore: Laura Cameran, lauracameran@gmail.com
Autori:
    <nome cognome, email>
    <nome cognome: email>
    ....
"""

# Posizione: Butterfly/
# Uso: python3 -m path.to.GLProducer

import argparse
from sys import stderr
from kafka import KafkaProducer
import kafka.errors
import json
from pathlib import Path
from producer.producer import Producer
from webhook.redmine.RedmineIssueWebhook import RedmineIssueWebhook
# from redminelib import Redmine


class RedmineProducer(Producer):

    def __init__(self, config):   # COSTRUTTORE
        self._producer = KafkaProducer(
            # Serializza l'oggetto Python in un oggetto JSON, codifica UTF-8
            value_serializer=lambda m: json.dumps(m).encode('utf-8'),
            **config
        )

    #def __del__(self):  # DISTRUTTORE
    #    self.close()

    @property
    def producer(self):
        """Restituisce il KafkaProducer"""
        return self._producer

    def produce(self, topic, msg: RedmineIssueWebhook):
        """Produce il messaggio in Kafka.
        Precondizione: msg è di tipo RedmineIssueWebhook

        Arguments:
        topic -- il topic dove salvare il messaggio.
        """
        # Può mai accadere false??
        assert isinstance(msg, RedmineIssueWebhook), \
            'msg non è di tipo RedmineIssueWebhook'

        # Parse del JSON associato al webhook ottenendo un oggetto Python
        msg.parse()
        try:
            print()
            # Inserisce il messaggio in Kafka, serializzato in formato JSON
            self.producer.send(topic, msg.webhook())
            self.producer.flush(10)   # Attesa 10 secondi
        except kafka.errors.KafkaTimeoutError:
            stderr.write('Errore di timeout\n')
            exit(-1)

    #def close(self):
    #    """Rilascia il Producer associato"""
    #    self._producer.close()


def main():

    # Configurazione da config.json
    with open(Path(__file__).parents[1] / 'config.json') as f:
        config = json.load(f)

    """Fetch dei topic dal file topics.json
    Campi:
    - topics['id']
    - topics['label']
    - topics['project']
    """
    with open(Path(__file__).parents[2] / 'topics.json') as f:
        topics = json.load(f)

    # Istanzia il Producer
    producer = RedmineProducer(config)

    # Parsing dei parametri da linea di comando
    parser = argparse.ArgumentParser(description='Crea messaggi su Kafka')
    parser.add_argument('-t', '--topic', type=str,
                        help='topic di destinazione')
    args = parser.parse_args()

    # Inzializza RedmineIssueWebhook con il percorso
    # a open_issue_redmine_webhook.json
    webhook = RedmineIssueWebhook(
            Path(__file__).parents[2] / 'webhook/redmine/open_issue_redmine_webhook.json')

    # print(topics[0]['label'])
    if args.topic:  # Topic passato con la flag -t
        producer.produce(args.topic, webhook)
    else:  # Prende come Topic di default il primo del file webhook.json
        producer.produce(topics[0]['label'], webhook)


if __name__ == '__main__':
    main()
