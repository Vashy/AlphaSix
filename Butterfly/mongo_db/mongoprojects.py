from mongo_db.mongointerface import MongoInterface
from mongo_db.mongosingleton import MongoAdapter


class MongoProjects(MongoInterface):

    def __init__(self):
        self._mongo = MongoAdapter()

    def projects(self, filter={}):
        """Restituisce un `Cursor` che corrisponde al `filter` passato
        alla collezione `projects`.
        Per accedere agli elementi del cursore, è possibile iterare con
        un `for .. in ..`, oppure usare il subscripting `[i]`.
        """
        return self.collection('projects').find(filter)

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
        result = self._mongo.db['projects'].insert_one(project)
        return result

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
