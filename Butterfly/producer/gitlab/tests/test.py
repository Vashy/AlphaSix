import pytest
from producer.gitlab.GLProducer import GLProducer
from unittest.mock import Mock
from kafka import KafkaProducer
from pathlib import Path

class ProdTest:
    def __init__(self, kafka_producer: KafkaProducer):
        assert isinstance(kafka_producer, KafkaProducer)
        self.producer = kafka_producer

mock = Mock()
mock.__class__ = KafkaProducer
mock.send.return_value = True

def test():
    assert 3 == 3
    assert False == False
    print(mock)
    producer = ProdTest(mock)
    producer = GLProducer(mock)

    # with open(Path(__file__).parents[0] / "webhook" / "gitlab" / "open_issue_gitlab.json", "r") as f:
    #      = f
    # producer.produce("topic", )
