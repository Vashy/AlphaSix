from unittest.mock import patch

from consumer.creator import KafkaConsumerCreator, KafkaConsumer

@patch('consumer.creator.json.loads')
@patch('consumer.creator.kafka.errors.NoBrokersAvailable', autospec=True)
@patch('consumer.creator.KafkaConsumer', autospec=True)
def test_create(
        kafka,
        errors,
        json_loads,
):

    creator = KafkaConsumerCreator()
    kafka_consumer = creator.create({}, 'topic')

    kafka.assert_called_once()
    assert isinstance(kafka_consumer, KafkaConsumer)
