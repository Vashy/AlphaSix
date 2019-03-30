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

# Processor
PROCESSOR = Mock()
PROCESSOR.__class__ = Processor

client = ClientGP(KAFKA_CONSUMER, KAFKA_PRODUCER, MONGO)

message_items = {
    'message' : 'user',
    'message' : 'user',
    'message' : 'user',
    'message' : 'user',
    'message' : 'user',
    'message' : 'user',
    'message' : 'user',
}


def test_read_message():
    print('test')


@patch('gestore_personale.ClientGP.process')
def test_process():
    print('test')


def test_send_all():
    client.send_all(message_items)
