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

Versione: 0.1.0
Creatore: Samuele Gardin, samuelegardin1997@gmail.com
Autori:

"""

from pathlib import Path
import json

from consumer.telegram.creator import TelegramConsumerCreator


_config_path = Path(__file__).parents[1] / 'config.json'


def _open_kafka_configs(path: Path = _config_path):
    """Apre il file di configurazione per Kafka.
    """

    with open(path) as file:
        configs = json.load(file)

    configs = configs['kafka']
    timeout = 'consumer_timeout_ms'
    if (timeout in configs
            and configs[timeout] == 'inf'):
        configs[timeout] = float('inf')
    return configs


def main():
    # Ottiene le configurazioni da Kafka
    configs = _open_kafka_configs()

    # Istanzia il TelegramConsumer
    consumer = TelegramConsumerCreator().create(configs)
    try:
        consumer.listen()
    except KeyboardInterrupt:
        consumer.close()
        print(' Closing Consumer ...')


if __name__ == '__main__':
    main()