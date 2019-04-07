from gestore_personale.Processor import Processor


class GitlabProcessor(Processor):

    def _filter_users_by_topic(self, users: list, obj: str) -> list:
        """
        Cerca gli utenti disponibili nella data della notifica iscritti ai
        topic della segnalazione
        :param users: lista di utenti appartenenti al progetto della
            segnalazione e disponibili nel giorno della segnalazione
        :param obj: tipologia della segnalazione per GitLab
        :return: lista di utenti iscritti a quel topic
        """
        # Se la segnalazione consiste in un push o nel commento di un commit.
        # Le due segnazioni vengono considerate allo stesso modo
        if obj == 'push' or obj == 'note_commit':
            return self._mongofacade.get_match_keywords(
                users,
                self._message['title']
            )
        # Se la segnalazione consiste in una issue
        elif obj == 'issue':
            self._check_labels(self._message['labels'])
            return self._mongofacade.get_match_labels(
                users,
                self._message['labels']
            )
        # Se la segnalazione consiste nel commento di una issue
        elif obj == 'note_issue':
            self._check_labels(self._message['labels'])
            labels = []
            # codice con richiesta http per recuperare le label della issue commentata

            return self._mongofacade.get_match_labels(
                users,
                labels
            )
        else:
            raise NameError('Type not exists')

    def _check_labels(self, labels: list):
        """
        Guarda se le label della segnalazione legate al progetto indicati esistono.
        Funzione ausiliaria per _filter_user_by_project. Lavora come RedmineProcessor._check_label
        :param labels: lista delle label della segnalazione
        """
        project = self._message['project_id']
        label_project = self._mongofacade.get_label_project(project)
        for label in labels:
            if label not in label_project:
                self._mongofacade.insert_label_by_project(label, project)



class RedmineProcessor(Processor):

    def _filter_users_by_topic(self, users: list, obj: str) -> list:
        """
        Cerca gli utenti disponibili nella data della notifica iscritti ai
        topic della segnalazione
        :param users: lista di utenti appartenenti al progetto della
            segnalazione e disponibili nel giorno della segnalazione
        :param obj: tipologia della segnalazione per redmine
        :return: lista di utenti iscritti a quel topic
        """
        # L'unico tipo di segnalazioni possono essere 'issue'
        if obj != 'issue':
            raise NameError('Type not exists')

        self._check_labels(self._message['labels'])
        return self._mongofacade.get_match_labels(
            users,
            [self._message['labels']]
        )

    def _check_labels(self, labels: list):
        """
        Guarda se le label della segnalazione legate al progetto indicati esistono
        :param labels: lista delle label della segnalazione
        """
        project = self._message['project_id']
        label_project = self._mongofacade.get_label_project(project)
        for label in labels:
            if label not in label_project:
                self._mongofacade.insert_label_by_project(label, project)
