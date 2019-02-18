
# Posizione: Butterfly/
# Uso: python3 -m path.to.GLProducer

import argparse
from sys import stderr
from kafka import KafkaProducer
import kafka.errors
import json
from pathlib import Path
from producer.producer import Producer
from webhook.webhook import GLIssueWebhook


class WebhookProducer(Producer):
    def __init__(self, config):
        self._producer = KafkaProducer(
            # Serializza l'oggetto Python in un oggetto JSON, codifica UTF-8
            value_serializer=lambda m: json.dumps(m).encode('utf-8'),
            **config
        )

    def __del__(self):
        self.close()


    @property
    def producer(self):
        """Restituisce il KafkaProducer"""
        return self._producer


    def produce(self, topic, msg: GLIssueWebhook):
        """Produce il messaggio in Kafka.
        Precondizione: msg è di tipo GLIssueWebhook

        Arguments:
        topic -- il topic dove salvare il messaggio.
        """

        assert isinstance(msg, GLIssueWebhook), \
                'msg non è di tipo GLIssueWebhook'

        # Parse del JSON associato al webhook ottenendo un oggetto Python 
        msg.parse()
        try:
            print()
            # Inserisce il messaggio in Kafka, serializzato in formato JSON
            self.producer.send(topic, msg.webhook())
            self.producer.flush(10) # Attesa 10 secondi
        except kafka.errors.KafkaTimeoutError:
            stderr.write('Errore di timeout\n')
            exit(-1)

    def close(self):
        """Rilascia il Producer associato"""
        self._producer.close()


def main():

    # Configurazione da config.json
    with open(Path(__file__).parent / 'config.json') as f:
        config = json.load(f)

    """Fetch dei topic dal file topics.json
    Campi:
    - topics['id']
    - topics['label']
    - topics['project']
    """
    with open(Path(__file__).parent.parent / 'topics.json') as f:
        topics = json.load(f)

    # Istanzia il Producer
    producer = WebhookProducer(config)

    # Parsing dei parametri da linea di comando
    parser = argparse.ArgumentParser(description='Crea messaggi su Kafka')
    parser.add_argument('-t', '--topic', type=str,
                        help='topic di destinazione')
    args = parser.parse_args()

    # Produce i messaggi nel topic passato come argomento


    # Inizializza il GLIssueWebhook con il path a webhook.json
    webhook = GLIssueWebhook(Path(__file__).parent.parent / 'webhook/webhook.json')
    if args.topic:
        producer.produce(args.topic, webhook)
    else:
        producer.produce(topics[0]['label'], webhook)


if __name__ == '__main__':
    main()
