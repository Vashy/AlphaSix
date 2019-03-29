from unittest.mock import MagicMock, patch

from consumer.email.consumer import EmailConsumer


@patch('consumer.email.consumer.smtplib.SMTP')
# @patch('consumer.email.consumer.smtplib.SMTP')
def test_send(
        smtp,
):
    kafka_mock = MagicMock()
    consumer = EmailConsumer(kafka_mock, 'email')

    consumer.send('a@gmail.com', 'msg')
    smtp.assert_called_once_with('smtp.gmail.com', 587)
    assert consumer.bold == ''


@patch('consumer.consumer.json')
@patch('consumer.email.consumer.smtplib.SMTP')
def test_listen(_, json):
    kafka_mock = MagicMock()
    consumer = EmailConsumer(kafka_mock, 'email')

    msg = MagicMock()
    json.loads.return_value = {
        'app': 'telegram',
        'receiver': '142',
        'project_name': 'Project',
        'project_id': 'http://...',
        'author': 'author',
        'title': 'Title',
        'description': 'Description',
        'action': 'open',
    }

    kafka_mock.__iter__.return_value = [
        msg
    ]

    consumer.listen()

    json.loads.assert_called_once()
