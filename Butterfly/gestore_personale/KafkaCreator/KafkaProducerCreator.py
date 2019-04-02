from abc import ABC, abstractmethod
from pathlib import Path
import json

from kafka import KafkaProducer
import kafka.errors


class KafkaProducerCreator(ABC):
    """Interfaccia `ProducerCreator`. Un `ProducerCreator` ha il
    compito di inizializzare un `Producer` concreto.
    """
    _config_path = Path(__file__).parents[1] / 'config_producer.json'

    def create(self, configs=_config_path) -> KafkaProducer:
        """Restituisce un'istanza concreta di `Producer`, inizializzando un
        `KafkaProducer` e passandolo come parametro al `Producer`

        Parameters:

        `configs`: dizionario contenente le configurazioni per il
        `KafkaProducer`.
        """

        with open(KafkaProducerCreator._config_path, 'r') as f:
            configs = json.load(f)

        # if (configs['consumer_timeout_ms'] is not None
        #         and configs['consumer_timeout_ms'] == 'inf'):
        #     configs['consumer_timeout_ms'] = float('inf')

        notify = False
        while True:  # Attende una connessione con il Broker
            try:
                return KafkaProducer(
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