from abc import ABC, abstractmethod

import pymongo


class MongoAdapter(ABC):

    @property
    @abstractmethod
    def instance(self):
        pass


class MongoDBImpl(MongoAdapter):

    class MongoSingleton:

        def __init__(
                self,
                db: str,
                mongo_client=pymongo.MongoClient('localhost', 27017)
        ):
            self._client = mongo_client
            print('Connessione stabilita.')
            self._db = self._client[db]

        def create(
                self, document: dict, collection: str,
        ) -> pymongo.collection.InsertOneResult:
            """Aggiunge il documento `document` alla collezione
            `collection`, se non è già presente. Restituisce un
            `InsertOneResult`.
            """
            return MongoDBImpl.instance._db[collection].insert_one(document)

        def read(
                self, collection_name: str
        ) -> pymongo.collection.Collection:
            """Restituisce la collezione con il nome passato come
            argomento."""
            return MongoDBImpl.instance._db[collection_name]

        def delete(
                self, filter: dict, collection: str
        ) -> pymongo.collection.DeleteResult:
            """Rimuove un documento che corrisponde al
            `filter`, se presente, e restituisce il risultato.
            Restituisce un `DeleteResult`.
            """
            return MongoDBImpl.instance._db[collection].delete_one(filter)

    _INSTANCE = MongoSingleton('butterfly')

    # def __init__(self):
    #     if not MongoDBImpl.instance:
    #         MongoDBImpl.instance = MongoDBImpl.MongoSingleton('butterfly')

    @property
    def instance(self):
        return MongoDBImpl._INSTANCE
