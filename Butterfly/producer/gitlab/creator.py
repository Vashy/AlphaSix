import json

from kafka import KafkaProducer
import kafka.errors

from producer.gitlab.producer import GitlabProducer
from producer.creator import ProducerCreator
from producer.producer import Producer


class GitlabProducerCreator(ProducerCreator):
    """Assembler per GitlabProducer
    """
    def create(self, configs) -> Producer:
        notify = False
        while True:  # Attende una connessione con il Broker
            try:
                kafkaProducer = KafkaProducer(
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

        # Istanzia il Producer
        producer = GitlabProducer(kafkaProducer)
        return producer
