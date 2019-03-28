class MongoFacade:

    def __init__(self, mongo_users, mongo_projects):
        self._mongo_users = mongo_users
        self._mongo_projects = mongo_projects

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
