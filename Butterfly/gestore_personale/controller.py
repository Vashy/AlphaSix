# Usage: python3 __file__.py

from os import urandom
from abc import ABC, abstractmethod
import pathlib
import json
import datetime
import calendar

from flask import Flask, request, session, make_response, redirect, url_for, render_template_string
import flask_restful

from mongo_db.facade import MongoFacade
from mongo_db.users import MongoUsers
from mongo_db.projects import MongoProjects
from mongo_db.singleton import MongoSingleton

html = (pathlib.Path(__file__).parent / 'static' / 'html').resolve()


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
        return 'email' in session or 'telegram' in session

    def _check_values(self):
        return len(request.values) != 0

    def access(self):
        fileHtml = html / 'access.html'
        page = fileHtml.read_text()
        userid = request.values.get('userid')
        if userid:
            if self._model.user_exists(userid):
                session['email'] = self._model.get_user_email(userid)
                session['telegram'] = self._model.get_user_telegram(userid)
                session['userid'] = session['email'] if 'email' in session else session['telegram']
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
            if ((
                email and
                self._model.user_exists(email) and
                email != session['email']
            )or(
                telegram and
                self._model.user_exists(telegram) and
                telegram != session['telegram']
                )
            ):
                page = page.replace(
                    '*modifyuser*',
                    '<p>I dati inseriti confliggono\
con altri già esistenti.</p>'
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
                if('email' in modify and
                    ('email' not in session) or
                    (modify['email'] != session['email'])
                ):
                    self._model.update_user_email(
                        session['userid'],
                        modify['email']
                    )
                    session['email'] = modify['email']
                if('telegram' in modify and
                    ('telegram' not in session) or
                    (modify['telegram'] != session['telegram'])
                ):
                    self._model.update_user_telegram(
                        session['userid'],
                        modify['telegram']
                    )
                    session['telegram'] = modify['telegram']
        if request.values.get('modifyuser'):
            page = page.replace(
                    '*modifyuser*',
                    '<p>Si prega di inserire almeno email o telegram\
per modificare l\'utente.</p>')
        user = self._model.read_user(session['userid'])
        page = page.replace('*nome*', user['name'])
        page = page.replace('*cognome*', user['surname'])
        page = page.replace('*email*', user['email'])
        page = page.replace('*telegram*', user['telegram'])
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

    def load_preference_topic(self):
        user_projects = self._model.get_user_projects(session['userid'])
        form = '<form id="topics">\
        <table border="1"><tr><th>Url</th><th>Priorità</th>\
<th>Labels</th><th>Keywords</th></tr>'
        for user_project in user_projects:
            project_data = self._model.read_project(
                user_project['url']
            )
            project_data['url'] = project_data['url'].lstrip().rstrip()
            row = '<tr>'
            row += '<th>' + project_data['url'] + '</th>'
            row += '<td><select id="priority" name="\
' + project_data['url'] + '-priority">'
            for priority in range(1, 4):
                row += '<option'
                if priority == user_project['priority']:
                    row += ' selected="selected"'
                row += ' value="' + str(priority) + '">\
' + str(priority) + '</option>'
            row += '</select></td><td>'
            for topic in project_data['topics']:
                row += '<label>' + topic + '</label>'
                row += '<input type="checkbox" name="\
' + project_data['url'] + '-topics"'
                if topic in user_project['topics']:
                    row += ' checked="checked"'
                row += ' value="' + topic + '">'
            row += '</td><td><textarea id="textkeywords" name="\
' + project_data['url'] + '-keywords">'
            for keyword in user_project['keywords']:
                row += keyword
                row += ','
            row = row[:-1]  # elimino l'ultima virgola
            row += '</textarea></td></tr>'
            form += row
        form += '</table><input id="modifytopics"\
name="modifytopics" type="button" \
value="Modifica preferenze di progetti e topic"></form>'
        return form

    def load_preference_project(self):
        projects = self._model.projects()
        form = '<form id="projects"><select name="projects">'
        for project in projects:
            form += '<option value="' + project['url'] + '">\
' + project['name'] + '</option>'
        form += '</select> <input id="addproject"\
name="addproject" type="button" \
value="Aggiungi il progetto">\
<input id="removeproject"\
name="removeproject" type="button" \
value="Rimuovi il progetto"></form>'
        return form

    def load_preference_availability(
        self,
        year=datetime.datetime.now().year,
        month=datetime.datetime.now().month
    ):
        date = datetime.datetime(year, month, 1)
        irreperibilita = self._model.read_user(
            session['userid']
        ).get('irreperibilita')
        form = '<form id="availability">\
        <fieldset><legend>Giorni di indisponibilità</legend>\
<div id="calendario"></div><p>' + date.strftime("%B") + ' \
' + date.strftime('%Y') + '</p>'
        month_with_0 = str(month)
        if len(month_with_0) < 2:
                month_with_0 = '0' + month_with_0
        for day in range(1, calendar.monthrange(year, month)[1]+1):
            day = str(day)
            if len(day) < 2:
                day = '0' + day
            date = str(year) + '-' + month_with_0 + '-' + day
            form += '<label for="' + date + '\
            ">' + day + '</label><input type="checkbox"\
name="indisponibilita[]" value="' + date + '"'
            if date in irreperibilita:
                form += ' checked="checked"'
            form += '>'
        form += '<input type="button" value="Mese precedente"/>\
<input type="button" value="Mese successivo"/>\
<input id="irreperibilita" name="irreperibilita" type="button"\
value="Modifica irreperibilità"/></fieldset></form>'
        return form

    def load_preference_platform(self):
        platform = self._model.read_user(session['userid'])['preference']
        form = '<form id="platform"><fieldset>\
<legend>Piattaforma preferita</legend>\
<label for="email">Email</label>\
<input name="platform" id="email"\
type="radio"'
        if(platform == 'email'):
            form += ' checked = "checked"'
        form += '/><label for="telegram">Telegram</label>\
<input name="platform" id="telegram" type="radio"'
        if(platform == 'telegram'):
            form += ' checked = "checked"'
        form += '/><input id="piattaforma" name="piattaforma" type="button"\
value="Modifica piattaforma preferita"/></fieldset></form>'
        return form

    def modifytopics(self):
        user_projects = self._model.get_user_projects(session['userid'])
        for key, value in request.values.items():
            for project in user_projects:
                if project['url'] in key:
                    if 'priority' in key:
                        # TODO : set_priority(user,project)
                    elif 'topics' in key:
                        # TODO : get_topics(user,project)
                        # TODO : remove_topics(user,project,topics-value)
                        # TODO : add_topics(user,project,value-topics)
                    elif 'keywords' in key:
                        # TODO : get_keywords(user,project)
                        # TODO : remove_keywords(user,project,keywords-value)
                        # TODO : add_topics(user,project,value-topics)
        return self.load_preference_topic()

    def addproject(self):
        project = request.values['project']
        # TODO : add_project(user,project)
        return self.load_preference_project()

    def removeproject(self):
        project = request.values['project']
        # TODO : remove_project(user,project)
        return self.load_preference_project()

    def indisponibilita(self):
        giorni = request.values['indisponibilita']
        # TODO : get_indisponibilita(user)
        # TODO : remove_indisponibilita(user,user_indis-indis)
        # TODO : add_indisponibilita(user,indis-user_indis)
        return self.load_preference_availability()

    def piattaforma(self):
        platform = request.values['platform']
        # TODO : setplatform(user, platform)
        return self.load_preference_platform()

    def modify_preference(self):
        fileHtml = html / 'preference.html'
        page = fileHtml.read_text()
        if request.values.get('preference'):
            page = page.replace('*topics*', self.load_preference_topic())
            page = page.replace('*projects*', self.load_preference_project())
            page = page.replace(
                '*availability*',
                self.load_preference_availability()
            )
            page = page.replace('*platform*', self.load_preference_platform())
        elif request.values.get('modifytopics'):
            return self.modifytopics()
        elif request.values.get('addproject'):
            return self.addproject()
        elif request.values.get('removeproject'):
            return self.removeproject()
        elif request.values.get('indisponibilita'):
            return self.indisponibilita()
        elif request.values.get('piattaforma'):
            return self.piattaforma()
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
