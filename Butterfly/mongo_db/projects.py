from mongo_db.singleton import MongoAdapter


class MongoProjects:

    def __init__(self):
        self._mongo = MongoAdapter()

    def projects(self, filter={}):
        """Restituisce un `Cursor` che corrisponde al `filter` passato
        alla collezione `projects`.
        Per accedere agli elementi del cursore, è possibile iterare con
        un `for .. in ..`, oppure usare il subscripting `[i]`.
        """
        return self._mongo.collection('projects').find(filter)
        
    def exists(self, project: str) -> bool:
        """Restituisce `True` se l'`id` di un utente
        (che può essere Telegram o Email) è salvato nel DB.
        """
        count = self._mongo.collection('projects').count_documents({
            {'url': project}
        })
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
        
    def read(
        self, url: str
    ) -> bool:
        """Restituisce il progetto corrispondente a `url`.
        
        Raises:
        `AssertionError` -- se `url` non è presente nel DB.
        """
        assert self.exists(url), f'User {id} inesistente'

        return self.projects({
            {'url': url},
        })[0]
        
        
