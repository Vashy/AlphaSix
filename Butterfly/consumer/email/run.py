"""
File: run.py
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

Versione: 0.2.0
Creatore: Samuele Gardin, samuelegardin1997@gmail.com
Autori:
    Matteo Marchiori, matteo.marchiori@gmail.com
    Nicola Carlesso
"""

import kafka.errors

from consumer.email.creator import EmailConsumerCreator


def main():
    """Fetch dei topic dal file topics.json
    Campi:
    - topics['id']
    - topics['label']
    - topics['project']
    """

    # Inizializza WebhookConsumer
    try:
        consumer = EmailConsumerCreator().create()
    except kafka.errors.KafkaConfigurationError as e:
        print(e.with_traceback())

    try:
        consumer.listen()  # Resta in ascolto del Broker
    except KeyboardInterrupt:
        consumer.close()
        print(' Closing Consumer ...')


if __name__ == '__main__':
    main()
