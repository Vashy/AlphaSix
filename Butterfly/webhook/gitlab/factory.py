from webhook.factory import WebhookFactory
from webhook.webhook import Webhook
from webhook.gitlab.issue_webhook import GitlabIssueWebhook
from webhook.gitlab.push_webhook import GitlabPushWebhook
from webhook.gitlab.issue_comment_webhook import GitlabIssueCommentWebhook
from webhook.gitlab.commit_comment_webhook import GitlabCommitCommentWebhook


class GitlabWebhookFactory(WebhookFactory):
    """Crea Webhook del tipo `GitlabWebhook`."""

    def create_webhook(self, kind: str) -> Webhook:
        """Crea un `GitlabWebhook` concreto in base al parametro.

        Parameters:

        `kind` - può essere 'issue', 'push'.

        Raises:

        `NameError` - se il tipo di webhook non viene riconosciuto.
        """
        if kind == 'issue':
            return GitlabIssueWebhook()

        if kind == 'push':
            return GitlabPushWebhook()

        if kind == 'commit-note':
            return GitlabCommitCommentWebhook()

        if kind == 'issue-note':
            return GitlabIssueCommentWebhook()

        raise NameError()  # default
