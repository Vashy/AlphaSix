import re

from gestore_personale.Processor import Processor
from mongo_db.facade import MongoFacade


class GitlabProcessor(Processor):


    def filter_users_by_topic(self, users: list, obj: str) -> list:
        try:
            if obj == 'push' || obj == 'note_commit':
                return get_user_keyword(users)
            elif obj == 'issue':
                return get_user_issue_labels(users)
            elif obj == 'note_issue'
                return get_user_comment_label(users)
            else:
                raise NameError('Type not exists')

    def get_user_keywords(self, users: list) -> list:
        return self._mongofacade.get_match_keywords(users,
            self._message['title']
        )

    def get_user_issue_labels(self, users: list) -> list:    
        return self._mongofacade.get_match_labels(users,
            self._message['labels']
        )

    def get_user_comment_labels(self, users: list) -> list:
        labels = []
        # codice con richiesta http

        return self._mongofacade.get_match_labels(users, labels)


class RedmineProcessor(Processor):

    def filter_users_by_topic(self, users: list, obj: str) -> list:
        try:
            if obj == 'issue':
                raise NameError('Type not exists')

        return return self._mongofacade.get_match_labels(users,
            [self._message['labels']]
        )

