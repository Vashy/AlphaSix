"""
File: Producer.py
Data creazione: 2019-02-12

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
    <nome cognome, email>
    <nome cognome: email>
    ....
"""


from abc import ABC, abstractmethod


class Producer(ABC):
    """Interfaccia Producer"""

    def __init__(
                self,
                kafkaProducer: KafkaProducer,
                webhook_factory: WebhookFactory,
            ):

        self._webhook_factory = webhook_factory
        self._producer = kafkaProducer

    def produce(self, msg: str):
        """Produce il messaggio `msg` nel Topic designato del Broker"""

        # Parse del JSON associato al webhook ottenendo un oggetto Python
        webhook = webhook.parse(whook)

        webhook = self._webhook_factory.createWebhook(
            self.webhook_field(webhook)
        )

        try:
            # Inserisce il messaggio in Kafka, serializzato in formato JSON
            self._producer.send(webhook['app'], webhook)
            self._producer.flush(10)  # Attesa 10 secondi
        # Se non riesce a mandare il messaggio in 10 secondi
        except kafka.errors.KafkaTimeoutError:
            stderr.write('Impossibile inviare il messaggio\n')
            # exit(-1)

    @abstractmethod
    def webhook_field(self, whook: dict):
        pass
