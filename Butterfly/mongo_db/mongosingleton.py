class MongoDBImpl:

    class MongoSingleton:
    
        def __init__(self, db: str, server='localhost', port=27017):
            print('Apertura connessione ...')
            self._client = pymongo.MongoClient(server, port)
            print('Connessione stabilita.')
            self._db = self._client[db] 
    
    instance = None
    
    def __init__(self, arg):
        if not MongoDBImpl.instance:
            MongoDBImpl.instance = MongoDBImpl.MongoSingleton()
            
    def getInstance(self):
        return instance
