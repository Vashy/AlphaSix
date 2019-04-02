from webhook.factory import WebhookFactory
from webhook.webhook import Webhook
from webhook.redmine.issue_webhook import RedmineIssueWebhook


class RedmineWebhookFactory(WebhookFactory):
    """Crea Webhook del tipo `GitlabWebhook`."""

    def create_webhook(self, kind: str) -> Webhook:
        """Crea un `RedmineWebhook` concreto in base al parametro.

        Parameters:

        `kind` - può essere 'issue', 'push'.

        Raises:

        `NameError` - se il tipo di webhook non viene riconosciuto.
        """
        if kind == 'issue':
            return RedmineIssueWebhook()

        raise NameError()  # default
