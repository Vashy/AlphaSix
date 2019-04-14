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
        self._model = model
        self._server = server
        self._api = api

        self._user = User
        self._preference = Preference

        self._api.add_resource(
            self._user, '/api/user'
        )

        self._api.add_resource(
            self._preference, '/api/preference'
        )

        self._user.addObserver(self._user, obs=self)
        self._preference.addObserver(self._preference, obs=self)

        self._server.add_url_rule(
            '/',
            'panel',
            self.panel,
            methods=['GET', 'POST']
        )

        self._server.add_url_rule(
            '/web_user',
            'web_user',
            self.web_user,
            methods=['GET', 'POST', 'PUT', 'DELETE']
        )

        self._server.add_url_rule(
            '/web_preference',
            'web_preference',
            self.web_preference,
            methods=['POST']
        )

    def _users_id(self):
        ids = []
        for user in self._model.users():
            ids.append(user['_id'])
        return ids

    def _check_session(self):
        return 'userid' in session

    def _check_values(self):
        return len(request.values) != 0

    def access(self):
        fileHtml = html / 'access.html'
        page = fileHtml.read_text()
        userid = request.values.get('userid')
        if userid:
            if self._model.user_exists(userid):
                session['userid'] = userid
                return redirect(url_for('panel'), code=303)
            else:
                page = page.replace(
                    '*access*',
                    '<p>Accesso non riuscito. ' + userid + ' non trovato.</p>')
                page = page.replace('*userid*', userid)
        if request.values.get('access'):
            page = page.replace(
                    '*access*',
                    '<p>Si prega di inserire un identificativo\
                    per eseguire l\'accesso.</p>')
        page = page.replace('*access*', '')
        page = page.replace('*userid*', '')
        return page

    def panel(self):
        if self._check_session():
            fileHtml = html / 'panel.html'
            return render_template_string(fileHtml.read_text())
        else:
            return self.access()

    def add_user(self):
        fileHtml = html / 'adduser.html'
        page = fileHtml.read_text()
        nome = request.values.get('nome')
        cognome = request.values.get('cognome')
        email = request.values.get('email')
        telegram = request.values.get('telegram')
        if email or telegram:
            if nome:
                page = page.replace('*nome*', nome)
            if cognome:
                page = page.replace('*cognome*', cognome)
            if email:
                page = page.replace('*email*', email)
            if telegram:
                page = page.replace('*telegram*', telegram)
            if (
                (email and self._model.user_exists(email)) or
                (telegram and self._model.user_exists(telegram))
            ):
                page = page.replace(
                    '*adduser*',
                    '<p>L\'utente inserito esiste già.</p>'
                )
            else:
                page = page.replace(
                    '*adduser*',
                    '<p>Utente inserito correttamente.</p>'
                )
                self._model.insert_user(
                    name=nome,
                    surname=cognome,
                    email=email,
                    telegram=telegram
                )
        if request.values.get('adduser'):
            page = page.replace(
                    '*adduser*',
                    '<p>Si prega di inserire almeno email o telegram\
                    per inserire l\'utente.</p>')
        page = page.replace('*nome*', '')
        page = page.replace('*cognome*', '')
        page = page.replace('*email*', '')
        page = page.replace('*telegram*', '')
        page = page.replace('*adduser*', '')
        return page

    def modify_user(self):
        fileHtml = html / 'modifyuser.html'
        page = fileHtml.read_text()
        nome = request.values.get('nome')
        cognome = request.values.get('cognome')
        email = request.values.get('email')
        telegram = request.values.get('telegram')
        modify = {}
        if email or telegram:
            if nome:
                page = page.replace('*nome*', nome)
                modify.update(nome=nome)
            if cognome:
                page = page.replace('*cognome*', cognome)
                modify.update(cognome=cognome)
            if email:
                page = page.replace('*email*', email)
                modify.update(email=email)
            if telegram:
                page = page.replace('*telegram*', telegram)
                modify.update(telegram=telegram)
            if (
                email and self._model.user_exists(email) or
                telegram and self._model.user_exists(telegram)
            ):
                page = page.replace(
                    '*modifyuser*',
                    '<p>I dati inseriti confliggono con altri già\
                     esistenti.</p>'
                )
            else:
                page = page.replace(
                    '*modifyuser*',
                    '<p>Utente modificato correttamente.</p>'
                )
                if('nome' in modify):
                    self._model.update_user_name(
                        session['userid'],
                        modify['nome']
                    )
                if('cognome' in modify):
                    self._model.update_user_surname(
                        session['userid'],
                        modify['cognome']
                    )
                if('email' in modify):
                    self._model.update_user_email(
                        session['userid'],
                        modify['email']
                    )
                if('telegram' in modify):
                    self._model.update_user_telegram(
                        session['userid'],
                        modify['telegram']
                    )
        if request.values.get('modifyuser'):
            page = page.replace(
                    '*modifyuser*',
                    '<p>Si prega di inserire almeno email o telegram\
                    per modificare l\'utente.</p>')
        page = page.replace('*nome*', '')
        page = page.replace('*cognome*', '')
        page = page.replace('*email*', '')
        page = page.replace('*telegram*', '')
        page = page.replace('*modifyuser*', '')
        return page

    def remove_user(self):
        fileHtml = html / 'removeuser.html'
        page = fileHtml.read_text()
        userid = request.values.get('userid')
        if userid:
            page = page.replace(
                '*removeuser*',
                '<p>Utente rimosso correttamente.</p>'
            )
            print(self._model.delete_user(userid).deleted_count)
        page = page.replace('*removeuser*', '')

        values = self._users_id()
        display = []
        for user in values:
            telegram = self._model.get_user_telegram(user)
            email = self._model.get_user_email(user)
            if telegram is None:
                telegram = ''
            if email is None:
                email = ''
            display.append(
                telegram +
                ' ' +
                email
            )
        options = '<select id="userid" name="userid">'
        for i, voice in enumerate(display):
            options += '<option value="' + str(values[i]) + '">'
            options += display[i]
            options += '</option>'
        options += '</select>'
        return page.replace('*userids*', options)

    def web_user(self):
        if self._check_session():
            if request.method == 'POST':
                page = self.add_user()
            elif request.method == 'PUT':
                page = self.modify_user()
            elif request.method == 'DELETE':
                page = self.remove_user()
            return render_template_string(page)
        else:
            return self.access()

    def modify_preference(self):
        fileHtml = html / 'preference.html'
        page = fileHtml.read_text()
        return page

    def web_preference(self):
        if self._check_session():
            page = self.modify_preference()
            return render_template_string(page)
        else:
            return self.access()

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
            return self._api_user(request_type, msg)
        elif resource == 'preference':
            return self._api_preference(request_type, msg)


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
