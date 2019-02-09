#!/usr/bin/env python3

# Uso: python3 path/to/producer.py -t nometopic msg1 "messaggio lungo 2" msg3

import argparse
from sys import stderr
from kafka import KafkaProducer
import kafka.errors
from abc import ABC, abstractmethod
import json
from pathlib import Path


class Producer(ABC):
    """Interfaccia Producer"""

    @abstractmethod
    def produce(self, topic: str, msg: str):
        """Produce il messaggio `msg` nel topic designato del broker"""
        pass

    @abstractmethod
    def close(self):
        """Chiude il Producer"""
        pass


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
            self.producer.send(topic, msg.encode())
            self.producer.flush(10) # 10 secondi
        except kafka.errors.KafkaTimeoutError:
            stderr.write("Errore di timeout\n")
            exit(-1)
        
    def close(self):
        """Rilascia il Producer associato"""
        self._producer.close()


def produce_messages(console_producer, topic):
    """Genera i messaggi degli argomenti passati a linea di comando"""
    for msg in args.message:
        producer.produce(topic, msg)




if __name__ == '__main__':

    # Configurazione da config.json
    with open(Path(__file__).parent / 'config.json') as f:
        config = json.load(f)
    config = config["producer"]

    # Fetch della lista dei topic da topics.json
    with open(Path(__file__).parent / 'topics.json') as f:
        topics = json.load(f)

    # Istanzia il Producer
    producer = ConsoleProducer(config)
    
    parser = argparse.ArgumentParser(description="Crea messaggi su Kafka")
    parser.add_argument("-t", "--topic", type=str,
                        help="topic di destinazione")
    parser.add_argument("message", type=str, nargs="+",
                        help="crea messaggi su Kafka")
    args = parser.parse_args()

    # Produce i messaggi nel topic passato come argomento
    if args.topic:
        produce_messages(ConsoleProducer, args.topic)
    else:
        produce_messages(ConsoleProducer, topics["topics"][0])
