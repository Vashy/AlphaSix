#!/usr/bin/env python3

# Uso: python3 path/to/consumer.py

from kafka import KafkaConsumer
import kafka.errors
from abc import ABC, abstractmethod
import json
from pathlib import Path

class Consumer(ABC):
    """Interfaccia Consumer"""

    @abstractmethod
    def listen(self):
        """Resta in ascolto del Broker"""
        pass


class ConsoleConsumer(Consumer):
    """Implementa Consumer"""

    def __init__(self, topics: list, configs: dict):

        # Converte stringa 'inf' nel relativo float
        if configs["consumer_timeout_ms"] == "inf":
            configs["consumer_timeout_ms"] = float("inf")
        self._consumer = KafkaConsumer(*topics, **config)

    def listen(self):
        """Ascolta i messaggi provenienti dai Topic a cui il consumer è
        abbonato.
        Precondizione: i messaggi devono essere codificati in binario.
        """
        for message in self._consumer:
            print ("{}:{}:{}:\tkey={}\tvalue={}".format(
                    message.topic,
                    message.partition,
                    message.offset,
                    message.key,
                    message.value.decode()
                )
            )

    @property
    def consumer(self):
        """Restituisce il KafkaConsumer"""
        return self._consumer

    def close(self):
        """Chiude la connessione del Consumer"""
        self._consumer.close()

class WebhookConsumer(Consumer):
    """Implementa Consumer"""

    def __init__(self, topics: list, configs: dict):
        # Converte stringa 'inf' nel relativo float
        if configs["consumer_timeout_ms"] == "inf":
            configs["consumer_timeout_ms"] = float("inf")

        self._consumer = KafkaConsumer(
            *topics,
            # Deserializza i messaggi dal formato JSON a oggetti Python
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            **config
        )

    def listen(self):
        """Ascolta i messaggi provenienti dai Topic a cui il
        consumer è abbonato.

        Precondizione: i messaggi salvati nel broker devono essere
        in formato JSON, e devono contenere dei campi specifici
        definiti in nel modulo webhook
        """
        for message in self._consumer:
            print ("{}:{}:{}:\tkey={}\n{}".format(
                    message.topic,
                    message.partition,
                    message.offset,
                    message.key,
                    self.pretty(message.value),
                )
            )
            # La versione con format è più carina
            # print (f"{message.topic}:{message.partition}:{message.offset}:"
            #     "\tkey={message.key}\n{self.pretty(message.value)}")

    def pretty(self, obj: object):
        """Restituisce una stringa con una formattazione migliore da un
        oggetto JSON (Webhook).

        Arguments:
        obj -- JSON object
        """

        res = ""
        return "".join(
            [
                res, f'Type: \t\t{obj["object_kind"]}',
                res, f'\nTitle: \t\t{obj["title"]}',
                res, f'\nProject ID: \t{obj["project"]["id"]}',
                res, f'\nProject name: \t{obj["project"]["name"]}',
                res, f'\nAction: \t{obj["action"]}\n ... ',
            ]
        )


    def close(self):
        """Chiude la connessione del Consumer"""
        self._consumer.close()


if __name__ == '__main__':

    """Fetch dei topic dal file topics.json
    Campi:
    - topics['id']
    - topics['label']
    - topics['project']
    """
    with open(Path(__file__).parent / 'topics.json') as f:
        topics = json.load(f)

    # Fetch delle configurazioni dal file config.json
    with open(Path(__file__).parent / 'config.json') as f:
        config = json.load(f)
    config = config['consumer']

    # Per ora, sono solo di interesse i nomi (label) dei Topic
    topiclst = []
    for topic in topics:
        # Per ogni topic, aggiunge a topiclst solo se non è già presente 
        if topic['label'] not in topiclst:
            topiclst.append(topic['label'])

    # Inizializza WebhookConsumer
    consumer = WebhookConsumer(
        topiclst, 
        config 
    )

    try:
        consumer.listen() # Resta in ascolto del Broker
    except KeyboardInterrupt as e:
        consumer.close()
        print(' Closing Consumer ...')
