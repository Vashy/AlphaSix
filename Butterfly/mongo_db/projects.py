import copy

import pymongo

from mongo_db.singleton import MongoSingleton

apps = [
    'gitlab',
    'redmine',
]


class MongoProjects:

    def __init__(self, mongo: MongoSingleton):
        self._mongo = mongo

    def projects(self, mongofilter={}):
        """Restituisce un `Cursor` che corrisponde al `filter` passato
        alla collezione `projects`.
        Per accedere agli elementi del cursore, è possibile iterare con
        un `for .. in ..`, oppure usare il subscripting `[i]`.
        """
        return self.collection.find(mongofilter)

    def exists(self, project: str) -> bool:
        """Restituisce `True` se l'`id` di un utente
        (che può essere Telegram o Email) è salvato nel DB.
        """
        count = self.collection.count_documents({
            '$or': [
                {'_id': project},
                {'url': project},
            ]
        })
        return count != 0

    @property
    def collection(self):
        return self._mongo.read('projects')

    def create(
        self,
        **fields,
    ) -> pymongo.results.InsertOneResult:
        """Aggiunge il documento `project` alla collezione `projects`,
        se non già presente, e restituisce il risultato, che può essere
        `None` in caso di chiave duplicata.

        Raises:
        `pymongo.errors.DuplicateKeyError`
        """

        # Valori di default dei campi
        defaultfields = {
            '_id': None,
            'url': None,
            'name': None,
            'app': None,
            'topics': [],
        }

        # Copia profonda del dict default
        new_project = copy.copy(defaultfields)

        # Aggiorna i valori di default con quelli passati al costruttore
        for key in new_project:
            if key in fields:
                new_project[key] = fields.pop(key)

        assert not fields, 'Sono stati inseriti campi non validi'
        assert new_project['url'] is not None, \
            'inserire il campo `url`'
        assert new_project['app'] is not None, \
            'inserire il campo `app`'
        assert new_project['app'] in apps, '`app` non riconosciuta'

        # L'ultimo carattere non deve essere '/'
        if new_project['url'][-1:] == '/':
            new_project['url'] = new_project['url'][:-1]

        assert not self.exists(new_project['url'])

        # Via libera all'aggiunta al DB
        if new_project['_id'] is None:  # Per non mettere _id = None sul DB
            del new_project['_id']

        return self._mongo.create(
            new_project,
            'projects'
        )

    def delete(
        self, url: str
    ) -> pymongo.results.DeleteResult:
        """Rimuove un documento che corrisponda a `url` o `_id` del progetto,
        se presente, e restituisce il risultato.
        """
        return self._mongo.delete({
            '$or': [
                {'_id': url},
                {'url': url},
            ],
        },
            'projects'
        )

    def read(
        self, project: str
    ) -> dict:
        """Restituisce il progetto corrispondente a `project`.

        Raises:
        `AssertionError` -- se `project` non è presente nel DB.
        """
        assert self.exists(project), f'Project {project} inesistente'

        return self.projects({
            '$or': [
                {'_id': project},
                {'url': project},
            ]
        }).next()

    def update_app(self, project: str, app: str) -> dict:
        """Aggiorna il campo `app` del progetto corrispondente a
        `url` con il valore `app`.
        """
        assert self.exists(project), f'Project {project} inesistente'
        assert app in apps, f'app "{app}" non riconosciuta'

        return self.collection.find_one_and_update(
            {
                '$or': [
                    {'_id': project},
                    {'url': project},
                ]},
            {
                '$set': {
                    'app': app,
                }
            }
        )

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
