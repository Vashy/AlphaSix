import pymongo


class DBConnection(object):
    def __init__(self, db, server='localhost', port=27017):
        print('Opening connection ...')
        self._client = pymongo.MongoClient(server, port)
        self._db = self._client[db]

    def __enter__(self):
        # print('Opening connection ...')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # print('Closing connection ...')
        self.close()

    # @property
    def db(self):
        return self._db

    def close(self):
        print('Closing connection ...')
        self._client.close()
