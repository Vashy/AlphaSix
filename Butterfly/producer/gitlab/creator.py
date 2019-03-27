from kafka import KafkaProducer

from producer.gitlab.producer import GitlabProducer
from producer.creator import ProducerCreator
from producer.producer import Producer
from webhook.gitlab.factory import GitlabWebhookFactory


class GitlabProducerCreator(ProducerCreator):
    """Creator per `GitlabProducer`. Implementa `ProducerCreator`
    """
    def instantiate(self, kafka_producer: KafkaProducer) -> Producer:
        """Restituisce un istanza concreta di `GitlabProducer`.
        """
        return GitlabProducer(kafka_producer, GitlabWebhookFactory())
