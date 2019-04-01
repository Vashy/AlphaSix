# Usage: python3 __file__.py

from os import urandom
from abc import ABC, abstractmethod
import pathlib

from flask import Flask, request, session, make_response
import flask_restful

from mongo_db.facade import MongoFacade
from mongo_db.creator import MongoFacadeCreator

root = (pathlib.Path(__file__).parent / 'public_html').resolve()


class Observer(ABC):

    @abstractmethod
    def update(self, msg: dict):
        pass


class Subject(ABC):

    def addObserver(self, obs: Observer):
        if not hasattr(self, '_lst'):
            self._lst = []
        if obs not in self._lst:
            self._lst.append(obs)

    @abstractmethod
    def notify(self, request_type: str, resource: str, msg: str):
        pass


class FinalMeta(type(Subject), type(flask_restful.Resource)):
    pass


class Resource(Subject, flask_restful.Resource, metaclass=FinalMeta):

    def __init__(self):
        super(Resource, self).__init__()
        self._response = None

    def notify(self, request_type: str, resource: str, msg: str):
        for obs in self._lst:
            return obs.update(request_type, resource, msg)


class Panel(Resource):

    def get(self):
        """Restituisce il pannello di controllo

        Usage example:
            `curl http://localhost:5000/panel`
        """
        return make_response(
            self.notify('panel', 'GET', self._response),
            200
        )


class User(Resource):

    def get(self):
        """Restituisce lo user con l'id specificato

        Usage example:
            `curl http://localhost:5000/user/1`
        """
        return self.notify('user', 'GET', self._response)

    def post(self) -> dict:
        """Modifica un user

        Usage example:
            `curl http://localhost:5000/users -X POST -d "data=some data"`
        """
        data = request.get_json(force=True)
        return self.notify('user', 'POST', data)


class Preference(Resource):

    def get(self):
        """Restituisce le preferenze dello user con l'id specificato

        Usage example:
            `curl http://localhost:5000/preference/1`
        """
        return self.notify('preference', 'GET', self._response)

    def post(self) -> dict:
        """Modifica le preferenze dello user indicato nel corpo della request

        Usage example:
            `curl http://localhost:5000/users -X POST -d "data=some data"`
        """
        data = request.get_json(force=True)
        return self.notify('user', 'POST', data)


class Controller(Observer):

    def __init__(self, api: flask_restful.Api, model: MongoFacade):
        self.model = model
        self.api = api

        self.user = User
        self.panel = Panel
        self.preference = Preference

        self.api.add_resource(
            self.panel, '/'
        )

        self.api.add_resource(
            self.user, '/user'
        )

        self.api.add_resource(
            self.preference, '/preference'
        )

        self.user.addObserver(self.user, obs=self)
        self.panel.addObserver(self.panel, obs=self)
        self.preference.addObserver(self.preference, obs=self)

    def _checkSession(self):
        return 'userid' in session

    def access(self):
        file = root / 'access.html'
        page = file.read_text()
        page = page.replace('*access*', '')
        page = page.replace('*userid*', '')
        return page

    def panel(self, request_type: str, msg: str):
        if request_type == 'GET':
            pass
        elif request_type == 'POST':
            pass

    def user(self, request_type: str, msg: str):
        if request_type == 'GET':
            pass
        elif request_type == 'POST':
            pass

    def preference(self, request_type: str, msg: str):
        if request_type == 'GET':
            pass
        elif request_type == 'POST':
            pass

    def update(self, resource: str, request_type: str, msg: str):
        if self._checkSession():
            if resource == 'panel':
                return self.panel(request_type, msg)
            elif resource == 'user':
                return self.user(request_type, msg)
            elif resource == 'preference':
                return self.preference(request_type, msg)
        return self.access()


def main():
    flask = Flask(__name__)
    flask.secret_key = urandom(16)
    Controller(
        flask_restful.Api(flask),
        MongoFacadeCreator().instantiate()
    )

    flask.run(debug=True)


if __name__ == "__main__":
    main()
