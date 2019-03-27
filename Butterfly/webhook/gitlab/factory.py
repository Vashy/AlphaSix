from webhook.factory import WebhookFactory
from webhook.webhook import Webhook
from webhook.gitlab.issue_webhook import GitlabIssueWebhook


class GitlabWebhookFactory(WebhookFactory):
    """Crea Webhook del tipo `GitlabWebhook`."""

    def create_webhook(self, event_type: str) -> Webhook:
        """Crea un `GitlabWebhook` concreto in base al parametro.

        Parameters:

        `event_type` - può essere 'issue', 'push'.

        Raises:

        `NameError` - se il tipo di webhook non viene riconosciuto.
        """
        if event_type == 'issue':
            return GitlabIssueWebhook()

        raise NameError()  # default
