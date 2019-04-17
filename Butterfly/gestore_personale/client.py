from kafka import KafkaProducer, KafkaConsumer
# from kafka import KafkaConsumer
from kafka.errors import KafkaTimeoutError

from gestore_personale.creator import KafkaConsumerCreator
from gestore_personale.creator import KafkaProducerCreator
# from gestore_personale.processor import Processor
from gestore_personale.concrete_processor import GitlabProcessor
from gestore_personale.concrete_processor import RedmineProcessor
from mongo_db.facade import MongoFacade
from mongo_db.singleton import MongoSingleton
from mongo_db.users import MongoUsers
from mongo_db.projects import MongoProjects


class ClientGP():
    def __init__(
            self,
            consumer: KafkaConsumer,
            producer: KafkaProducer,
            mongo: MongoFacade
    ):
        # print(type(kafka_producer))
        # print(KafkaProducer)
        assert isinstance(producer, KafkaProducer)
        assert isinstance(consumer, KafkaConsumer)
        self._consumer = consumer
        self._producer = producer
        self._mongo = mongo

    def read_messages(self):
        print('Listening to messages from topics:')
        for topic in self._consumer.subscription():
            print(f'- {topic}')
        print()
        # Per ogni messaggio ricevuta da Kafka, processiamolo
        # in modo da poterlo reinserirlo in Telegram o Email
        for message in self._consumer:
            self.process(message.value)

    def process(self, message: dict):
        tecnology = message['app']
        if tecnology == 'gitlab':
            processore_messaggio = GitlabProcessor(
                message, self._mongo
            )
        elif tecnology == 'redmine':
            processore_messaggio = RedmineProcessor(
                message, self._mongo
            )
        # processore_messaggio = Processor(message, self._mongo.instantiate())
        mappa_contatto_messaggio = processore_messaggio.prepare_message()
        self.send_all(mappa_contatto_messaggio, message)

    def send_all(self, map_message_contact: dict, message: dict):
        # app_ricevente sarà telegram o email (chiave,valore)
        for app_ricevente, contact_list in map_message_contact.items():
            for contact in contact_list:
                try:
                    message['receiver'] = contact  # da ricontrollare
                    import pdb; pdb.set_trace()
                    # Inserisce il messaggio in Kafka, serializzato in formato JSON
                    self._producer.send(
                        app_ricevente, message
                    )
                    print(f'inviato msg sul topic {app_ricevente}')
                    self._producer.flush(10)  # Attesa 10 secondi
                # Se non riesce a mandare il messaggio in 10 secondi
                except KafkaTimeoutError:
                    print('Impossibile inviare il messaggio\n')

    def close(self):
        print('\nClosing Producer ...')
        self._producer.close()

        print('Closing Consumer ...')
        self._consumer.close()

        print('bye')


if __name__ == "__main__":
    # producer = self._creator.create(configs['kafka'])  # O senza il campo
    kafka_consumer = KafkaConsumerCreator().create()
    kafka_producer = KafkaProducerCreator().create()
    mongo = MongoFacade(
        MongoUsers(MongoSingleton.instance()),
        MongoProjects(MongoSingleton.instance()),
    )
    client = ClientGP(kafka_consumer, kafka_producer, mongo)
    try:
        client.read_messages()
    except KeyboardInterrupt:
        pass
    finally:
        client.close()
