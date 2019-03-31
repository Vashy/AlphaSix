import json
from pathlib import Path

import pytest

from webhook.redmine.issue_webhook import RedmineIssueWebhook


def test_redmine_issue_webhook():
    webhook = RedmineIssueWebhook()

    with pytest.raises(AssertionError):
        webhook.parse(None)

    with open(
            Path(__file__).parents[3] /
            'webhook/redmine/tests' /
            'open_issue_redmine_webhook.json'
        ) as file:
        whook = json.load(file)

    webhook = webhook.parse(whook)

    assert webhook['app'] == 'redmine'
    assert webhook['object_kind'] == 'issue'
    assert webhook['title'] == 'Issue #1'
    assert webhook['description'] == 'This is a new issue'
    assert webhook['project_id'] == 1
    assert webhook['project_name'] == 'Test Project #1'
    assert webhook['action'] == 'opened'
    assert webhook['author'] == 'AlphaSix'
    assert webhook['assignees'] == 'AlphaSix'
    assert webhook['labels'] == 'Bug'

    assert webhook['update'] == {}


def test_redmine_update_issue_webhook():
    webhook = RedmineIssueWebhook()

    with pytest.raises(AssertionError):
        webhook.parse(None)

    with open(
            Path(__file__).parents[3] /
            'webhook/redmine/tests' /
            'update_1_issue_redmine_webhook.json'
    ) as file:
        whook = json.load(file)

    webhook = webhook.parse(whook)

    assert webhook['app'] == 'redmine'
    assert webhook['object_kind'] == 'issue'
    assert webhook['title'] == 'Issue #1'
    assert webhook['description'] == 'This is a new issue'
    assert webhook['project_id'] == 1
    assert webhook['project_name'] == 'Test Project #1'
    assert webhook['action'] == 'updated'
    assert webhook['author'] == 'AlphaSix'
    assert webhook['assignees'] == 'AlphaSix'
    assert webhook['labels'] == 'Bug'

    assert webhook['update']['comment'] == 'Editing Issue #1'
    assert webhook['update']['author'] == 'Redmine'
    assert webhook['update']['status'] == 'In Progress'
    assert webhook['update']['priority'] == 'Normal'
