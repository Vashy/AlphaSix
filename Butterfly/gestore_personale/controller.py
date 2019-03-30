# Usage: python3 __file__.py

from abc import ABC, abstractmethod
import json

from flask import Flask, request
import flask_restful

from mongo_db.facade import MongoFacade
from mongo_db.creator import MongoFacadeCreator


class Observer(ABC):

    @abstractmethod
    def update(self, msg: dict):
        pass


class Resource(flask_restful.Resource):

    def __init__(self, obs: Observer):
        self._controller = obs
        self._response = None

    def notify(self, request_type: str, resource: str, msg: str):
        return self._controller.update(request_type, resource, msg)


class Access(Resource):

    def get(self):
        """Restitu==ce l'access page

        Usage example:
            `curl http://localhost:5000/access`
        """
        return self.notify('access', 'GET', self._response)

    def post(self) -> dict:
        """Fa accedere con lo user specificato nella richiesta post

        Usage example:
            `curl http://localhost:5000/access -X POST -d "data=some data"`
        """
        data = request.get_json(force=True)
        return self.notify('access', 'POST', data)


class Panel(Resource):

    def get(self):
        """Restitu==ce il pannello di controllo

        Usage example:
            `curl http://localhost:5000/panel`
        """
        return self.notify('panel', 'GET', self._response)


class User(Resource):

    def get(self):
        """Restitu==ce lo user con l'id specificato

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
        """Restitu==ce le preferenze dello user con l'id specificato

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

        self.api.add_resource(
            Access, '/access',
            resource_class_kwargs={'obs': self}
        )

        self.api.add_resource(
            Panel, '/panel',
            resource_class_kwargs={'obs': self}
        )

        self.api.add_resource(
            User, '/user',
            resource_class_kwargs={'obs': self}
        )

        self.api.add_resource(
            Preference, '/preference',
            resource_class_kwargs={'obs': self}
        )

    def access(self, request_type: str, msg: str):
        if request_type == 'GET':
            pass
        elif request_type == 'POST':
            pass

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
        if resource == 'access':
            return self.access(request_type, msg)
        elif resource == 'panel':
            return self.panel(request_type, msg)
        elif resource == 'user':
            return self.user(request_type, msg)
        elif resource == 'preference':
            return self.preference(request_type, msg)


def main():
    flask = Flask(__name__)
    Controller(
        flask_restful.Api(flask),
        MongoFacadeCreator().instantiate()
    )

    flask.run(debug=True)


if __name__ == "__main__":
    main()
