from abc import ABC, abstractmethod

from mongo_db.facade import MongoFacade


class Processor():

    def __init__(self, message: dict, mongofacade: MongoFacade):  # aggiungere riferimento DB
        self.__message = message
        self.__mongofacade = mongofacade

    def template_method(self) -> dict:
        progetto = self.check_project()  # URL progetto
        obj = self.__message['object_kind']  # Issue o push ecc
        # Dict di tutti gli utenti disponibili oggi nel progetto
        utenti_disponibili = self.get_involved_users()
        utenti_interessati = self.filter_users_by_topic(
            utenti_disponibili, obj
        )

    def check_project(self) -> str:
        urlProgetto = self._message['project_url']
        # Vediamo nel DB se il prog c'è
        exists_project = self.__mongofacade.get_project_by_url(urlProgetto)
        # Se non c'è lo aggiungiamo
        if not exists_project:
            self.__mongofacade.insert_project(urlProgetto)
        return urlProgetto

    # def get_users_from_project(self, project: str) -> dict:
    #     return self.__mongofacade.get_users_project(project)

    def get_involved_users(self, project: str) -> list:
        return self.__mogofacade.get_users_available(project)

    @abstractmethod
    def filter_users_by_topic(self, users: list, obj: str) -> list:
        pass


