from unittest.mock import Mock, patch, MagicMock

import pytest

from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaTimeoutError
from mongo_db.creator import MongoFacadeCreator
from mongo_db.facade import MongoFacade
from gestore_personale.ClientGP import ClientGP
from gestore_personale.Processor import Processor

# Kafka producer mock
KAFKA_PRODUCER = Mock()
KAFKA_PRODUCER.__class__ = KafkaProducer

# Kafka consumer mock
KAFKA_CONSUMER = Mock()
KAFKA_CONSUMER.__class__ = KafkaConsumer

# Mongo mock
MONGO = Mock()
MONGO.__class__ = MongoFacadeCreator

# Processor = Mock()

client = ClientGP(KAFKA_CONSUMER, KAFKA_PRODUCER, MONGO)

message = {
    'app': 'gitlab',
    'object_kind': 'note',
    'title': 'Issue numero quindici',
    'description': 'Questa è una stuqwerpida descrizione',
    'project_url': 'http/sdfbwjfenw'
}

message2 = {
    'app': 'redmine',
    'object_kind': 'issue',
    'title': 'Issue numero quinewrtdici',
    'description': 'Questa è una wqer descrizione',
    'project_url': 'http/itttt',  # diventa 'project_id'
    'action': 'opened',
    'label': 'fix'
}

map_message_contacts = {
    'email': ['2@gmail.com', '8@gmail.com'],
    'telegram': ['2', '3']
}


KAFKA_CONSUMER.__iter__ = Mock(return_value=iter([message, message2]))
# Processor.prepare_message.return_value = map_message_contacts
MONGO.instantiate.return_value = Mock()


def test_send_all():
    KAFKA_PRODUCER.send = Mock()

    client.send_all(map_message_contacts, message)

    KAFKA_PRODUCER.send.called
    KAFKA_PRODUCER.send.assert_called_with('telegram', {'app': 'gitlab', 'object_kind': 'note', 'title': 'Issue numero quindici', 'description': 'Questa è una stuqwerpida descrizione', 'project_url': 'http/sdfbwjfenw', 'receiver': '3'})
    # KAFKA_PRODUCER.send.assert_called_with('email', {'app': 'gitlab', 'object_kind': 'note', 'title': 'Issue numero quindici', 'description': 'Questa è una stuqwerpida descrizione', 'project_url': 'http/sdfbwjfenw', 'receiver': '3'})

    # KAFKA_PRODUCER.send.assert_called_once()  # Deve dare false: 4


# @patch('gestore_personale.Processor')
def test_process():
    client.send_all = Mock()
    # Processor = Mock()
    # Processor.prepare_message.return_value = map_message_contacts

    client.process(message)  # Metodo da testare

    client.send_all.assert_called_once()
    # client.send_all.assert_called_with(
    #     map_message_contacts, message
    # )


# Controlla che la chiamata a process effetivamente avvenga per i due messaggi
def test_read_message():
    client.process = Mock()

    client.read_messages()  # Metodo da testare

    # Verifichiamo che venga chiamato 2 volte per i 2 messaggi
    client.process.assert_any_call(message)
    client.process.assert_any_call(message2)
