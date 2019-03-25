class MongoFacade (DBUser, DBProject):

    def __init__(self):
        self._mongo_users = MongoUsers()
        self._mongo_projects = MongoProjects()

    def insert_user(self, **fields):
        pass
        
    def delete_user(self, user: str):
        pass
    
    def update_user_name(self, user: str, name: str):
        pass
    
    def update_user_surname(self, user: str, surname: str):
        pass
        
    def update_user_telegram(self, user: str, telegram: str):
        pass

    def update_user_email(self, user: str, email: str):
        pass
        
    def insert_user_project(self, user: str, project: str):
        pass
        
    def delete_user_project(self, user: str, project: str):
        pass
    
    def insert_project(self, project: str):
        pass
        
    def delete_project(self, url: str):
        pass
