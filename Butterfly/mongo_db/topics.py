from mongo_db.mongointerface import MongoInterface
from mongo_db.mongosingleton import MongoAdapter


class MongoTopics (MongoInterface):

    def __init__(self):
        self._mongo = MongoAdapter().getInstance()

    def create(self, label: str, project: str):
        """Aggiunge il documento `topic`, corrispondente alla coppia
        `label`-`project`, alla collezione `topics` se
        non già presente e restituisce il risultato, che può essere
        `None` in caso di chiave (`label`-`project`) duplicata.

        Raises:
        `pymongo.errors.DuplicateKeyError`
        """
        # L'ultimo carattere dell'url di project non deve essere '/'
        if project[-1:] == '/':
            project = project[:-1]

        try:  # Tenta l'aggiunta del topic al DB
            # Ottiene l'id massimo
            # TODO: DESCENDING è molto dipendente da pymongo...
            max_id = (
                self.collection('topics')
                    .find()
                    .sort('_id', -1)
                    .limit(1)[0]['_id']
            )

            result = self._mongo.db['topics'].insert_one({
                '_id': max_id+1,
                'label': label,
                'project': project,
            })
            return result

        except IndexError:  # Caso in cui nessun topic è presente
            result = self._mongo.db['topics'].insert_one({
                '_id': 0,
                'label': label,
                'project': project,
            })
            return result

        # except pymongo.errors.DuplicateKeyError as err:
        #     print(err)
        #     return None

    def delete(
            self,
            label: str,
            project: str,
    ):
        """Rimuove un documento che corrisponda alla coppia `label`-`project`,
        se presente, e restituisce il risultato.
        """
        return self._mongo.delete({
                'label': label,
                'project': project,
            },
            'topics',
        )
