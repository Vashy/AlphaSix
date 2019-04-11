# Usage: python3 __file__.py

from os import urandom
from abc import ABC, abstractmethod
import pathlib
import json

from flask import Flask, request, session, make_response, redirect, url_for, render_template_string

import flask_restful

from mongo_db.facade import MongoFacade
from mongo_db.users import MongoUsers
from mongo_db.projects import MongoProjects
from mongo_db.singleton import MongoSingleton

html = (pathlib.Path(__file__).parent / 'static/html').resolve()


class Observer(ABC):

    @abstractmethod
    def update(self, resource: str, request_type: str, msg: str):
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


class SubjectResource(type(Subject), type(flask_restful.Resource)):
    pass


class Resource(Subject, flask_restful.Resource, metaclass=SubjectResource):

    def __init__(self):
        super(Resource, self).__init__()
        self._response = None

    def notify(self, request_type: str, resource: str, msg: str):
        for obs in self._lst:
            return obs.update(request_type, resource, msg)


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
            `curl http://localhost:5000/api/preference/1`
        """
        return self.notify('preference', 'GET', self._response)

    def post(self) -> dict:
        """Modifica le preferenze dello user indicato nel corpo della request

        Usage example:
        `curl http://localhost:5000/api/preference -X POST -d "data=some data"`
        """
        data = request.get_json(force=True)
        return self.notify('preference', 'POST', data)


class Controller(Observer):

    def __init__(
        self,
        server: Flask,
        api: flask_restful.Api,
        model: MongoFacade
    ):
        self.model = model
        self.server = server
        self.api = api

        self.user = User
        self.preference = Preference

        self.api.add_resource(
            self.user, '/api/user'
        )

        self.api.add_resource(
            self.preference, '/api/preference'
        )

        self.user.addObserver(self.user, obs=self)
        self.preference.addObserver(self.preference, obs=self)

        self.server.add_url_rule(
            '/',
            'panel',
            self.panel,
            methods=['GET', 'POST']
        )

        self.server.add_url_rule(
            '/web_user',
            'web_user',
            self.web_user,
            methods=['GET', 'POST', 'PUT', 'DELETE']
        )

        self.server.add_url_rule(
            '/web_preference',
            'web_preference',
            self.web_preference,
            methods=['GET', 'POST', 'PUT', 'DELETE']
        )

    def _users_id(self, userid: str):
        ids = []
        for user in self.model.users():
            ids.append(user[userid])
        return ids

    def _check_session(self):
        return 'userid' in session

    def _check_values(self, request: request):
        return len(request.values) != 0

    def access(self, request: request):
        fileHtml = html / 'access.html'
        page = fileHtml.read_text()
        userid = request.form.get('userid')
        if request.form.get('userid'):
            if self.model.user_exists(request.form['userid']):
                session['userid'] = request.form['userid']
                return redirect(url_for('panel'), code=303)
            else:
                page = page.replace(
                    '*access*',
                    '<p>Accesso non riuscito. ' + userid + ' non trovato.</p>')
                page = page.replace('*userid*', userid)
        page = page.replace('*access*', '')
        page = page.replace('*userid*', '')
        return page

    def panel(self):
        if self._check_session():
            fileHtml = html / 'panel.html'
            return render_template_string(fileHtml.read_text())
        else:
            return self.access(request)

    def remove_user(self):
        values = self._users_id('_id')
        display = []
        for user in values:
            telegram = self.model.get_user_telegram(user)
            email = self.model.get_user_email(user)
            if telegram is None:
                telegram = ''
            if email is None:
                email = ''
            display.append(
                telegram +
                ' ' +
                email
            )
        options = '<select>'
        for i,voice in enumerate(display):
            options += '<option value="' + str(values[i]) + '">' + display[i] + '</option>'
        options += '</select>'
        fileHtml = html / 'removeuser.html'
        page = fileHtml.read_text()
        return page.replace('*userids*', options)


    def web_user(self):
        if self._check_session():
            if(not self._check_values(request)):
                if request.method == 'PUT':
                    fileHtml = html / 'adduser.html'
                    page = fileHtml.read_text()
                elif request.method == 'POST':
                    fileHtml = html / 'modifyuser.html'
                    page = fileHtml.read_text()
                elif request.method == 'DELETE':
                    page = self.remove_user()
                return render_template_string(page)
        else:
            return self.access(request)

    def web_preference(self):
        if self._check_session():
            if(not self._check_values(request)):
                fileHtml = html / 'preference.html'
                page = fileHtml.read_text()
                return render_template_string(page)
        else:
            return self.access(request)

    def api_user(self, request_type: str, msg: str):
        if request_type == 'GET':
            pass
        elif request_type == 'POST':
            pass

    def api_preference(self, request_type: str, msg: str):
        if request_type == 'GET':
            pass
        elif request_type == 'POST':
            pass

    def update(self, resource: str, request_type: str, msg: str):
        if resource == 'user':
            return self.api_user(request_type, msg)
        elif resource == 'preference':
            return self.api_preference(request_type, msg)


def main():
    flask = Flask(__name__)
    flask.secret_key = urandom(16)
    api = flask_restful.Api(flask)
    mongo = MongoSingleton.instance()
    users = MongoUsers(mongo)
    projects = MongoProjects(mongo)
    facade = MongoFacade(users, projects)
    Controller(
        flask,
        api,
        facade
    )

    flask.run(debug=True)


if __name__ == "__main__":
    main()
