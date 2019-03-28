from abc import ABC, abstractmethod


class Processor(Subject):

    def __init__(self, message: dict): # aggiungere riferimento DB
        self._message = message

    def template_method(self):
        progetto = self.check_project()        

    def check_project(self) -> str:
        urlProgetto = self._message['url']

        return urlProgetto
