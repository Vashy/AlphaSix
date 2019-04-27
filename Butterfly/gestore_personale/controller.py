# Usage: python3 __file__.py

from os import urandom
from abc import ABC, abstractmethod
import pathlib
import json
import datetime
import calendar

from flask import Flask, request, session, make_response, redirect, url_for, render_template_string
import flask_restful
from bson.json_util import dumps

from mongo_db.facade import MongoFacade
from mongo_db.users import MongoUsers
from mongo_db.projects import MongoProjects
from mongo_db.singleton import MongoSingleton

html = (pathlib.Path(__file__).parent / 'static' / 'html').resolve()


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


class SubjectResource(type(Subject), type(flask_restful.Resource)):
    pass


class Resource(Subject, flask_restful.Resource, metaclass=SubjectResource):

    def __init__(self):
        super(Resource, self).__init__()

    def notify(self, request_type: str, resource: str, url: str, msg: str):
        for obs in self._lst:
            return obs.update(request_type, resource, url, msg)


class User(Resource):

    def get(self, url: str):
        return self.notify('user', 'GET', url, None)

    def put(self, url: str) -> dict:
        data = request.get_json(force=True)
        return self.notify('user', 'PUT', url, data)

    def delete(self, url: str) -> dict:
        data = request.get_json(force=True)
        return self.notify('user', 'DELETE', url, data)


class PostUser(Resource):

    def post(self) -> dict:
        """
        Usage example:
            `curl http://localhost:5000/users -X POST -d "data=some data"`
        """
        data = request.get_json(force=True)
        return self.notify('user', 'POST', None, data)


class Preference(Resource):

    def get(self, url: str):
        return self.notify('preference', 'GET', None)

    def put(self) -> dict:
        data = request.get_json(force=True)
        return self.notify('preference', 'PUT', data)

    def delete(self) -> dict:
        data = request.get_json(force=True)
        return self.notify('preference', 'DELETE', data)


