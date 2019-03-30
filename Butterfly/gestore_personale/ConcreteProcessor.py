from gestore_personale.Processor import Processor


class GitlabProcessor(Processor):

    def _filter_users_by_topic(self, users: list, obj: str) -> list:
        """
        Cerca gli utendi disponibili nella data della notifica iscritti ai
        topic della segnalazione
        :param users: lista di utenti apparteneti al progetto della
            segnalazione e diponibili nel giorno della segnalazione
        :param obj: tipologia della segnalazione per GitLab
        :return: lista di utenti iscritti a quel topic
        """
        # Se la segnalazione consiste in un push o nel commento di un commit.
        # Le due segnazioni vengono considerate allo stesso modo
        if obj == 'push' or obj == 'note_commit':
            return self._mongofacade.get_match_keywords(users,
                self._message['title']
            )
        # Se la segnalazione consiste in una issue
        elif obj == 'issue':
            return self._mongofacade.get_match_labels(users,
                self._message['labels']
            )
        # Se la segnalazione consiste nel commento di una issue
        elif obj == 'note_issue':
            labels = []
            # codice con richiesta http per recuperare le label della issue commentata

            return self._mongofacade.get_match_labels(users,
                labels
            )
        else:
            raise NameError('Type not exists')


class RedmineProcessor(Processor):

    def _filter_users_by_topic(self, users: list, obj: str) -> list:
        """
        Cerca gli utendi disponibili nella data della notifica iscritti ai
        topic della segnalazione
        :param users: lista di utenti apparteneti al progetto della
            segnalazione e diponibili nel giorno della segnalazione
        :param obj: tipologia della segnalazione per redmine
        :return: lista di utenti iscritti a quel topic
        """
        # L'unico tipo di segnalazioni possono essere 'issue'
        if obj != 'issue':
            raise NameError('Type not exists')

        return self._mongofacade.get_match_labels(users,
            [self._message['labels']]
        )
