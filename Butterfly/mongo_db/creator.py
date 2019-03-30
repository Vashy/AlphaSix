from mongo_db.singleton import MongoDBImpl
from mongo_db.facade import MongoFacade
from mongo_db.users import MongoUsers
from mongo_db.projects import MongoProjects


class MongoDBImplCreator():

    def instantiate(self):  # NB: dipendenza nascosta
        return MongoDBImpl()


class MongoFacadeCreator():

    def instantiate(self):  # NB: dipendenza nascosta
        return MongoFacade(
            MongoUsers(MongoDBImplCreator().instantiate()),
            MongoProjects(MongoDBImplCreator().instantiate())
        )
