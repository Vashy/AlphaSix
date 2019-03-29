from mongo_db.facade import MongoFacade
from mongo_db.users import MongoUsers
from mongo_db.projects import MongoProjects


class MongoFacadeCreator():

    def instantiate(self):  # NB: dipendenza nascosta
        return MongoFacade(MongoUsers(), MongoProjects())
