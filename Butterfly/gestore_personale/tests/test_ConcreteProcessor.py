from unittest.mock import Mock, patch, MagicMock
from gestore_personale.ConcreteProcessor import GitlabProcessor, RedmineProcessor


mongoFacade = Mock()
message_issue_gitlab = {
    'app': 'gitlab',
    'object_kind': 'issue',
    'title': 'Issue #1',
    'description': 'cose a caso',
    'project_id': 'https://nfnidd',
    'project_name': 'proj #1',
    'author': 'Tullio',
    'assignees': [
        'me',
        'te'
    ],
    'action': 'close',
    'labels': [
        'bug',
        'fix'
    ]
}

message_issue_redmine = {
'app': 'redmine',
    'object_kind': 'issue',
    'title': 'Issue #1',
    'description': 'cose a caso',
    'project_id': 1,
    'project_name': 'proj #1',
    'author': 'Tullio',
    'assignees': 'me',
    'action': 'close',
    'labels': 'Bug'
}

message_commit_gitlab = {
    'app': 'gitlab',
    'object_kind': 'issue',
    'title': 'Issue #1',
    'project_id': 'https://nfnidd',
    'project_name': 'proj #1',
    'author': 'Tullio'
}

message_commit_comment_gitlab = {
    'app': 'gitlab',
    'object_kind': 'note_issue',
    'title': 'Issue #1',
    'description': 'cose a caso',
    'project_id': 'https://nfnidd',
    'project_name': 'proj #1',
    'author': 'Tullio',
    'comment': 'commento'
}

mongoFacade.get_match_keywords.return_value = ['1', '2', '3', '4']
mongoFacade.get_match_labels.return_value = ['1', '2', '5']
users = ['1', '2', '3', '4', '5', '6', '7']


def test_gitlab_filter_push():
    p_gitlab = GitlabProcessor(message_commit_gitlab, mongoFacade)
    user_subscribes = p_gitlab._filter_users_by_topic(users, 'push')
    assert user_subscribes == ['1', '2', '3', '4']

def test_gitlab_filter_issue():
    p_gitlab = GitlabProcessor(message_issue_gitlab, mongoFacade)
    user_subscribers = p_gitlab._filter_users_by_topic(users, 'issue')
    assert user_subscribers == ['1', '2', '5']

def test_redmine_filter_issue():
    p_gitlab = RedmineProcessor(message_issue_redmine, mongoFacade)
    user_subscribers = p_gitlab._filter_users_by_topic(users, 'issue')
    assert user_subscribers == ['1', '2', '5']