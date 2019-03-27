
from unittest.mock import Mock

import pytest
from kafka import KafkaProducer

from producer.gitlab.producer import GitlabProducer
from webhook.factory import WebhookFactory


# Kafka producer mock
KAFKA_PRODUCER = Mock()
KAFKA_PRODUCER.__class__ = KafkaProducer

# Webhook mock
WEBHOOK_MOCK = Mock()
WEBHOOK_MOCK.parse.return_value = {'app': 'gitlab'}

# Factory mock
FACTORY = Mock()
FACTORY.__class__ = WebhookFactory
FACTORY.create_webhook.return_value = WEBHOOK_MOCK


def test_webhook_type():
    producer = GitlabProducer(
        KAFKA_PRODUCER,
        FACTORY,
    )
    value = producer.webhook_type({'object_kind': 'issue'})
    assert value == 'issue'


def test_produce():
    producer = GitlabProducer(
        KAFKA_PRODUCER,
        FACTORY
    )
    producer.produce({'object_kind': 'issue'})

# @pytest.mark.skip(reason="no way of currently testing this")
def test_constructor():
    with pytest.raises(AssertionError):
        GitlabProducer(FACTORY, FACTORY)

    with pytest.raises(AssertionError):
        GitlabProducer(KAFKA_PRODUCER, KAFKA_PRODUCER)
