from mongo_db.users import MongoUsers
from mongo_db.projects import MongoProjects


class MongoFacade():

    def __init__(
        self,
        mongo_users: MongoUsers,
        mongo_projects: MongoProjects
    ):
        self._users = mongo_users
        self._projects = mongo_projects

    def insert_user(self, **fields):
        self._users.create(fields)

    def read_user(self, user: str):
        return self._users.read(user)

    def users(self, mongofilter={}):
        return self._users.users(mongofilter)

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

    def projects(self, mongofilter={}):
        return self._projects.projects(mongofilter)

    def insert_label_by_project(self, label: str, project: str):
        self._projects.insert_label_by_project(label, project)

    def insert_keyword_by_project(self, keyword: str, project: str):
        self._projects.insert_keyword(keyword, project)

    def user_exists(self, userid: str):
        return self._users.exists(userid)

    def user_has_email(self, email: str):
        return self._users.user_has_email(email)

# Metodi per la ricerca dei dati

    def get_users_available(self, url: str) -> list:
        return self._users.get_users_available(url)

    def get_users_max_priority(self, url: str) -> list:
        return self._users.get_users_max_priority(url)

    def get_project_by_url(self, url: str) -> bool:
        return self._projects.exists(url)

    def get_user_telegram(self, userID: str) -> str:
        return self._users.get_user_telegram(userID)

    def get_user_email(self, userID: str) -> str:
        return self._users.get_user_email(userID)

    def get_match_keywords(self, users: list, commit: str) -> list:
        return self._users.get_match_keywords(users, commit)

    def get_match_labels(self, users: list, labels: list) -> list:
        return self._users.get_match_labels(users, labels)

    # TODO : relativamente a quel progetto
    def get_users_from_list_with_max_priority(self, users: list, url: str) -> list:
        # filtra, tra gli utenti dati, solo quelli che hanno la priorità
        # maggiore
        # (è diverso da 'get_users_max_priority' perchè non li vogliamo tutti)
        pass

    def get_label_project(self, project: str) -> list:
        return self._projects.labels(project)
