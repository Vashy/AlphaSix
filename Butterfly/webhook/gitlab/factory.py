from webhook.factory import WebhookFactory
from webhook.webhook import Webhook

class GitlabWebhookFactory(WebhookFactory):

    def createWebhook(self, event_type: str) -> Webhook:
        if event_type == 'issue':
            return GitlabIssueWebhook()
        # elif event_type == 'push':
        #     return GitlabPushWebhook()
        # elif event_type == 'comment':
        #     return GitlabCommentWebhook()
