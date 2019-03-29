from abc import ABC, abstractmethod


class Observer(ABC):

    @abstractmethod
    def update(self, msg: dict):
        pass


class MongoFacade(Observer):

    def __init__(self, mongo_users, mongo_projects):
        self._users = mongo_users
        self._projects = mongo_projects

    def insert_user(self, **fields):
        self._users.create(fields)
        
    def read_user(self, user: str):
        return self._users.read(user)
        
    def users(self, mongofilter={}):
        return self._proj_users.users(mongofilter)

    def delete_user(self, user: str):
        self._users.delete(user)

    def update_user_name(self, user: str, name: str):
        self._users.update_user_name(user, name)

    def update_user_surname(self, user: str, surname: str):
        self._users.update_user_surname(user, surname)

    def update_user_telegram(self, user: str, telegram: str):
        self._users.update_user_telegram(user, telegram)

    def update_user_email(self, user: str, email: str):
        self._users.update_user_email(user, email)

    def insert_user_project(self, user: str, project: str):
        self._users.insert_user_project(user, project)

    def delete_user_project(self, user: str, project: str):
        self._users.delete_user_project(user, project)

    def insert_project(self, project: str):
        self._projects.create(project)

    def delete_project(self, project: str):
        self._projects.delete(project)

    def projects(self, filter={}):
        return self._projects.projects(filter)

    # TODO
    def get_project_by_url(self, url: str) -> bool:
        # Faccio una search del progetto
        # Se c'è torno true
        pass

    # TODO
    def get_users_available(self, url: str) -> list:
        # Dato un progetto, cerco tutti
        # Gli utenti disponibili oggi
        pass

