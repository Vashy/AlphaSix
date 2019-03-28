from abc import ABC, abstractmethod


class Processor(ABC):

    def __init__(self, message: dict):
        self._message = message

    def template_method(self):
        progetto = check_project()


    def check_project(self)
