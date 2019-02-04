import sys
from kafka import KafkaProducer
import kafka.errors
from abc import ABC, abstractmethod
import configparser


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
    def __init__(self, servers: str):
        self._producer = KafkaProducer(bootstrap_servers=servers)

    def __del__(self):
        self.close()

    @property
    def producer(self):
        """Restituisce il Producer"""
        return self._producer

    def produce(self, topic: str, msg: str):
        try:
            self.producer.send(topic, msg.encode())
            self.producer.flush(10) # 10 secondi
        except kafka.errors.KafkaTimeoutError:
            sys.stderr.write("Errore di timeout\n")
            exit(-1)

    def close(self):
        """Rilascia il Producer associato"""
        self._producer.close()


if __name__ == '__main__':
    # Inizializza il ConfigParser
    config = configparser.ConfigParser()
    config.read('Butterfly/butterfly/config.ini')

    # Legge i dati dal file config.ini
    server = config["DEFAULT"]["server"]
    port = config["DEFAULT"]["port"]
    topic = config["DEFAULT"]["topic"]

    # Istanzia il producer
    producer = ConsoleProducer('{}:{}'.format(server, port))
    for msg in sys.argv[1:]: # Genera i messaggi degli argomenti passati a linea di comando
        producer.produce(topic, msg)
