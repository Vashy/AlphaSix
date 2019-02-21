import pymongo

class MyMongoClient():
    _client
    
    def __init__(self, server = 'localhost', port = 27017):
        print('Opening connection ...')
        self._client = pymongo.MongoClient(server, port)
    
    def insert(self, database, collection, documents):
        self._client[database][collection].insert_many(documents)
        
    def select(self, database, collection, query):
        return self._client[database][collection].find(query)