from unittest.mock import MagicMock, patch

from consumer.email.creator import EmailConsumerCreator, EmailConsumer


def test_instantiate():
    creator = EmailConsumerCreator()
    assert creator.topic == 'email'
    assert creator.topic != 'telegram'

    kafka_mock = MagicMock()
    consumer = creator.instantiate(kafka_mock)

    assert isinstance(consumer, EmailConsumer)

@patch('consumer.creator.Path')
@patch('consumer.creator.KafkaConsumer', autospec=True)
@patch('consumer.creator.json')
def test_create(
        json,
        kafka,
        path,
):
    json.load.return_value = {
        'kafka': {
            'consumer_timeout_ms': 1,
        },
        'another': 'value'
    }
    creator = EmailConsumerCreator()

    consumer = creator.create()
    assert isinstance(consumer, EmailConsumer)
