"""
File: ConsoleProducer.py
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
    <nome cognome, email>
    <nome cognome: email>
    ....
"""

# Posizione: Butterfly/
# Uso: python3 -m path.to.ConsoleProducer -t nometopic
# Uso: python3 -m path.to.ConsoleProducer

import argparse
from sys import stderr
from kafka import KafkaProducer
import kafka.errors
from producer.producer import Producer
import json
from pathlib import Path


class ConsoleProducer(Producer):
    def __init__(self, config):
        notify = False
        while True:  # Attende una connessione con il Broker
            try:
                self._producer = KafkaProducer(**config)
                break
            except kafka.errors.NoBrokersAvailable:
                if not notify:
                    notify = True
                    print('Broker offline. In attesa di una connessione ...')
            except KeyboardInterrupt:
                print(' Closing Producer ...')
                exit(1)
        print('Connessione con il Broker stabilita')

    @property
    def producer(self):
        """Restituisce il KafkaProducer"""
        return self._producer

    def produce(self, topic: str, msg: str):
        """Produce il messaggio in Kafka"""
        try:
            # Produce il messaggio sul Broker, codificando la
            # stringa in binario
            self.producer.send(topic, msg.encode())
            self.producer.flush(10)  # Attende 10 secondi
        except kafka.errors.KafkaTimeoutError:
            stderr.write('Errore di timeout\n')
            exit(-1)

    def close(self):
        """Rilascia il Producer associato"""
        self._producer.close()


# Funzione ausiliaria per ConsoleProducer
def produce_messages(console_producer, topic, messages):
    """Genera i messaggi degli argomenti passati a linea di comando"""
    for msg in messages:
        console_producer.produce(topic, msg)


def main():

    # Configurazione da config.json
    with open(Path(__file__).parent / 'config.json') as f:
        config = json.load(f)

    """Fetch dei topic dal file topics.json
    Campi:
    - topics['id']
    - topics['label']
    - topics['project']
    """

    with open(Path(__file__).parents[1] / 'topics.json') as f:
        topics = json.load(f)

    # Istanzia il Producer
    producer = ConsoleProducer(config)
    # producer = WebhookProducer(config)

    # Parsing dei parametri da linea di comando
    parser = argparse.ArgumentParser(description='Crea messaggi su Kafka')
    parser.add_argument('-t', '--topic', type=str,
                        help='topic di destinazione')
    parser.add_argument('message', type=str, nargs='+',
                        help='crea messaggi su Kafka')
    args = parser.parse_args()

    # Produce i messaggi nel topic passato come argomento
    if args.topic:
        produce_messages(producer, args.topic, args.message)
    else:
        produce_messages(producer, topics[0]['label'], args.message)


if __name__ == "__main__":
    main()
