from unittest.mock import MagicMock, patch

import pytest

import producer
from producer.server import FlaskServer


def test_server():
    flask_mock = MagicMock()
    producer_mock = MagicMock()

    server = FlaskServer(flask_mock, producer_mock, 'gitlab')
    server.run(MagicMock())

    flask_mock.run.assert_called_once()


@patch('producer.server.request')
def test_webhook_handler(request_mock):
    request_mock.headers = {}
    request_mock.headers['Content-Type'] = 'application/json'
    request_mock.get_json.return_value = {}

    producer_mock = MagicMock()
    producer_mock.produce.return_value = None

    server = FlaskServer(MagicMock(), producer_mock, 'gitlab')
    value = server._webhook_handler()
    assert value == ('Ok', 200)

    producer_mock.produce.side_effect = KeyError()
    value = server._webhook_handler()
    assert value == ('Messaggio malformato', 402)

    request_mock.headers['Content-Type'] = 'xml'
    value = server._webhook_handler()
    assert value == ('', 400)
