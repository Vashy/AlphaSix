from abc import ABC, abstractmethod
import json

from kafka import KafkaProducer
import kafka.errors

from producer.producer import Producer


class ProducerCreator(ABC):
    """Interfaccia `ProducerCreator`. Un `ProducerCreator` ha il
    compito di inizializzare un `KafkaProducer` concreto.
    """

    @abstractmethod
    def create(self, configs: dict) -> KafkaProducer:
        """Restituisce un'istanza concreta di `KafkaProducer`, inizializzando un

        Parameters:

        `configs`: dizionario contenente le configurazioni per il
        `KafkaProducer`.
        """


class KafkaProducerCreator(ProducerCreator):

    def create(self, configs: dict) -> Producer:
        """Restituisce un'istanza concreta di `KafkaProducer`, inizializzando un

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

        return kafka_producer
