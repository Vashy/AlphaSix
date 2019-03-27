from abc import ABC, abstractmethod
from pathlib import Path
import json

from kafka import KafkaProducer
import kafka.errors

from producer.producer import Producer


class ProducerCreator(ABC):
    """Interfaccia `ProducerCreator`. Un `ProducerCreator` ha il
    compito di inizializzare un `Producer` concreto.
    """

    def create(self, configs: dict) -> Producer:
        """Restituisce un'istanza concreta di `Producer`, inizializzando un
        `KafkaProducer` e passandolo come parametro al `Producer`

        Parameters:

        `configs`: dizionario contenente le configurazioni per il
        `KafkaProducer`.
        """

        notify = False
        while True:  # Attende una connessione con il Broker
            try:
                kafka_producer = KafkaProducer(
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

        producer = self.instantiate(kafka_producer)
        return producer

    @abstractmethod
    def instantiate(self, kafka_producer: KafkaProducer) -> Producer:
        """Istanzia il `Producer` concreto, che adatta `KafkaProducer`
        all'interfaccia `Producer`, e lo restituisce"""


class ServerCreator(ABC):
    """Interfaccia `ServerCreator`. Inizializza il server."""
    @abstractmethod
    def initialize_app(self, topic: str, config_path: Path):
        """Restituisce il `Server` inizializzato"""
