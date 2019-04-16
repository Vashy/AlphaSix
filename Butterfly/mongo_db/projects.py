from mongo_db.singleton import MongoSingleton


class MongoProjects:

    def __init__(self, mongo: MongoSingleton):
        self._mongo = mongo

    def projects(self, mongofilter={}):
        """Restituisce un `Cursor` che corrisponde al `filter` passato
        alla collezione `projects`.
        Per accedere agli elementi del cursore, è possibile iterare con
        un `for .. in ..`, oppure usare il subscripting `[i]`.
        """
        return self._mongo.read('projects').find(mongofilter)

    def exists(self, project: str) -> bool:
        """Restituisce `True` se l'`id` di un utente
        (che può essere Telegram o Email) è salvato nel DB.
        """
        count = self._mongo.read('projects').count_documents(
            {'url': project}
        )
        return count != 0

    def create(self, project: dict):
        """Aggiunge il documento `project` alla collezione `projects`,
        se non già presente, e restituisce il risultato, che può essere
        `None` in caso di chiave duplicata.

        Raises:
        `pymongo.errors.DuplicateKeyError`
        """
        # L'ultimo carattere non deve essere '/'
        if project['url'][-1:] == '/':
            project['url'] = project['url'][:-1]
        # Tenta l'aggiunta del progetto, raises DuplicateKeyError
        return self._mongo.db['projects'].insert_one(project)

    def delete(
        self, url: str
    ):
        """Rimuove un documento che corrisponda a `url`,
        se presente, e restituisce il risultato.
        """
        return self._mongo.delete({
                'url': url,
            },
            'projects'
        )

    def read(
        self, url: str
    ) -> dict:
        """Restituisce il progetto corrispondente a `url`.

        Raises:
        `AssertionError` -- se `url` non è presente nel DB.
        """
        assert self.exists(url), f'Project {id} inesistente'

        return self.projects(
            {'url': url},
        ).next()

    def keywords(self, project: str) -> list:
        """Restituisce una lista contenente le parole chiave corrispondenti
        all'`id`: url del progetto
        """
        cursor = self.projects(
            {'url': project}
        )
        return cursor[0]['keywords']

    def labels(self, project: str) -> list:
        """Restituisce una lista contenente le labels corrispondenti
        all'`id`: url del progetto
        """
        cursor = self.projects(
            {'url': project}
        )
        return cursor.next()['topics']

    def insert_keyword_by_project(self, keyword: str, project: str):
        """Inserisce una nuova keyword nel progetto
        """
        keywords = self.keywords(project)
        keywords.append(keyword)
        self._mongo.db['projects'].update(
            {'url': project},
            {
                '$set':
                {'keywords': keywords}
            }
        )

    def insert_label_by_project(self, label: str, project: str):
        """Inserisce una nuova label nel progetto
        """
        labels = self.labels(project)
        labels.append(label)
        self._mongo.db['projects'].update(
            {'url': project},
            {
                '$set':
                {'topics': labels}
            }
        )
