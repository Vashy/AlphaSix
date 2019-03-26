import pprint
import copy

import pymongo

class MongoProjects:

    def __init__(self):
        self._mongo = MongoSingleton()
