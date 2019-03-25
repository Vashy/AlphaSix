from abc import ABC, abstractmethod

from kafka import KafkaProducer
import kafka.errors

from producer.producer import Producer
from producer.server import Server


class ProducerCreator(ABC):

    def create(self, configs: dict) -> Producer:
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
        pass


class ServerCreator(ABC):
    @abstractmethod
    def initialize_app(self, application, config_path) -> Server:
        pass
