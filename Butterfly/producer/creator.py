from abc import ABC, abstractmethod

from producer.producer import Producer


class ProducerCreator(ABC):
    @abstractmethod
    def create(self, configs) -> Producer:
        pass
