# import json
# import unittest
# from pathlib import Path

from unittest.mock import MagicMock, patch

from consumer.telegram.creator import TelegramConsumerCreator


@patch('consumer.telegram.creator.TelegramConsumer', autospec=True)
@patch('consumer.telegram.creator.Path', autospec=True)
@patch('consumer.telegram.creator.telepot.Bot', autospec=True)
@patch('consumer.telegram.creator.json', autospec=True)
def test_instantiate(
        json,
        bot,
        path,
        consumer,
):
    creator = TelegramConsumerCreator()
    creator.instantiate(MagicMock())

    json.load.assert_called_once()
    bot.assert_called_once()
    bot.assert_called_once()
    consumer.assert_called_once()


@patch('consumer.creator.KafkaConsumer', autospec=True)
@patch('consumer.telegram.creator.TelegramConsumer', autospec=True)
@patch('consumer.telegram.creator.Path', autospec=True)
@patch('consumer.telegram.creator.telepot.Bot', autospec=True)
@patch('consumer.telegram.creator.json', autospec=True)
def test_create(
        json,
        bot,
        path,
        consumer,
        kafka,
):
    json.load.return_value = {
        'kafka': {
            'consumer_timeout_ms': 1,
        },
        'telegram': {
            'token_bot': '123123',
        },
        'another': 'value',
    }
    creator = TelegramConsumerCreator()
    creator.create({})

    json.load.assert_called_once()
    kafka.assert_called_once()


def test_topic():
    creator = TelegramConsumerCreator()
    assert creator.topic == 'telegram'
