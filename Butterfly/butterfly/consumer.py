#!/usr/bin/env python3

import sys
from kafka import KafkaConsumer
import kafka.errors
from abc import ABC, abstractmethod
import json
from pathlib import Path

class Consumer(ABC):
    """Interfaccia Consumer"""

    @abstractmethod
    def listen(self):
        pass

    @abstractmethod
    def close(self):
        """Chiude il Consumer"""
        pass

class ConsoleConsumer(Consumer):
    """Implementa Consumer"""

    def __init__(self, topics: list, configs: dict):

        # Converte stringa 'inf' nel relativo float
        if configs["consumer_timeout_ms"] == "inf":
            configs["consumer_timeout_ms"] = float("inf")
        self._consumer = KafkaConsumer(*topics, **config)

    def listen(self):
        """Ascolta i messaggi provenienti dai topic a cui il consumer è abbonato"""
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
        self._consumer.close()


if __name__ == "__main__":


    # Fetch dei topic dal file topics.json
    with open(Path(__file__).parent / 'topics.json') as f:
        topics = json.load(f)

    # Fetch delle configurazioni dal file config.json
    with open(Path(__file__).parent / 'config.json') as f:
        config = json.load(f)
    config = config["consumer"]

    consumer = ConsoleConsumer(
        topics["topics"],
        config
    )

    try:
        consumer.listen()
    except KeyboardInterrupt as e:
        print(" Closing Consumer ...")
