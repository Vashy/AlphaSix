from gestore_personale.processor import Processor


class GitlabProcessor(Processor):

    def _filter_users_by_topic(self, users: list, kind: str) -> list:
        """
        Cerca gli utenti disponibili nella data della notifica iscritti ai
        topic della segnalazione
        :param users: lista di utenti appartenenti al progetto della
            segnalazione e disponibili nel giorno della segnalazione
        :param kind: tipologia della segnalazione per GitLab
        :return: lista di utenti iscritti a quel topic
        """

        if kind == 'push':
            full_string = ''
            # Concatena i messaggi di tutti i commit
            for commit in self._message['commits']:
                full_string = ' '.join([
                    full_string,
                    commit['message'],
                ])
            return self._mongofacade.get_match_keywords(
                users,
                self._message['project_id'],
                full_string,
            )

        if kind == 'commit-note':
            return self._mongofacade.get_match_keywords(
                users,
                self._message['project_id'],
                self._message['description'],
            )

        # Se la segnalazione consiste in una issue
        elif kind == 'issue':
            self._check_labels(self._message['labels'])
            return self._mongofacade.get_match_labels(
                users,
                self._message['project_id'],
                self._message['labels'],
            )

        # Se la segnalazione consiste nel commento di una issue
        elif kind == 'issue-note':
            self._check_labels(self._message['labels'])
            labels = self._message['labels']
            # codice con richiesta http per recuperare le label della issue commentata

            return self._mongofacade.get_match_labels(
                users,
                self._message['project_id'],
                labels,
            )
        else:
            raise NameError('Type doesn\'t exist')

    def _check_labels(self, labels: list):
        """Guarda se le label della segnalazione
        legate al progetto indicati esistono.
        Funzione ausiliaria per `_filter_user_by_project`.
        Lavora come RedmineProcessor._check_label
        :param labels: lista delle label della segnalazione
        """
        project = self._message['project_id']
        label_project = self._mongofacade.get_label_project(project)
        for label in labels:
            if label not in label_project:
                self._mongofacade.insert_label_by_project(project, label)


class RedmineProcessor(Processor):

    def _filter_users_by_topic(self, users: list, kind: str) -> list:
        """
        Cerca gli utenti disponibili nella data della notifica iscritti ai
        topic della segnalazione
        :param users: lista di utenti appartenenti al progetto della
            segnalazione e disponibili nel giorno della segnalazione
        :param kind: tipologia della segnalazione per redmine
        :return: lista di utenti iscritti a quel topic
        """
        # L'unico tipo di segnalazioni possono essere 'issue'
        if kind != 'issue':
            raise NameError('Type not exists')

        self._check_labels(self._message['labels'])
        return self._mongofacade.get_match_labels(
            users,
            self._message['project_id'],
            self._message['labels'],
        )

    def _check_labels(self, labels: list):
        """
        Guarda se le label della segnalazione legate al progetto indicati
        esistono

        :param labels: lista delle label della segnalazione
        """
        project = self._message['project_id']
        label_project = self._mongofacade.get_label_project(project)
        for label in labels:
            if label not in label_project:
                self._mongofacade.insert_label_by_project(project, label)
