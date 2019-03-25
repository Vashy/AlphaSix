from kafka import KafkaConsumer


from consumer.creator import ConsumerCreator
from consumer.telegram.TelegramConsumer import TelegramConsumer, Consumer


class TelegramConsumerCreator(ConsumerCreator):
    """Assembler per GitlabProducer
    """

    def instantiate(self, kafka_consumer: KafkaConsumer) -> Consumer:
        return TelegramConsumer(kafka_consumer)

    @property
    def topic(self):
        return 'telegram'
