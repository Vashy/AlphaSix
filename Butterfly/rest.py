# Usage: python3 __file__.py

from abc import ABC, abstractmethod

from flask import Flask, request
import flask_restful
from flask_restful import Api

from mongo_db.facade import Observer

users = {}


class Subject(ABC):

    def __init__(self):
        self.lst = []

    @abstractmethod
    def notify(self, request_type: str, msg: dict):
        pass

    def add_observer(self, obs: Observer):
        if obs not in self.lst:
            self.lst.append(obs)


class User(flask_restful.Resource):

    def get(self, user_id):
        """Restituisce lo User con l'id specificato

        Usage example:
            `curl http://localhost:5000/user/<user_id>`
        """
        return {user_id: users[user_id]}

    def delete(self, user_id):
        """Rimuove un User

        Usage example:
            `curl http://localhost:5000/user/<user_id> -X DELETE`
        """
        if user_id in users:
            return users.pop(user_id)


class Resource(flask_restful.Resource, Subject):

    def notify(self, request_type, msg):
        for observer in self.lst:
            observer.update(request_type, msg)


class Users(Resource):

    @classmethod
    def make_api(cls, response):
        cls.response = response
        return cls

    def get(self):
        """Restituisce la collezione di Users.

        Usage example:
            `curl http://localhost:5000/users`
        """
        response = self.notify('GET', self.response)
        return response

    def post(self) -> dict:
        """Crea un User.

        Usage example:
            `curl http://localhost:5000/users -X POST -d "data=some data"`
        """
        # user_id = len(users)
        # users[user_id] = request.form['data']
        # return {user_id: users[user_id]}
        # print('AAAAAAAAAAAAAAAAAA')
        # return 200
        data = request.form['data']
        self.notify('POST', self.response['data'])
        self.response[len(self.response)] = data
        return 'Ok', 200


class Controller(Observer):

    def __init__(self, api: Api):
        self.api = api
        # self.api.add_resource(User, '/user/<int:user_id>')

        us = Users.make_api(users)
        # us = Users()
        # us.add_observer(model)
        # us.add_observer(model)
        self.api.add_resource(us, '/users')

        # self.api.make_response

    def update(self, msg, a):
        pass

#    def notify(self, request_type, msg):
#        for obs in self.observers:
#            print('AAAAAAAAAAAAAAAaa')
#            obs.update(request_type, msg)


def main():
    # import pdb; pdb.set_trace()
    flask = Flask(__name__)
    from unittest.mock import Mock
    controller = Controller(Api(flask))
    flask.run(debug=True)


if __name__ == "__main__":
    main()
