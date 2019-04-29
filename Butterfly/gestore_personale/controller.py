# Usage: python3 __file__.py

from os import urandom

from flask import Flask
import flask_restful

from mongo_db.facade import MongoFacade
from mongo_db.users import MongoUsers
from mongo_db.projects import MongoProjects
from mongo_db.singleton import MongoSingleton
from gestore_personale.observer import Observer
from gestore_personale.api import User, PostUser, Preference, ApiHandler
from gestore_personale.web import Web


class Controller(Observer):

    def __init__(
        self,
        server: Flask,
        api: flask_restful.Api,
        handler: ApiHandler,
        web: Web,
        model: MongoFacade
    ):
        self._server = server
        self._api = api
        self._handler = handler
        self._web = web
        self._user = User
        self._post_user = PostUser
        self._preference = Preference

        self._api.add_resource(
            self._user,
            '/api/v1/user/<url>',
            resource_class_kwargs={'model': model}
        )

        self._api.add_resource(
            self._post_user,
            '/api/v1/user',
            resource_class_kwargs={'model': model}
        )

        self._api.add_resource(
            self._preference,
            '/api/v1/preference/<url>',
            resource_class_kwargs={'model': model}
        )

        self._user.addObserver(self._user, obs=self)
        self._post_user.addObserver(self._post_user, obs=self)
        self._preference.addObserver(self._preference, obs=self)

        self._server.add_url_rule(
            '/',
            'panel',
            self._web.panel,
            methods=['GET', 'POST']
        )

        self._server.add_url_rule(
            '/web_user',
            'web_user',
            self._web.web_user,
            methods=['GET', 'POST', 'PUT', 'DELETE']
        )

        self._server.add_url_rule(
            '/web_preference',
            'web_preference',
            self._web.web_preference,
            methods=['PUT']
        )

    def update(self, resource: str, request_type: str, url: str, msg: str):
        if resource == 'user':
            return self._handler.api_user(request_type, url, msg)
        elif resource == 'preference':
            return self._handler.api_preference(request_type, url, msg)


def main():
    flask = Flask(__name__)
    flask.secret_key = urandom(16)
    api = flask_restful.Api(flask)
    mongo = MongoSingleton.instance()
    users = MongoUsers(mongo)
    projects = MongoProjects(mongo)
    facade = MongoFacade(users, projects)
    web = Web(facade)
    handler = ApiHandler(facade)
    Controller(
        flask,
        api,
        handler,
        web,
        facade
    )

    flask.run(debug=True)


if __name__ == "__main__":
    main()
