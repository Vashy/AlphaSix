from unittest.mock import Mock, patch, MagicMock

import kafka
import pytest

from producer.gitlab.creator import GitlabProducerCreator
import producer

def test_instantiate():
    creator = GitlabProducerCreator()
    mock = Mock()
    mock.__class__ = kafka.KafkaProducer
    value = creator.instantiate(mock)

    assert mock.assert_called


@patch('producer.gitlab.creator.GitlabWebhookFactory', MagicMock(return_value='Ok'))
@patch('producer.gitlab.creator.GitlabProducer')
@patch('producer.creator.KafkaProducer')
def test_producer_creator(kafka_mock, producer_mock):
    producer.creator.KafkaProducer()
    assert kafka_mock is producer.creator.KafkaProducer

    kafka_mock.return_value = MagicMock()
    producer_mock.return_value = MagicMock()

    creator = GitlabProducerCreator()
    creator.create({'bootstrap_servers': 'localhost'})

    assert kafka_mock.assert_called
    assert kafka_mock.assert_called