class PostPreference(Resource):

    def post(self) -> dict:
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
        self._post_user = PostUser
        self._preference = Preference
        self._post_preference = PostPreference

        self._api.add_resource(
            self._user, '/api/v1/user/<url>'
        )

        self._api.add_resource(
            self._post_user, '/api/v1/user'
        )

        self._api.add_resource(
            self._preference, '/api/v1/preference/<url>'
        )

        self._api.add_resource(
            self._post_preference, '/api/v1/preference'
        )

        self._user.addObserver(self._user, obs=self)
        self._post_user.addObserver(self._post_user, obs=self)
        self._preference.addObserver(self._preference, obs=self)
        self._post_preference.addObserver(self._post_preference, obs=self)

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
                session['email'] = self._model.get_user_email_web(userid)
                session['telegram'] = self._model.get_user_telegram_web(userid)
                if 'email' in session:
                    session['userid'] = session['email']
                else:
                    session['userid'] = session['telegram']
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

    def logout(self):
        session.clear()

    def panel(self, error=''):
        if self._check_session():
            fileHtml = html / 'panel.html'
            page = fileHtml.read_text()
            page = page.replace('*panel*', error)
            try:
                return render_template_string(page)
            except TypeError:
                return page
        else:
            try:
                return render_template_string(self.access())
            except TypeError:
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
                    '<p>Si prega di inserire almeno email o telegram \
per inserire l\'utente.</p>')
        page = page.replace('*nome*', '')
        page = page.replace('*cognome*', '')
        page = page.replace('*email*', '')
        page = page.replace('*telegram*', '')
        page = page.replace('*adduser*', '')
        return page

    def modify_user(self):
        try:
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
                        '<p>Si prega di inserire almeno email o telegram \
    per modificare l\'utente.</p>')
            user = self._model.read_user(session['userid'])
            page = page.replace('*nome*', user['name'] if user['name'] else '')
            page = page.replace('*cognome*', user['surname'] if user['surname'] else '')
            page = page.replace('*email*', user['email'] if user['email'] else '')
            page = page.replace('*telegram*', user['telegram'] if user['telegram'] else '')
            page = page.replace('*modifyuser*', '')
            return page
        except AssertionError:
            return self.panel(error='Non sei più iscritto alla piattaforma.')

    def remove_user(self):
        fileHtml = html / 'removeuser.html'
        page = fileHtml.read_text()
        userid = request.values.get('userid')
        if userid:
            page = page.replace(
                '*removeuser*',
                '<p>Utente rimosso correttamente.</p>'
            )
            email = self._model.get_user_email_from_id(userid)
            telegram = self._model.get_user_telegram_from_id(userid)
            user = email if email else telegram
            self._model.delete_user_from_id(userid)
            if user == session['email'] or user == session['telegram']:
                self.logout()
                return redirect(url_for('panel'), code=303)
        page = page.replace('*removeuser*', '')

        values = self._users_id()
        display = []
        for user in values:
            telegram = self._model.get_user_telegram_from_id(user)
            email = self._model.get_user_email_from_id(user)
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
            if request.method == 'GET':
                page = self.panel()
            elif request.method == 'POST':
                if 'logout' in request.values:
                    self.logout()
                    page = self.panel()
                else:
                    page = self.add_user()
            elif request.method == 'PUT':
                page = self.modify_user()
            elif request.method == 'DELETE':
                page = self.remove_user()
            try:
                return render_template_string(page)
            except TypeError:
                return page
        else:
            return self.access()

    def load_preference_topic(self):
        user_projects = self._model.get_user_projects(session['userid'])
        form = '<form id="topics">\
        <table id="topics-table"><tr><th>Url</th><th>Priorità</th>\
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
                row += '<br/><label>' + topic + '</label>'
                row += '<input type="checkbox" name="\
' + project_data['url'] + '-topics"'
                if topic in user_project['topics']:
                    row += ' checked="checked"'
                row += ' value="' + topic + '">'
            row += '</td><td><textarea id="textkeywords" name="\
' + project_data['url'] + '-keywords">'
            if user_project['keywords']:
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
        form = '<form id="projects"><select name="project">'
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
        for day in range(1, calendar.monthrange(year, month)[1]+1):
            date = datetime.datetime(year, month, day)
            form += '<label for="' + str(date) + '\
">' + str(day) + '</label><input type="checkbox"\
name="indisponibilita[]" value="' + str(date) + '"'
            if date in irreperibilita:
                form += ' checked="checked"'
            form += '>'
        form += '<br/><input type="button" id="previousmonth"\
value="Mese precedente"/>\
<input type="button" id="nextmonth" value="Mese successivo"/>\
<input type="hidden" name="mese" value="' + date.strftime("%m") + '">\
<input type="hidden" name="anno" value="' + date.strftime("%Y") + '">\
<br/><input id="irreperibilita" name="irreperibilita" type="button"\
value="Modifica irreperibilità"/></fieldset></form>'
        return form

    def load_preference_platform(self, error=''):
        platform = self._model.read_user(session['userid'])['preference']
        form = '<form id="platform"><fieldset>\
<legend>Piattaforma preferita</legend>\
<label for="email">Email</label>\
<input name="platform" id="email"\
type="radio" value="email"'
        if(platform == 'email'):
            form += ' checked = "checked"'
        form += '/><br/><label for="telegram">Telegram</label>\
<input name="platform" id="telegram" type="radio" value="telegram"'
        if(platform == 'telegram'):
            form += ' checked = "checked"'
        form += '/><br/><input id="piattaforma" name="piattaforma"\
type="button" value="Modifica piattaforma preferita"/></fieldset></form>'
        form += error
        return form

    def modifytopics(self):
        firstTopic = True
        old = None
        for key, value in request.values.items(multi=True):
            url = key.replace('-priority', '')
            url = url.replace('-topics', '')
            url = url.replace('-keywords', '')
            if not old:
                old = url
            elif url != old:
                firstTopic = True
                old = url
            if url != 'modifytopics':
                if 'priority' in key:
                    self._model.set_user_priority(
                        session['userid'], url, value
                    )
                elif 'topics' in key:
                    if firstTopic:
                        self._model.reset_user_topics(
                            session['userid'],
                            url
                        )
                    self._model.add_user_topics(
                        session['userid'],
                        url,
                        value
                    )
                    firstTopic = False
                elif 'keywords' in key:
                    value = value.strip()
                    keywords = value.split(',')
                    self._model.reset_user_keywords(
                        session['userid'],
                        url
                    )
                    self._model.add_user_keywords(
                        session['userid'],
                        url,
                        *keywords
                    )
        return self.load_preference_topic()

    def addproject(self):
        project = request.values['project']
        self._model.add_user_project(session['userid'], project)
        return self.load_preference_topic()

    def removeproject(self):
        project = request.values['project']
        self._model.remove_user_project(session['userid'], project)
        return self.load_preference_topic()

    def indisponibilita(self):
        giorni = request.values.getlist('indisponibilita[]')
        giorni_old = self._model.read_user(
            session['userid']
        ).get('irreperibilita')
        giorni_new = []
        for giorno in giorni:
            giorni_new.append(
                datetime.datetime.strptime(giorno, '%Y-%m-%d %H:%M:%S')
            )
        if giorni_new:
            year = giorni_new[0].strftime('%Y')
            month = giorni_new[0].strftime('%m')
            for giorno in giorni_old:
                if (
                    giorno.strftime('%Y') == year and
                    giorno.strftime('%m') == month
                ):
                    if giorno not in giorni_new:
                        self._model.remove_giorno_irreperibilita(
                            session['userid'],
                            int(year),
                            int(month),
                            int(giorno.strftime('%d'))
                        )
            for giorno in giorni_new:
                self._model.add_giorno_irreperibilita(
                    session['userid'],
                    int(year),
                    int(month),
                    int(giorno.strftime('%d'))
                )
        return self.load_preference_availability()

    def previous_indisponibilita(self):
        mese = int(request.values['mese'])
        anno = int(request.values['anno'])
        if (mese == 1):
            anno = anno - 1
            mese = 12
        else:
            mese = mese - 1
        self.indisponibilita()
        return self.load_preference_availability(anno, mese)

    def next_indisponibilita(self):
        mese = int(request.values['mese'])
        anno = int(request.values['anno'])
        if (mese == 12):
            anno = anno + 1
            mese = 1
        else:
            mese = mese + 1
        self.indisponibilita()
        return self.load_preference_availability(anno, mese)

    def piattaforma(self):
        platform = request.values['platform']
        if platform == "telegram":
            telegram = self._model.get_user_telegram_web(session['userid'])
            if not telegram:
                return self.load_preference_platform(error='<p>Non hai\
 memorizzato la piattaforma telegram nel sistema.</p>')
        if platform == "email":
            email = self._model.get_user_email_web(session['userid'])
            if not email:
                return self.load_preference_platform(error='<p>Non hai\
 memorizzato la piattaforma email nel sistema.</p>')
        self._model.update_user_preference(session['userid'], platform)
        return self.load_preference_platform()

    def modify_preference(self):
        fileHtml = html / 'preference.html'
        page = fileHtml.read_text()
        if request.values.get('preference'):
            try:
                page = page.replace('*topics*', self.load_preference_topic())
                page = page.replace(
                    '*projects*',
                    self.load_preference_project()
                )
                page = page.replace(
                    '*availability*',
                    self.load_preference_availability()
                )
                page = page.replace(
                    '*platform*',
                    self.load_preference_platform()
                )
            except AssertionError:
                return self.panel(error='Non sei più iscritto alla\
 piattaforma.')
        elif request.values.get('modifytopics'):
            return self.modifytopics()
        elif request.values.get('addproject'):
            return self.addproject()
        elif request.values.get('removeproject'):
            return self.removeproject()
        elif request.values.get('irreperibilita'):
            return self.indisponibilita()
        elif request.values.get('previousmonth'):
            return self.previous_indisponibilita()
        elif request.values.get('nextmonth'):
            return self.next_indisponibilita()
        elif request.values.get('piattaforma'):
            return self.piattaforma()
        return page

    def web_preference(self):
        if self._check_session():
            page = self.modify_preference()
            try:
                return render_template_string(page)
            except TypeError:
                return page
        else:
            return self.access()

    def _api_user(self, request_type: str, url: str, msg: str):
        if request_type == 'GET':
            user = self._model.read_user(url)
            userjson = json.loads(dumps(user))
            for i, data in enumerate(userjson['irreperibilita']):
                userjson['irreperibilita'][i]['$date'] = datetime.datetime.strftime(
                    datetime.datetime.fromtimestamp(
                        userjson['irreperibilita'][i]['$date']/1000
                    ),
                    format="%Y-%m-%d"
                )
            return userjson
        elif request_type == 'PUT':
            nome = msg.get('nome')
            cognome = msg.get('cognome')
            email = msg.get('email')
            telegram = msg.get('telegram')
            modify = {}
            if url:
                if(nome):
                    self._model.update_user_name(
                        url,
                        nome
                    )
                if(cognome):
                    self._model.update_user_surname(
                        url,
                        cognome
                    )
                if email and email != url:
                    self._model.update_user_email(
                        url,
                        email
                    )
                if telegram and telegram != url:
                    self._model.update_user_telegram(
                        url,
                        telegram
                    )
                return {'ok': 'Utente modificato correttamente'}, 200
            else:
                return {'error': 'Si prega di inserire almeno email o telegram \
per modificare l\'utente.'}, 409
        elif request_type == 'DELETE':
            if url:
                email = self._model.get_user_email(url)
                telegram = self._model.get_user_telegram(url)
                self._model.delete_user(url)
                return {'ok': 'Utente rimosso correttamente'}, 200
            return {'error': 'Si prega di inserire almeno email o telegram \
per rimuovere l\'utente.'}, 409
        elif request_type == 'POST':
            nome = msg.get('nome')
            cognome = msg.get('cognome')
            email = msg.get('email')
            telegram = msg.get('telegram')
            if email or telegram:
                if (
                    (email and self._model.user_exists(email)) or
                    (telegram and self._model.user_exists(telegram))
                ):
                    return {'error': 'L\'utente inserito esiste già.'}, 409
                else:
                    self._model.insert_user(
                        name=nome,
                        surname=cognome,
                        email=email,
                        telegram=telegram
                    )
                    return {'ok': 'Utente inserito correttamente'}, 200
            else:
                return {'error': 'Si prega di inserire almeno email o telegram \
per inserire l\'utente.'}, 409

    def _api_preference(self, request_type: str, url: str, msg: str):
        if request_type == 'GET':
            pass
        elif request_type == 'PUT':
            pass
        elif request_type == 'DELETE':
            pass
        elif request_type == 'POST':
            pass

    def update(self, resource: str, request_type: str, url: str, msg: str):
        if resource == 'user':
            return self._api_user(request_type, url, msg)
        elif resource == 'preference':
            return self._api_preference(request_type, url, msg)


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
