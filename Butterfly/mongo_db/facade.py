class MongoFacade:

    def __init__(self, mongo_users, mongo_projects):
        self._mongo_users = mongo_users
        self._mongo_projects = mongo_projects

    def insert_user(self, **fields):
        self._mongo_users.create(fields)

    def delete_user(self, user: str):
        self._mongo_users.delete(user)

    def update_user_name(self, user: str, name: str):
        self._mongo_users.update_user_name(user, name)

    def update_user_surname(self, user: str, surname: str):
        self._mongo_users.update_user_surname(user, surname)

    def update_user_telegram(self, user: str, telegram: str):
        self._mongo_users.update_user_telegram(user, telegram)

    def update_user_email(self, user: str, email: str):
        self._mongo_users.update_user_email(user, email)

    def insert_user_project(self, user: str, project: str):
        self._mongo_users.insert_user_project(user, project)

    def delete_user_project(self, user: str, project: str):
        self._mongo_users.delete_user_project(user, project)

    def insert_project(self, project: str):
        self._mongo_projects.create(project)

    def delete_project(self, project: str):
        self._mongo_projects.delete(project)
