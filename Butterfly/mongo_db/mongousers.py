import pprint
import copy

import pymongo

class MongoUsers:

    def __init__(self):
        self._mongo = MongoSingleton()
