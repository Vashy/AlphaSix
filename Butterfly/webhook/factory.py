from abc import ABC, abstractmethod

from webhook.webhook import Webhook


class WebhookFactory(ABC):

    @abstractmethod
    def createWebhook(self, type: str) -> Webhook:
        pass
