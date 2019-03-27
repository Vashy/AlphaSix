from unittest.mock import MagicMock, patch

import pytest

import producer
from producer.server import FlaskServerCreator, FlaskServer


@patch('producer.server.FlaskServer')
@patch('producer.server.Flask')
def test_flask_creator(flask_mock, server_mock):
    mock = MagicMock()
    with pytest.raises(AssertionError):
        FlaskServerCreator(mock)

    mock.__class__ = producer.gitlab.creator.GitlabProducerCreator
    server = FlaskServerCreator(mock)
    app = server.initialize_app('gitlab')

    flask_mock.assert_called_once()
    server_mock.assert_called_once()


@patch('producer.server.Path')
@patch('producer.server.json')
def test_open_configs(json_mock, path_mock):
    path_mock.return_value = producer.server.Path()
    json_mock.load.return_value = {'gitlab': '5003'}
    val = producer.server._open_configs(path_mock())

    assert 'gitlab' in val
    assert path_mock.called_once


@patch('producer.server.json')
def test_server(json_mock):
    flask_mock = MagicMock()
    producer_mock = MagicMock()
    json_mock.load.return_value = {
        'gitlab': {
            'ip': 'localhost',
            'port': 5003,
        }
    }

    server = FlaskServer(flask_mock, producer_mock, 'gitlab')
    server.run(MagicMock())

    json_mock.load.assert_called_once()
    flask_mock.run.assert_called_once()


@patch('producer.server.request')
def test_processor(request_mock):
    request_mock.headers = {}
    request_mock.headers['Content-Type'] = 'application/json'
    request_mock.get_json.return_value = {}

    producer_mock = MagicMock()
    producer_mock.produce.return_value = None

    server = FlaskServer(MagicMock(), producer_mock, 'gitlab')
    value = server._processor()
    assert value == ('', 200)

    producer_mock.produce.side_effect = KeyError()
    value = server._processor()
    assert value == ('', 401)

    request_mock.headers['Content-Type'] = 'xml'
    value = server._processor()
    assert value == ('', 400)
