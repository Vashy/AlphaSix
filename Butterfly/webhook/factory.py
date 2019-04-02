from abc import ABC, abstractmethod

from webhook.webhook import Webhook


class WebhookFactory(ABC):
    """Interfaccia WebhookFactory per la creazione degli Webhook.
    """

    @abstractmethod
    def create_webhook(self, kind: str) -> Webhook:
        """Crea il `Webhook` concreto in base a `event_type`.

        Parameters:

        `event_type` - Il tipo di Webhook da creare.
        """
