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
    assert webhook['app'] == 'gitlab'
    assert webhook['object_kind'] == 'push'
    assert webhook['project_id'] == 'https://gitlab.com/AlphaSix/webhooktest'
    assert webhook['project_id'] == 'https://gitlab.com/AlphaSix/webhooktest'
    assert webhook['project_name'] == 'WebHookTest'
    assert webhook['author'] == 'AlphaSix'
    assert webhook['commits_count'] == 1
    assert webhook['repository'] == 'WebHookTest'
    assert webhook['commits'][0]['id'] \
        == 'e1ec96b6eb5e67422935913530a54b0c612acf87'


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
    assert webhook['object_kind'] == 'commit-note'
    assert webhook['title'] == 'Files added\n'
    assert webhook['project_id'] == 'http://gitlab-9888b58bf-6qj5c/root/butterfly-test-project-1'
    assert webhook['author'] == 'Administrator'
    assert webhook['description'] == 'Just commenting a commit, don\'t bother with me'


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
    assert webhook['object_kind'] == 'issue-note'
    assert webhook['title'] == 'Test Issue 1'
    assert webhook['project_id'] == 'http://gitlab-9888b58bf-6qj5c/root/butterfly-test-project-1'
    assert webhook['author'] == 'Administrator'
    assert webhook['description'] == 'This issue has been successfully commented'
