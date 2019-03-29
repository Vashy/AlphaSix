"""
File: consumer.py
Data creazione: 2019-03-29

<descrizione>

Licenza: Apache 2.0

Copyright 2019 AlphaSix

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Versione: 0.1.0
Creatore: Timoty Granziero, timoty.granziero@gmail.com
Autori:

"""
from abc import ABC, abstractmethod
from pathlib import Path
import json

from kafka import KafkaConsumer
import kafka.errors

from consumer.consumer import Consumer


class ConsumerCreator(ABC):

    _config_path = Path(__file__).parents[0] / 'config.json'

    def create(self, configs=_config_path) -> Consumer:
         # Converte stringa 'inf' nel relativo float

        with open(ConsumerCreator._config_path, 'r') as f:
            configs = json.load(f)
        configs = configs['kafka']
        timeout = 'consumer_timeout_ms'
        if (timeout in configs
                and configs[timeout] is not None
                and configs[timeout] == 'inf'):
            configs[timeout] = float('inf')

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
