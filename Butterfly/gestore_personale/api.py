import json
import datetime

from flask import request
import flask_restful
from bson.json_util import dumps

from mongo_db.facade import MongoFacade
from gestore_personale.observer import Subject


class SubjectResource(type(Subject), type(flask_restful.Resource)):
    pass


class Resource(Subject, flask_restful.Resource, metaclass=SubjectResource):

    def __init__(self, model: MongoFacade):
        super(Resource, self).__init__()
        self._model = model

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

    def put(self, url: str) -> dict:
        data = request.get_json(force=True)
        return self.notify('preference', 'PUT', url, data)


class ApiHandler:

    def __init__(
        self,
        model: MongoFacade
    ):
        self._model = model

    def api_user(self, request_type: str, url: str, msg: str):
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
                return {'error': 'Si prega di inserire almeno email o telegram\
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
                    if email:
                        self._model.update_user_preference(email, 'email')
                    elif telegram:
                        self._model.update_user_preference(
                            telegram,
                            'telegram'
                        )
                    return {'ok': 'Utente inserito correttamente'}, 200
            else:
                return {'error': 'Si prega di inserire almeno email o telegram\
per inserire l\'utente.'}, 409

    def api_preference(self, request_type: str, url: str, msg: str):
        tipo = msg.get('tipo')
        if tipo == 'progetto':
            project = msg.get('project')
            priority = msg.get('priority')
            topics = msg.get('topics')
            keywords = msg.get('keywords')
            self._model.set_user_priority(
                url, project, priority
            )
            self._model.reset_user_topics(
                url,
                project
            )
            self._model.add_user_topics(
                url,
                project,
                topics
            )
            self._model.reset_user_keywords(
                url,
                project
            )
            self._model.add_user_keywords(
                url,
                project,
                keywords
            )
            return {'ok': 'Preferenza modificata correttamente'}, 200
        elif tipo == 'irreperibilita':
            giorni = msg.get('giorni')
            giorni_old = self._model.read_user(
                url
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
                                url,
                                int(year),
                                int(month),
                                int(giorno.strftime('%d'))
                            )
                for giorno in giorni_new:
                    self._model.add_giorno_irreperibilita(
                        url,
                        int(year),
                        int(month),
                        int(giorno.strftime('%d'))
                    )
            return {'ok': 'Preferenza modificata correttamente'}, 200
        elif tipo == 'piattaforma':
            platform = msg.get('platform')
            if platform == "telegram":
                telegram = self._model.get_user_telegram_web(url)
                if not telegram:
                    return {'error': 'Telegram non presente nel sistema.'}, 404
            if platform == "email":
                email = self._model.get_user_email_web(url)
                if not email:
                    return {'error': 'Email non presente nel sistema.'}, 404
            self._model.update_user_preference(url, platform)
            return {'ok': 'Preferenza modificata correttamente'}, 200
