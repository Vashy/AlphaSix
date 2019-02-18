#!/usr/bin/env python3


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
# from webhook.webhook import Webhook


class ConsoleProducer(Producer):
    def __init__(self, config):
        self._producer = KafkaProducer(**config)

    def __del__(self):
        self.close()

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
            self.producer.flush(10) # Attende 10 secondi
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
    with open(Path(__file__).parent.parent / 'topics.json') as f:
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
