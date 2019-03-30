from unittest.mock import patch, MagicMock
import json
from pathlib import Path

import pytest

from webhook.gitlab.issue_webhook import GitlabIssueWebhook
from webhook.gitlab.push_webhook import GitlabPushWebhook
from webhook.gitlab.commit_comment_webhook import GitlabCommitCommentWebhook
from webhook.gitlab.issue_comment_webhook import GitlabIssueCommentWebhook


def test_gitlab_issue_webhook():
    webhook = GitlabIssueWebhook()

    with pytest.raises(AssertionError):
        webhook.parse(None)

    with open(
            Path(__file__).parents[3] /
            'webhook/gitlab/tests' /
            'open_issue_gitlab_webhook.json'
        ) as file:
        whook = json.load(file)

    webhook = webhook.parse(whook)

    assert webhook['app'] == 'gitlab'
    assert webhook['object_kind'] == 'issue'
    assert webhook['title'] == 'New Issue'
    assert webhook['project_id'] == 'https://gitlab.com/AlphaSix/webhooktest'
    assert webhook['author'] == 'AlphaSix'
    assert webhook['action'] == 'open'

    with open(
            Path(__file__).parents[3] /
            'webhook/gitlab/tests' /
            'close_issue_gitlab_webhook.json'
        ) as file:
        whook = json.load(file)

    webhook = GitlabIssueWebhook()
    webhook = webhook.parse(whook)

    assert webhook['action'] == 'close'


def test_gitlab_push_webhook():
    webhook = GitlabPushWebhook()

    with pytest.raises(AssertionError):
        webhook.parse(None)

    with open(
            Path(__file__).parents[3] /
            'webhook/gitlab/tests' /
            'push_gitlab_webhook.json'
    ) as file:
        whook = json.load(file)

    webhook = webhook.parse(whook)

    for value in webhook:
        assert value['app'] == 'gitlab'
        assert value['object_kind'] == 'push'
        assert value['title'] == 'New commit fix #5 close #10 resolves #12'
        assert value['project_id'] == 'https://gitlab.com/AlphaSix/webhooktest'
        assert value['author'] == 'AlphaSix'


def test_gitlab_commit_comment_webhook():
    webhook = GitlabCommitCommentWebhook()

    with pytest.raises(AssertionError):
        webhook.parse(None)

    with open(
            Path(__file__).parents[3] /
            'webhook/gitlab/tests' /
            'commit_comment_gitlab_webhook.json'
    ) as file:
        whook = json.load(file)

    webhook = webhook.parse(whook)

    assert webhook['app'] == 'gitlab'
    assert webhook['object_kind'] == 'note_commit'
    assert webhook['title'] == 'Files added\n'
    assert webhook['project_id'] == 'http://gitlab-9888b58bf-6qj5c/root/butterfly-test-project-1'
    assert webhook['author'] == 'Administrator'
    assert webhook['comment'] == 'Just commenting a commit, don\'t bother with me'


def test_gitlab_issue_comment_webhook():
    webhook = GitlabIssueCommentWebhook()

    with pytest.raises(AssertionError):
        webhook.parse(None)

    with open(
            Path(__file__).parents[3] /
            'webhook/gitlab/tests' /
            'issue_comment_gitlab_webhook.json'
    ) as file:
        whook = json.load(file)

    webhook = webhook.parse(whook)

    assert webhook['app'] == 'gitlab'
    assert webhook['object_kind'] == 'note_issue'
    assert webhook['title'] == 'Test Issue 1'
    assert webhook['project_id'] == 'http://gitlab-9888b58bf-6qj5c/root/butterfly-test-project-1'
    assert webhook['author'] == 'Administrator'
    assert webhook['comment'] == 'This issue has been successfully commented'
