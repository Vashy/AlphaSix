from webhook.factory import WebhookFactory
from webhook.webhook import Webhook
from webhook.gitlab.issue_webhook import GitlabIssueWebhook
from webhook.gitlab.push_webhook import GitlabPushWebhook

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

        if event_type == 'push':
            return GitlabPushWebhook()

        if event_type == 'commit-note':
            return GitlabPushWebhook()

        if event_type == 'issue-note':
            return GitlabPushWebhook()

        raise NameError()  # default
