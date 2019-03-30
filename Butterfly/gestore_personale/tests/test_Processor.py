
from unittest.mock import Mock, patch, MagicMock

import pytest

from gestore_personale.Processor import Processor


mongofacade = Mock()
message = {
    'app': 'redmine',
    'object_kind': 'issue',
    'title': 'Issue numero quindici',
    'description': 'Questa è una stupida descrizione',
    'project_url': 'http/sdfbwjfenw',
    'action': 'updated',
    'label': 'bug'
}
mongofacade.get_project_by_url.return_value = True
# mongofacade.insert_project.return_value =
mongofacade.get_users_available.return_value = ['1', '2']
p = Processor(message, mongofacade)
p.get_telegram_contacts.return_value = ['12314', '435435', '2']
p.get_email_contacts.return_value = ['matteo@gmail.it', 'pino@gmail.com']


def test_prepare_message():
    # p = Processor(message, mongofacade)
    p.prepare_message()
    assert p is not False


def test_check_project():
    url = p._check_project()
    assert url == 'http/sdfbwjfenw'


def test_get_involved_users():
    lista = p.get_involved_users(message['project_url'])
    assert lista == ['1', '2']
