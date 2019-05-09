"""
File: web.py
Data creazione: 2019-03-15

<descrizione>

Licenza: Apache 2.0

Copyright 2019 AlphaSix

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Versione: 0.1.0
Creatore: Matteo Marchiori, matteo.marchiori@gmail.com
Autori:
"""

import pathlib
import datetime
import calendar

from flask import request, session, redirect
from flask import url_for, render_template_string

from mongo_db.facade import MongoFacade


html = (pathlib.Path(__file__).parent / 'static' / 'html').resolve()


class Web:

    def __init__(
        self,
        model: MongoFacade
    ):
        self._model = model

    def _users_id(self):
        ids = []
        for user in self._model.users():
            ids.append(user['_id'])
        return ids

    def _projects_id(self):
        ids = []
        for project in self._model.projects():
            ids.append(project['url'])
        return ids

    def _check_session(self):
        return 'email' in session or 'telegram' in session

    def _check_admin(self):
        return 'admin' in session

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
                if 'email' in session and session['email']:
                    session['userid'] = session['email']
                else:
                    session['userid'] = session['telegram']
                user = self._model.read_user(userid)
                if 'admin' in user and user['admin'] == 1:
                    session['admin'] = 1
                return redirect(url_for('panel'), code=303)
            else:
                page = page.replace(
                    '*access*',
                    '<p>Accesso non riuscito. ' + userid + ' non trovato.</p>')
                page = page.replace('*userid*', userid)
        if request.values.get('access'):
            page = page.replace(
                    '*access*',
                    '<p>Si prega di inserire un identificativo \
per eseguire l\'accesso.</p>')
        page = page.replace('*access*', '')
        page = page.replace('*userid*', '')
        return page

    def logout(self):
        session.clear()

    def panel(self, error=''):
        if self._check_session():
            if self._check_admin():
                fileHtml = html / 'adminpanel.html'
            else:
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
                if email:
                    self._model.update_user_preference(email, 'email')
                elif telegram:
                    self._model.update_user_preference(telegram, 'telegram')
        if 'postuser' in request.values:
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
                email != session.get('email')
            )or(
                telegram and
                self._model.user_exists(telegram) and
                telegram != session.get('telegram')
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
                if(
                    'email' in modify and (
                    ('email' not in session) or
                    (modify['email'] != session['email'])
                )):
                    self._model.update_user_email(
                        session['userid'],
                        modify.get('email')
                    )
                    session['email'] = modify['email']
                    session['userid'] = modify['email']
                if('telegram' in modify and (
                    ('telegram' not in session) or
                    (modify['telegram'] != session['telegram'])
                )):
                    self._model.update_user_telegram(
                        session['userid'],
                        modify.get('telegram')
                    )
                    session['telegram'] = modify['telegram']
                    session['userid'] = modify['telegram']
                if('email' not in modify):
                    self._model.update_user_email(
                        session['userid'],
                        ''
                    )
                    if session.get('email'):
                        session.pop('email')
                        session['userid'] = session['telegram']
                    self._model.update_user_preference(
                        session['userid'],
                        'telegram'
                    )
                if('telegram' not in modify):
                    self._model.update_user_telegram(
                        session['userid'],
                        ''
                    )
                    if session.get('telegram'):
                        session.pop('telegram')
                        session['userid'] = session['email']
                    self._model.update_user_preference(
                        session['userid'],
                        'email'
                    )
        if 'putuser' in request.values:
            page = page.replace(
                    '*modifyuser*',
                    '<p>Si prega di inserire almeno email o telegram \
per modificare l\'utente.</p>')
        user = self._model.read_user(session['userid'])
        page = page.replace('*nome*', user['name'] if user['name'] else '')
        page = page.replace(
            '*cognome*',
            user['surname'] if user['surname'] else ''
        )
        page = page.replace(
            '*email*',
            user['email'] if user['email'] else ''
        )
        page = page.replace(
            '*telegram*',
            user['telegram'] if user['telegram'] else ''
        )
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

    def show_user(self):
        fileHtml = html / 'showuser.html'
        page = fileHtml.read_text()
        userid = request.values.get('userid')
        if userid:
            email = self._model.get_user_email_from_id(userid)
            telegram = self._model.get_user_telegram_from_id(userid)
            user = email if email else telegram
            page = page.replace('*showuser*', self.load_web_user(user))
        page = page.replace('*showuser*', '')
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
            options += '<option value="' + str(values[i]) + '"'
            if str(values[i]) == userid:
                options += ' selected="selected"'
            options += '>'
            options += display[i]
            options += '</option>'
        options += '</select>'
        return page.replace('*userids*', options)

    def remove_project(self):
        fileHtml = html / 'removeproject.html'
        page = fileHtml.read_text()
        project = request.values.get('projectid')
        if project:
            page = page.replace(
                '*removeuser*',
                '<p>Progetto rimosso correttamente.</p>'
            )
            users = self._model.get_project_users(project)
            for user in users:
                if user.get('email'):
                    userid = user['email']
                elif user.get('telegram'):
                    userid = user['telegram']
                self._model.remove_user_project(userid, project)
            self._model.delete_project(project)
        page = page.replace('*removeproject*', '')
        values = self._projects_id()
        options = '<select id="projectid" name="projectid">'
        for value in values:
            options += '<option value="' + str(value) + '"'
            if str(value) == project:
                options += ' selected="selected"'
            options += '>'
            options += value
            options += '</option>'
        options += '</select>'
        return page.replace('*projectids*', options)


    def show_project(self):
        fileHtml = html / 'showproject.html'
        page = fileHtml.read_text()
        project = request.values.get('projectid')
        if project:
            page = page.replace(
                '*showproject*',
                self.load_web_project(project)
            )
        page = page.replace('*showproject*', '')
        values = self._projects_id()
        options = '<select id="projectid" name="projectid">'
        for value in values:
            options += '<option value="' + str(value) + '"'
            if str(value) == project:
                options += ' selected="selected"'
            options += '>'
            options += value
            options += '</option>'
        options += '</select>'
        return page.replace('*projectids*', options)

    def load_web_user(self, user: str):
        user_projects = self._model.get_user_projects(user)
        table = '<table id="topics-table"><tr><th>Url</th><th>Priorità</th>\
<th>Labels</th><th>Keywords</th></tr>'
        for user_project in user_projects:
            project_data = self._model.read_project(
                user_project['url']
            )
            project_data['url'] = project_data['url'].lstrip().rstrip()
            row = '<tr>'
            row += '<td><a href="' + project_data['url'] + '" target="_blank">' + project_data['url'] + '</a></td>'
            row += '<td>' + str(user_project['priority']) + '</td><td>'
            for topic in project_data['topics']:
                if topic in user_project['topics']:
                    row += topic + ','
            row = row[:-1]  # elimino l'ultima virgola
            row += '</td><td>'
            if user_project['keywords']:
                for keyword in user_project['keywords']:
                    row += keyword
                    row += ','
                row = row[:-1]  # elimino l'ultima virgola
            row += '</td></tr>'
            table += row
        table += '</table>'
        return table

    def load_web_project(self, project: str):
        project = self._model.read_project(project)
        table = '<table id="projects-table"><tr><th>Url</th><th>Name</th>\
<th>App</th><th>Topics</th></tr><tr><td>' + project['url'] + '</td>\
<td>' + project['name'] + '</td><td>' + project['app'] + '</td><td>'
        for topic in project['topics']:
            table += topic + ','
        table = table[:-1]  # elimino l'ultima virgola
        table += '</td></tr></table>'
        return table

    def web_user(self):
        if self._check_session():
            if request.method == 'GET':
                page = self.panel()
            elif request.method == 'POST':
                if 'postlogout' in request.values:
                    self.logout()
                    page = self.panel()
                elif 'postuserpanelshow' in request.values:
                    page = self.show_user()
                else:
                    page = self.add_user()
            elif request.method == 'PUT':
                page = self.modify_user()
            elif request.method == 'DELETE':
                page = self.remove_user()
            page = self.removehtml(page)
            try:
                return render_template_string(page)
            except TypeError:
                return page
        else:
            return self.access()

    def web_project(self):
        if self._check_session():
            if request.method == 'POST':
                page = self.show_project()
            elif request.method == 'DELETE':
                page = self.remove_project()
            page = self.removehtml(page)
            try:
                return render_template_string(page)
            except TypeError:
                return page
        else:
            return self.access()

    def load_preference_topic(self, message=''):
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
            row += '<td><a href="' + project_data['url'] + '" target="_blank">' + project_data['url'] + '</a></td>'
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
        form += '</table><input id="putpreferencetopics" type="button" \
value="Modifica preferenze di progetti e topic"></form>'
        form += message
        return form

    def load_preference_project(self, message=''):
        projects = self._model.projects()
        form = '<form id="projects"><select name="project" id="projects-select">'
        for project in projects:
            form += '<option value="' + project['url'] + '">\
' + project['name'] + '</option>'
        form += '</select> <input id="putpreferenceprojectsadd" type="button" \
value="Aggiungi il progetto">\
<input id="putpreferenceprojectsremove" type="button" \
value="Rimuovi il progetto"></form>'
        form += message
        return form

    def load_preference_availability(
        self,
        message='',
        year=datetime.datetime.now().year,
        month=datetime.datetime.now().month
    ):
        date = datetime.datetime(year, month, 1)
        irreperibilita = self._model.read_user(
            session['userid']
        ).get('irreperibilita')
        form = '<form id="availability">\
<fieldset id="availability-fieldset"><legend>Giorni di indisponibilità</legend>\
<div id="calendario"></div><p>' + date.strftime("%B") + ' \
' + date.strftime('%Y') + '</p>'
        for day in range(1, calendar.monthrange(year, month)[1]+1):
            date = datetime.datetime(year, month, day)
            form += '<input class="day_checkbox" type="checkbox"\
name="indisponibilita[]" id="day_' + str(date.day) + '" value="' + str(date) + '"'
            if irreperibilita and date in irreperibilita:
                form += ' checked="checked"'
            form += '/><label class="day_label" for="day_' + str(date.day) + '\
">' + str(day) + '</label>'
        form += '<br/><input type="button"\
 id="putpreferenceavailabilityprevious" value="Mese precedente"/>\
<input type="button"\
 id="putpreferenceavailabilitynext" value="Mese successivo"/>\
<input type="hidden" name="mese" value="' + date.strftime("%m") + '"/>\
<input type="hidden" name="anno" value="' + date.strftime("%Y") + '"/>\
<br/><input id="putpreferenceavailability" type="button"\
 value="Modifica irreperibilità"/></fieldset></form>'
        form += message
        return form

    def load_preference_platform(self, message=''):
        platform = self._model.read_user(session['userid']).get('preference')
        form = '<form id="platform"><fieldset id="platform-fieldset">\
<legend>Piattaforma preferita</legend>\
<label for="email">Email</label>\
<input name="platform" id="email"\
type="radio" value="email"'
        if(platform == 'email'):
            form += ' checked = "checked"'
        form += '/><label for="telegram">Telegram</label>\
<input name="platform" id="telegram" type="radio" value="telegram"'
        if(platform == 'telegram'):
            form += ' checked = "checked"'
        form += '/><input id="putpreferenceplatform" \
type="button" value="Modifica piattaforma preferita"/></fieldset></form>'
        form += message
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
                if firstTopic:
                    self._model.reset_user_topics(
                        session['userid'],
                        old
                    )
                firstTopic = True
                old = url
            if url != 'putpreferencetopics':
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
        return self.load_preference_topic('<p>Preferenze dei topic aggiornate.\
        </p>')

    def addproject(self):
        message = '<p>Progetto aggiunto correttamente.</p>'
        project = request.values.get('project')
        try:
            if project:
                self._model.add_user_project(session['userid'], project)
            else:
                message = '<p>Nessun progetto selezionato.</p>'
        except AssertionError:
            message = '<p>Il progetto è già presente in lista.</p>'
        return self.load_preference_topic(message)

    def removeproject(self):
        message = '<p>Progetto rimosso correttamente.</p>'
        project = request.values.get('project')
        try:
            if project:
                self._model.remove_user_project(session['userid'], project)
            else:
                message = '<p>Nessun progetto selezionato.</p>'
        except AssertionError:
            message = '<p>Il progetto non è presente in lista.</p>'
        return self.load_preference_topic(message)

    def indisponibilita(self):
        giorni = request.values.getlist('indisponibilita[]')
        month = request.values['mese']
        year = request.values['anno']
        giorni_old = self._model.read_user(
            session['userid']
        ).get('irreperibilita')
        giorni_new = []
        for giorno in giorni:
            giorni_new.append(
                datetime.datetime.strptime(giorno, '%Y-%m-%d %H:%M:%S')
            )
        if giorni_old:
            for giorno_old in giorni_old:
                if (
                    giorno_old.strftime('%Y') == year and
                    giorno_old.strftime('%m') == month
                ):
                    if (
                        (giorni_new and giorno_old not in giorni_new) or
                        not giorni_new
                    ):
                        self._model.remove_giorno_irreperibilita(
                            session['userid'],
                            int(year),
                            int(month),
                            int(giorno_old.strftime('%d'))
                        )
        if giorni_new:
            for giorno in giorni_new:
                self._model.add_giorno_irreperibilita(
                    session['userid'],
                    int(year),
                    int(month),
                    int(giorno.strftime('%d'))
                )
        return self.load_preference_availability('<p>Giorni di indisponibilità\
 aggiornati.</p>')

    def previous_indisponibilita(self):
        mese = int(request.values['mese'])
        anno = int(request.values['anno'])
        if (mese == 1):
            anno = anno - 1
            mese = 12
        else:
            mese = mese - 1
        self.indisponibilita()
        return self.load_preference_availability('<p>Giorni di indisponibilità\
 aggiornati, mese cambiato.</p>', anno, mese)

    def next_indisponibilita(self):
        mese = int(request.values['mese'])
        anno = int(request.values['anno'])
        if (mese == 12):
            anno = anno + 1
            mese = 1
        else:
            mese = mese + 1
        self.indisponibilita()
        return self.load_preference_availability('<p>Giorni di indisponibilità\
 aggiornati, mese cambiato.</p>', anno, mese)

    def piattaforma(self):
        platform = request.values['platform']
        if platform == "telegram":
            telegram = self._model.get_user_telegram_web(session['userid'])
            if not telegram:
                return self.load_preference_platform('<p>Non hai\
 memorizzato la piattaforma telegram nel sistema.</p>')
        if platform == "email":
            email = self._model.get_user_email_web(session['userid'])
            if not email:
                return self.load_preference_platform('<p>Non hai\
 memorizzato la piattaforma email nel sistema.</p>')
        self._model.update_user_preference(session['userid'], platform)
        return self.load_preference_platform('<p>Piattaforma preferita \
aggiornata correttamente.</p>')

    def modify_preference(self):
        fileHtml = html / 'preference.html'
        page = fileHtml.read_text()
        if 'putpreferencepanel' in request.values:
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
        elif request.values.get('putpreferencetopics'):
            return self.modifytopics()
        elif request.values.get('putpreferenceprojectsadd'):
            return self.addproject()
        elif request.values.get('putpreferenceprojectsremove'):
            return self.removeproject()
        elif request.values.get('putpreferenceavailability'):
            return self.indisponibilita()
        elif request.values.get('putpreferenceavailabilityprevious'):
            return self.previous_indisponibilita()
        elif request.values.get('putpreferenceavailabilitynext'):
            return self.next_indisponibilita()
        elif request.values.get('putpreferenceplatform'):
            return self.piattaforma()
        return page

    def web_preference(self):
        if self._check_session():
            page = self.modify_preference()
            page = self.removehtml(page)
            try:
                return render_template_string(page)
            except TypeError:
                return page
        else:
            return self.access()

    def removehtml(self, page: str):
        if 'panel' in request.values:
            page = page.replace("<!DOCTYPE html>", "")
            page = page.replace("<html id=\"html\">", "")
            page = page.replace("</html>", "")
        return page
