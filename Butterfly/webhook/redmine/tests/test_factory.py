from unittest.mock import patch, MagicMock

from pytest import raises

from webhook.redmine.factory import RedmineWebhookFactory


@patch('webhook.redmine.factory.RedmineIssueWebhook')
def test_create_webhook(webhook_mock):

    factory = RedmineWebhookFactory()
    webhook = factory.create_webhook('issue')

    webhook_mock.assert_called_once()
    assert isinstance(webhook, MagicMock)

    with raises(NameError):
        factory.create_webhook('aaaa')
