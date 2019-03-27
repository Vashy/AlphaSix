from webhook.factory import WebhookFactory
from webhook.webhook import Webhook
from webhook.gitlab.issue_webhook import GitlabIssueWebhook


class GitlabWebhookFactory(WebhookFactory):
    """Crea Webhook del tipo GitlabWebhook."""

    def create_webhook(self, event_type: str) -> Webhook:
        if event_type == 'issue':
            return GitlabIssueWebhook()
        # elif event_type == 'push':
        #     return GitlabPushWebhook()
        # elif event_type == 'comment':
        #     return GitlabCommentWebhook()

        raise NameError()
