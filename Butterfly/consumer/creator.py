from abc import ABC, abstractmethod
from pathlib import Path
import json

from kafka import KafkaConsumer
import kafka.errors

from consumer.consumer import Consumer


class ConsumerCreator(ABC):

    _config_path = Path(__file__).parents[1] / 'config.json'

    def create(self, configs=_config_path) -> Consumer:
         # Converte stringa 'inf' nel relativo float

        with open(ConsumerCreator._config_path, 'r') as f:
            configs = json.load(f)

        if (configs['consumer_timeout_ms'] is not None
                and configs['consumer_timeout_ms'] == 'inf'):
            configs['consumer_timeout_ms'] = float('inf')

        notify = False
        while True:  # Attende una connessione con il Broker
            try:
                # Il parametro value_deserializer tornerà probabilmente
                # utile successivamente, per ora lasciamo il controllo
                # del tipo a listen()
                kafka_consumer = KafkaConsumer(
                    self.topic,
                    # Deserializza i messaggi dal formato JSON a oggetti Python
                    # value_deserializer=(
                    #   (lambda m: json.loads(m.decode('utf-8'))),
                    **configs,
                )
                break
            except kafka.errors.NoBrokersAvailable:
                if not notify:
                    notify = True
                    print('Broker offline. In attesa di una connessione ...')
            except KeyboardInterrupt:
                print(' Closing Consumer ...')
                # exit(1)
        print('Connessione con il Broker stabilita')

        consumer = self.instantiate(kafka_consumer)
        return consumer

    @abstractmethod
    def instantiate(self, kafka_consumer: KafkaConsumer) -> Consumer:
        pass

    @property
    @abstractmethod
    def topic(self):
        pass


class Server(ABC):
    