from kafka import KafkaProducer, KafkaConsumer
# from kafka import KafkaConsumer
from kafka.errors import KafkaTimeoutError

from gestore_personale.KafkaCreator.KafkaConsumerCreator import KafkaConsumerCreator
from gestore_personale.KafkaCreator.KafkaProducerCreator import KafkaProducerCreator
from gestore_personale.Processor import Processor
from mongo_db.creator import MongoFacadeCreator


class ClientGP():
    def __init__(
            self,
            consumer: KafkaConsumer,
            producer: KafkaProducer,
            mongo: MongoFacadeCreator
    ):
        # print(type(kafka_producer))
        # print(KafkaProducer)
        assert isinstance(producer, KafkaProducer)
        assert isinstance(consumer, KafkaConsumer)
        self._consumer = consumer
        self._producer = producer
        self._mongo = mongo

    def read_messages(self):
        # Per ogni messaggio ricevuta da Kafka, processiamolo
        # in modo da poterlo reinserirlo in Telegram o Email
        for message in self._consumer:
            self.process(message)

    def process(self, message: dict):
        processore_messaggio = Processor(message, self._mongo.instantiate())
        mappa_contatto_messaggio = processore_messaggio.prepare_message()
        self.send_all(mappa_contatto_messaggio, message)

    def send_all(self, map_message_contact: dict, message: dict):
        # app_ricevente sarà telegram o email (chiave,valore)
        for app_ricevente, contact_list in map_message_contact.items():
            for contact in contact_list:
                try:
                    message['receiver'] = contact  # da ricontrollare
                    # Inserisce il messaggio in Kafka, serializzato in formato JSON
                    self._producer.send(
                        app_ricevente, message
                    )
                    self._producer.flush(10)  # Attesa 10 secondi
                # Se non riesce a mandare il messaggio in 10 secondi
                except KafkaTimeoutError:
                    print('Impossibile inviare il messaggio\n')


if __name__ == "__main__":
    # producer = self._creator.create(configs['kafka'])  # O senza il campo
    kafka_consumer = KafkaConsumerCreator.create()
    kafka_producer = KafkaProducerCreator.create()
    mongo = MongoFacadeCreator()
    client = ClientGP(kafka_consumer, kafka_producer, mongo)
    client.read_messages()
