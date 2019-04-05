"""
File: creator.py
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
Creatore: Samuele Gardin, samuelegardin1997@gmail.com
Autori:
"""

from kafka import KafkaConsumer
from consumer.creator import ConsumerCreator
from consumer.telegram.consumer import TelegramConsumer, Consumer


class TelegramConsumerCreator(ConsumerCreator):
    """Creator per TelegramConsumer
    """

    def instantiate(self, kafka_consumer: KafkaConsumer) -> Consumer:
        return TelegramConsumer(kafka_consumer, self.topic)

    @property
    def topic(self):
        return 'telegram'