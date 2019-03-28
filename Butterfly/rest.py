# Usage: python3 __file__.py

from abc import ABC, abstractmethod

from flask import Flask, request
from flask_restful import Resource, Api

users = {}


class Observer(ABC):
    @abstractmethod
    def update():
        pass


class Subject(ABC):

    def __init__():
        self.lst = []

    @abstractmethod
    def notify(self, msg: dict):
        pass

    def add_observer(self, obs: Observer):
        if obs not in self.lst:
            self.lst.append(obs)

    # def remove_observer()


class User(Resource):
    
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
        return self.response

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
        self.response[len(self.response)] = data
        return 'Ok', 200


class Controller(Subject):
    def __init__(self, api: Api, model):
        self.api = api
        self.api.add_resource(User, '/user/<int:user_id>')
        # self.observers = observers
        self.add_observer(model)

        us = Users.make_api(users)
        self.api.add_resource(us, '/users')
    
    def notify(self, msg):
        for obs in self.observers:
            obs.update(msg)




if __name__ == "__main__":
    flask = Flask(__name__)
    controller = Controller(Api(flask))
    flask.run(debug=True)
