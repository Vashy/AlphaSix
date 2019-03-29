from unittest.mock import MagicMock, patch

import pytest

from consumer.telegram.consumer import TelegramConsumer


def test_send():
    kafka_mock = MagicMock()
    bot_mock = MagicMock()
    bot_mock.sendMessage.return_value = {'prova': 'prova', 'a': 5}
    consumer = TelegramConsumer(kafka_mock, 'telegram', bot_mock)

    log = consumer.send({'msg': 'messaggio'})
    assert log == {'prova': 'prova', 'a': 5}

    bot_mock.sendMessage.assert_called_once()

    bot_mock.sendMessage.return_value = None

    log = consumer.send({'msg': 'messaggio'})
    assert log is None


def test_listen():
    kafka_mock = MagicMock()
    bot_mock = MagicMock()
    bot_mock.sendMessage.return_value = {'prova': 'prova', 'a': 5}
    consumer = TelegramConsumer(kafka_mock, 'telegram', bot_mock)

    kafka_mock.__iter__.return_value = [
        {b'value': b'lul'},
        {b'', b''},
    ]

    assert consumer.bold == '*'


def test_print():
    kafka_mock = MagicMock()
    bot_mock = MagicMock()
    bot_mock.sendMessage.return_value = {'prova': 'prova', 'a': 5}
    consumer = TelegramConsumer(kafka_mock, 'telegram', bot_mock)

    diz = {
        'app': 'telegram',
        'receiver': '142',
        'project_name': 'Project',
        'project_id': 'http://...',
        'author': 'author',
        'title': 'Title',
        'description': 'Description',
        'action': 'open',
    }

    dest, res = consumer.format(diz)

    assert 'telegram' in res
    assert 'Project' in res
    assert 'http://...' in res
    assert 'author' in res
    assert 'Description' in res
    assert '*Description*:' in res
    assert 'Orca marina' not in res
    assert dest == '142'
