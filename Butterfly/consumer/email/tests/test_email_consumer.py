from unittest.mock import MagicMock, patch

import pytest

from consumer.email.consumer import EmailConsumer


def test_preamble():
    kafka_mock = MagicMock()
    consumer = EmailConsumer(kafka_mock)

    assert 'aperta' in consumer._preamble('issue')
    assert 'push' in consumer._preamble('push')
    assert 'commentata una issue ' in consumer._preamble('issue-note')
    assert 'commentato' in consumer._preamble('commit-note')


msg = {
    'app': 'gitlab',
    'object_kind': 'issue',
    'receiver': '42',
    'project_name': 'Project',
    'project_id': 'http://...',
    'author': 'author',
    'title': 'Title',
    'description': 'Description',
    'action': 'open',
}


def test_format():
    kafka_mock = MagicMock()
    consumer = EmailConsumer(kafka_mock)

    res = consumer.format(msg)

    assert 'Gitlab' in res
    assert 'Project' in res
    assert 'http://...' in res
    assert 'author' in res
    assert 'Description' in res
    assert 'Description:' in res
    assert 'testo non presente' not in res


def test_format_html():
    kafka_mock = MagicMock()
    consumer = EmailConsumer(kafka_mock)

    res = consumer.format_html(msg)

    assert 'Gitlab' in res
    assert 'Project' in res
    assert '<code>http://...</code>' in res
    assert '<strong>Autore:</strong>' in res
    assert 'Description' in res
    assert 'Description:' in res
    assert 'testo non presente' not in res


@patch('consumer.email.consumer.smtplib.SMTP')
@patch('consumer.email.consumer.os.environ', MagicMock())
# @pytest.mark.skip()
def test_send(
        smtp,
):
    kafka_mock = MagicMock()
    consumer = EmailConsumer(kafka_mock)

    consumer.send('a@gmail.com', msg)
    smtp.assert_called_once_with('smtp.gmail.com', 587)
