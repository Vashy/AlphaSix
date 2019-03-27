from abc import ABC, abstractmethod

from webhook.webhook import Webhook


class WebhookFactory(ABC):

    @abstractmethod
    def create_webhook(self, event_type: str) -> Webhook:
        pass
