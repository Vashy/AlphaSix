import json
from pathlib import Path
from pprint import pprint
from abc import ABC, abstractmethod

from flask import Flask
from flask import request

from producer.producer import Producer
from producer.creator import ServerCreator
from producer.gitlab.creator import GitlabProducerCreator


class Server(ABC):
    @property
    @abstractmethod
    def app(self):
        pass
    
    @abstractmethod
    def run(self):
        pass


class FlaskServer(Server):  # FlaskServer

    def __init__(self, flask: Flask, producer: Producer, application: str):
        self._app = flask
        self._producer = producer
        self._application = application

    @property
    def app(self) -> Flask:
        return self._app

    @app.route('/', methods=['GET', 'POST'])
    def api_root(self):

        if request.headers['Content-Type'] == 'application/json':

            """Fetch dei topic dal file topics.json
            Campi:
            - topics['id']
            - topics['label']
            - topics['project']
            """

            webhook = request.get_json()
            print(
                '\n\n\nMessaggio da GitLab:\n'
                f'{pprint.pformat(webhook)}\n\n\n'
                'Parsing del messaggio ...'
            )

            try:
                self._producer.produce(webhook)
                print('Messaggio inviato.\n\n')
            except KeyError:
                print('Warning: messaggio malformato. '
                      'Non è stato possibile effettuare il parsing.\n'
                      'In attesa di altri messaggi...\n\n')

            return '', 200

        else:
            return '', 400

    def run(self):
        self.app.run(
            host=self.config[self._application]['ip'],
            port=self.config[self._application]['port']
        )


class FlaskServerCreator(ServerCreator):
    _config_path = Path(__file__).parents[1] / 'config.json'

    def __init__(self, creator: ProducerCreator):
        assert isinstance(creator, ProducerCreator)
        self._creator = creator

    def initialize_app(application: str):
        configs = FlaskServer._open_configs(FlaskServerCreator._config_path)

        flask = Flask(__name__, configs[application])
        producer = self._creator.create(configs['kafka'])  # O senza il campo

        app = FlaskServer(flask, producer)
        return app

    @staticmethod
    def _open_configs(path: Path):
        with open(path) as f:
            config = json.load(f)
        return config
