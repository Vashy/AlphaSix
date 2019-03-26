import json

from kafka import KafkaProducer
import kafka.errors

from producer.gitlab.producer import GitlabProducer
from producer.creator import ProducerCreator
from producer.producer import Producer
from webhook.gitlab.factory import GitlabWebhookFactory


class GitlabProducerCreator(ProducerCreator):
    """Assembler per GitlabProducer
    """
    def instantiate(self, kafka_producer: KafkaProducer) -> Producer:
        return GitlabProducer(kafka_producer, GitlabWebhookFactory())
