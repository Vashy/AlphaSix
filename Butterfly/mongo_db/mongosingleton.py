from abc import ABC, abstractmethod

import pymongo


class MongoAdapter(ABC):

    @abstractmethod
    def getInstance(self):
        pass

    @abstractmethod
    def create(
            self, document: dict, collection: str
    ) -> pymongo.collection.InsertOneResult:
        pass

    @abstractmethod
    def read(
            self, collection_name: str
    ) -> pymongo.collection.Collection:
        pass

    @abstractmethod
    def delete(
            self, filter: dict, collection: str
    ) -> pymongo.collection.DeleteResult:
        pass


class MongoDBImpl(MongoAdapter):

    class MongoSingleton:

        def __init__(self, db: str, server='localhost', port=27017):
            print('Apertura connessione ...')
            self._client = pymongo.MongoClient(server, port)
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

    instance = None

    def __init__(self, arg):
        if not MongoDBImpl.instance:
            MongoDBImpl.instance = MongoDBImpl.MongoSingleton('butterfly')

    def getInstance(self):
        return MongoDBImpl.instance
