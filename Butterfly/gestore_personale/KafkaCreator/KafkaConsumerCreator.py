from abc import ABC, abstractmethod
from pathlib import Path
import json

from kafka import KafkaConsumer
import kafka.errors


class KafkaConsumerCreator():

    _config_path = Path(__file__).parents[1] / 'config_consumer.json'

    def create(self, configs=_config_path) -> KafkaConsumer:
        # Converte stringa 'inf' nel relativo float

        with open(KafkaConsumerCreator._config_path, 'r') as f:
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
                return KafkaConsumer(
                    self.topic(),
                    # Deserializza i messaggi dal formato JSON a oggetti Python
                    value_deserializer=(
                      (lambda m: json.loads(m.decode('utf-8'))),
                    )
                    ** configs,
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

    def topic(self) -> list:
        return ['redmine', 'gitlab']
