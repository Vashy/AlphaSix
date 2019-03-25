from abc import ABC, abstractmethod

class DBUser(ABC):

    @abstractmethod
    def insert_user(self, **fields):
        pass
        
    @abstractmethod
    def delete_user(self, user: str):
        pass
    
    @abstractmethod   
    def update_user_name(self, user: str, name: str):
        pass
    
    @abstractmethod
    def update_user_surname(self, user: str, surname: str):
        pass
        
    @abstractmethod   
    def update_user_telegram(self, user: str, telegram: str):
        pass

    @abstractmethod  
    def update_user_email(self, user: str, email: str):
        pass
        
    @abstractmethod
    def insert_user_project(self, user: str, project: str):
        pass
        
    @abstractmethod
    def delete_user_project(self, user: str, project: str):
        pass
        
class DBProject(ABC):
    
    @abstractmethod
    def insert_project(self, project: str):
        pass
        
    @abstractmethod
    def delete_project(self, url: str):
        pass
