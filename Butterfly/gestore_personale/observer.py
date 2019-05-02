from abc import ABC, abstractmethod


class Observer(ABC):

    @abstractmethod
    def update(self, resource: str, request_type: str, url: str, msg: str):
        pass


class Subject(ABC):

    def addObserver(self, obs: Observer):
        if not hasattr(self, '_lst'):
            self._lst = []
        if obs not in self._lst:
            self._lst.append(obs)

    @abstractmethod
    def notify(self, request_type: str, resource: str, url: str, msg: str):
        pass
