from unittest.mock import patch, MagicMock


from producer.creator import KafkaProducerCreator
import producer


@patch('producer.creator.KafkaProducer')
def test_producer_creator(kafka_mock):
    producer.creator.KafkaProducer()
    assert kafka_mock is producer.creator.KafkaProducer

    kafka_mock.return_value = MagicMock()

    creator = KafkaProducerCreator()
    creator.create({'bootstrap_servers': 'localhost'})

    assert kafka_mock.assert_called
    assert kafka_mock.assert_called
