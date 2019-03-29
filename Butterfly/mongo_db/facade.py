from abc import ABC, abstractmethod


class Observer(ABC):

    @abstractmethod
    def update(self, msg: dict):
        pass


class Subject(ABC):

    def __init__(self):
        self.lst = []

    def notify(self):
        for obs in self.lst:
            obs.update()
            
    def add_observer(self, obs: Observer):
        self.lst.append(obs)


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

    def project_exists(self, url: str) -> bool:
        return self._projects.exists(url)

    def get_users_available(self, url: str) -> list:
        return self._users.get_users_available(url)

    # TODO
    def get_users_max_priority(self, url: str) -> list:
        # Dato un progetto, ritorno la lista di
        # utenti disponibili oggi di priorità maggiore
        # (la lista di ritorno contiene gli ID del DB)
        pass

    # TODO
    def get_user_telegram(self, userID: str) -> str:
        # Ritorno il telegram dell'utente (se presente)
        # altrimenti 0/None/NULL
        pass

    # TODO
    def get_user_email(self, userID: str) -> str:
        # Ritorno la mail dell'utente (se presente)
        # altrimenti 0/None/NULL
        pass
