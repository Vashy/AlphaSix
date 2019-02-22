import pymongo


class DBConnection(object):
    """Classe con la funzionalità di connessione e sconnessione
    a un database. Dovrebbe essere usata in un costrutto with,
    in modo da automatizzare il rilascio della risorsa.

    e.g.:
    with DBConnection('nomedb'):
        # ...

    Arguments:
        db -- Nome del database a cui connettersi
        server -- server mongo a cui connettersi
        port -- porta specifica in cui gira il processo mongod
    """
    def __init__(self, db: str, server='localhost', port=27017):
        print('Apertura connessione ...')
        self._client = pymongo.MongoClient(server, port)
        print('Connessione stabilita.')
        self._db = self._client[db]

    # Entrata nel costrutto with
    def __enter__(self):
        return self

    # Uscita dal costrutto with
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def drop_collections(self, *collections):
        """Elimina le collezioni passate come argomenti,
        solo se presenti.
        """
        for collection in collections:
            if collection in self.db.list_collection_names():
                self.db.drop_collection(collection)
                print(f'Dropped collection {collection}')

    @property
    def db(self):
        return self._db

    def close(self):
        """Chiude la connessione col client mongo.
        """
        print('Chiusura connessione ...')
        self._client.close()
        print('Connessione chiusa.')
