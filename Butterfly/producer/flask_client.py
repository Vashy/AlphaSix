import json
from pathlib import Path
from pprint import pprint
from abc import ABC, abstractmethod

from flask import Flask
from flask import request

from producer.producer import Producer
from producer.gitlab.creator import GitlabProducerCreator



class Server(ABC):
    @abstractmethod
    def app(self):
        pass
    
    @abstractmethod
    def run(self):
        pass


class FlaskServer(Server):  # FlaskClient
    _config_path = Path(__file__).parents[1] / 'config.json'

    def __init__(self, flask: Flask, producer: Producer):
        self._app: Flask = flask
        self._producer: Producer = producer

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
            host=self.config['gitlab']['ip'],
            port=self.config['gitlab']['port']
        )

    @staticmethod
    def initialize_app(config_path=FlaskClient._config_path):
        configs = FlaskClient._open_configs(config_path)

        flask = Flask(__name__, configs['gitlab'])

        creator = GitlabProducerCreator()
        producer = creator.create(configs['kafka'])  # O senza il campo

        app = FlaskClient(flask, producer)
        return app

    @staticmethod
    def _open_configs(path: Path):
        with open(path) as f:
            config = json.load(f)
        return config
