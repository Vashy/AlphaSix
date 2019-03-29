from abc import ABC, abstractmethod

from mongo_db.facade import MongoFacade


class Processor():

    def __init__(self, message: dict, mongofacade: MongoFacade):  # aggiungere riferimento DB
        self._message = message
        self._mongofacade = mongofacade

    def notify(self, request_type, msg):
        for observer in self.observer_lst:
            observer.update(request_type, msg)   

    def template_method(self):
        progetto = self.check_project()       

    def check_project(self) -> str:
        urlProgetto = self._message['project_url']
        self._values = ['GET'][urlProgetto
        notify()
        if self
        self._values = ['POST'][urlProgetto]
        notify()
        return urlProgetto

    def get_state(self):
        return self._values    
