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
        msg,
    ]

    # Mock degli altri metodi della classe
    with    patch.object(EmailConsumer, 'format') as fmt, \
            patch.object(EmailConsumer, 'send') as send, \
            patch.object(EmailConsumer, 'prelisten_hook') as hook:
        hook.return_value = None
        fmt.return_value = ('123', 'A juicy message')
        send.return_value = None

        consumer.listen()

        fmt.assert_called_once()
        hook.assert_called_once()
        send.assert_called_once_with('123', 'A juicy message')

    json.loads.assert_called_once()
