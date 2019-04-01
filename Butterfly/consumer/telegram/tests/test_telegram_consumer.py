from unittest.mock import MagicMock, patch

import pytest

from consumer.telegram.consumer import TelegramConsumer

@patch('consumer.telegram.consumer.requests', autospec=True)
def test_send(requests):
    kafka_mock = MagicMock()
    consumer = TelegramConsumer(kafka_mock, 'telegram')

    # requests.post.return_value = {
    #     'result': {
    #         'chat': {
    #             'username': 'aaa',
    #             'id': '123',
    #         }
    #     }
    # }
    mock = MagicMock()
    requests.post.return_value = mock
    mock.ok = True
    mock.json.return_value = {
        'result': {
            'chat': {
                'username': 'aaa',
                'id': '123',
            }
        }
    }
    response = consumer.send('123123', {'msg': 'messaggio'})
    assert response is True

    mock.json.assert_called_once()

    mock.ok = False
    response = consumer.send('123', {})
    assert response is False


def test_listen():
    kafka_mock = MagicMock()
    bot_mock = MagicMock()
    bot_mock.sendMessage.return_value = {'prova': 'prova', 'a': 5}
    consumer = TelegramConsumer(kafka_mock, 'telegram')

    kafka_mock.__iter__.return_value = [
        {b'value': b'lul'},
        {b'', b''},
    ]

    assert consumer.bold == '*'


def test_print():
    kafka_mock = MagicMock()
    bot_mock = MagicMock()
    bot_mock.sendMessage.return_value = {'prova': 'prova', 'a': 5}
    consumer = TelegramConsumer(kafka_mock, 'telegram')

    diz = {
        'app': 'telegram',
        'object_kind': 'issue',
        'receiver': '42',
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
    assert '*Description:*' in res
    assert 'Orca marina' not in res
    assert dest == '42'
