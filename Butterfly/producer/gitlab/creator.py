import json

from kafka import KafkaProducer
import kafka.errors

from producer.gitlab.producer import GitlabProducer
from producer.creator import ProducerCreator
from producer.producer import Producer


class GitlabProducerCreator(ProducerCreator):
    """Assembler per GitlabProducer
    """
    def instantiate(self, kafka_producer: KafkaProducer) -> Producer:
        return GitlabProducer(kafka_producer, GitlabWebhookFactory())
