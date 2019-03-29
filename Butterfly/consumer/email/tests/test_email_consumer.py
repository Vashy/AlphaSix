from unittest.mock import MagicMock, patch

from consumer.email.consumer import EmailConsumer

@patch('consumer.email.consumer.smtplib')
def test_send(
    smtplib,
):
    kafka_mock = MagicMock()
    consumer = EmailConsumer(kafka_mock, 'email')

    smtplib.SMTPAuthenticationError = Exception
    consumer.send('msg')
