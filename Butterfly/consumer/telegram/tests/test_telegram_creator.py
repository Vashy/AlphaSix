# import json
# import unittest
# from pathlib import Path

from unittest.mock import MagicMock, patch

import pytest

from consumer.telegram.creator import TelegramConsumerCreator, TelegramConsumer


@patch('consumer.telegram.creator.TelegramConsumer', autospec=True)
def test_instantiate(
        consumer,
):
    creator = TelegramConsumerCreator()
    consumer = creator.instantiate(MagicMock())

    assert isinstance(consumer, TelegramConsumer)


@patch('consumer.creator.KafkaConsumer', autospec=True)
@patch('consumer.telegram.creator.TelegramConsumer', autospec=True)
@patch('consumer.creator.json', autospec=True)
def test_create(
        json,
        consumer,
        kafka,
):
    json.loads.return_value = {
        'kafka': {
            'consumer_timeout_ms': 1,
        },
        'telegram': {
            'token_bot': '123123',
        },
        'another': 'value',
    }
    creator = TelegramConsumerCreator()
    consumer = creator.create({})

    assert isinstance(consumer, TelegramConsumer)
    kafka.assert_called_once()


def test_topic():
    creator = TelegramConsumerCreator()
    assert creator.topic == 'telegram'
