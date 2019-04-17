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
        self._users.create(**fields)

    def read_user(self, user: str):
        return self._users.read(user)

    def read_project(self, project: str):
        return self._projects.read(project)

    def users(self):
        return self._users.users()

    def projects(self):
        return self._projects.projects()

    def delete_user(self, user: str):
        return self._users.delete(user)

    def update_user_name(self, user: str, name: str):
        self._users.update_name(user, name)

    def update_user_surname(self, user: str, surname: str):
        self._users.update_surname(user, surname)

    def update_user_telegram(self, user: str, telegram: str):
        self._users.update_telegram(user, telegram)

    def update_user_email(self, user: str, email: str):
        self._users.update_email(user, email)

    def update_user_preference(self, user: str, preference: str):
        self._users.update_user_preference(user, preference)

    def add_user_project(self, user: str, project: str):
        self._users.add_project(user, project)

    def add_user_topics(self, user: str, project: str, topics: list):
        self._users.add_labels(user, project, topics)

    def add_user_keywords(self, user: str, project: str, *keywords):
        self._users.add_keywords(user, project, *keywords)

    def remove_user_project(self, user: str, project: str):
        self._users.remove_project(user, project)

    def add_giorno_irreperibilita(
        self,
        user: str,
        year: int, month: int, day: int,
    ):
        self._users.add_giorno_irreperibilita(user, year, month, day)

    def remove_giorno_irreperibilita(
        self,
        user: str,
        year: int, month: int, day: int,
    ):
        self._users.remove_giorno_irreperibilita(user, year, month, day)

    def reset_user_topics(self, user: str, project: str):
        self._users.reset_labels(user, project)

    def reset_user_keywords(self, user: str, project: str):
        self._users.reset_keywords(user, project)

    def delete_user_project(self, user: str, project: str):
        self._users.delete_user_project(user, project)

    def insert_project(self, **project):
        self._projects.create(**project)

    def delete_project(self, project: str):
        self._projects.delete(project)

    def insert_label_by_project(self, project: str, label: str):
        self._projects.add_topics(project, label)

    def insert_keyword_by_project(self, keyword: str, project: str):
        self._projects.insert_keyword(keyword, project)

    def user_exists(self, userid: str):
        return self._users.exists(userid)

# Metodi per la ricerca dei dati

    def get_users_available(self, url: str) -> list:
        return self._users.get_users_available(url)

    def get_users_max_priority(self, url: str) -> list:
        return self._users.get_users_max_priority(url)

    def set_user_priority(
        self, user: str, project: str, priority: int
    ) -> dict:
        return self._users.set_priority(user, project, priority)

    def get_project_by_url(self, url: str) -> bool:
        return self._projects.exists(url)

    def get_user_telegram_from_id(self, userID: str) -> str:
        return self._users.get_user_telegram_from_id(userID)

    def get_user_email_from_id(self, userID: str) -> str:
        return self._users.get_user_email_from_id(userID)

    def get_user_telegram(self, user: str) -> str:
        return self._users.get_user_telegram(user)

    def get_user_email(self, user: str) -> str:
        return self._users.get_user_email(user)

    def get_match_keywords(
        self,
        users: list,
        project: str,
        commit: str,
    ) -> list:
        return self._users.get_match_keywords(users, project, commit)

    def get_match_labels(
        self,
        users: list,
        project: str,
        labels: list,
    ) -> list:
        return self._users.get_match_labels(users, project, labels)

    def get_users_from_list_with_max_priority(
        self,
        users: list,
        url: str,
    ) -> list:
        # filtra, tra gli utenti dati, solo quelli che hanno la priorità
        # maggiore
        # (è diverso da 'get_users_max_priority' perchè non li vogliamo tutti)
        self._users.filter_max_priority(users, url)

    def get_label_project(self, project: str) -> list:
        return self._projects.topics(project)

    def get_user_projects(self, user: str) -> dict:
        return self._users.get_projects(user)
