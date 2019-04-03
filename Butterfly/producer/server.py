import json
from pathlib import Path
from pprint import pformat
from abc import ABC, abstractmethod

from flask import Flask
from flask import request

from producer.producer import Producer
from producer.creator import ServerCreator, ProducerCreator


_CONFIG_PATH = Path(__file__).parents[0] / 'config.json'


class Server(ABC):
    """Interfaccia `Server`. Avvia il Server con il metodo `run()`,
    un parametro opzionale
    `config_path`, contenente il path al file con le configurazioni
    necessarie.
    """
    @abstractmethod
    def run(self, config_path):
        """Avvia il `Server`

        Parameters:

        `config_path` - Path al file contenente le configurazioni per l'avvio.
        """


class FlaskServer(Server):
    """Implementa `Server`.
    Avvia il server `Flask` che resta in ascolto degli webhook in base a
    come è configurato.
    """

    def __init__(self, flask: Flask, producer: Producer, topic: str):
        self._app = flask
        self._producer = producer
        self._topic = topic
        self._app.add_url_rule(
            '/',
            view_func=self._webhook_handler,
            methods=['POST']
        )

    def _webhook_handler(self) -> (str, int):
        """Processa il webhook e verifica se è malformato.

        Returns:

        `200` - Il webhook è stato inoltrato con successo.\n
        `400` - La richiesta non è di tipo `application/json`\n
        `401` - Il `Producer` non è stato in grado di inviare il
            messaggio
        """
        if request.headers['Content-Type'] == 'application/json':

            webhook = request.get_json()
            print(
                '\n\n\nMessaggio da GitLab:\n'
                f'{pformat(webhook)}\n\n\n'
                'Parsing del messaggio ...'
            )

            try:
                self._producer.produce(webhook)
                print('Messaggio inviato.\n\n')
            except KeyError:
                print('Warning: messaggio malformato. '
                      'Non è stato possibile effettuare il parsing.\n'
                      'In attesa di altri messaggi...\n\n')
                return 'Messaggio malformato', 402
            except NameError:
                return 'Tipo di messaggio non riconosciuto', 401  # Errore messaggio malformato
            return 'Ok', 200  # Ok

        return '', 400  # Errore, tipo di richiesta non adatta

    def run(self, config_path=_CONFIG_PATH):
        """Avvia il `FlaskServer` con le configurazioni nel file
        contenuto in `config_path`.

        Parameters:

        `config_path` - path contenente le configurazioni necessarie all'avvio
            del server."""
        config = _open_configs(config_path)

        self._app.run(
            host=config[self._topic]['ip'],
            port=config[self._topic]['port']
        )


class FlaskServerCreator(ServerCreator):
    """Creator di FlaskServer. Si occupa di
    restituire un `FlaskServer` istanziato.
    """

    def __init__(self, creator: ProducerCreator):
        assert isinstance(creator, ProducerCreator)
        self._creator = creator

    def initialize_app(self, topic: str, config_path=_CONFIG_PATH) -> Server:
        """Inizializza il Server di tipo `topic` e lo restituisce.

        Parameters:

        `topic` - stringa con il nome del topic su cui restare in ascolto"""
        configs = _open_configs(
            _CONFIG_PATH)

        flask = Flask(__name__)
        producer = self._creator.create(configs['kafka'])  # O senza il campo

        app = FlaskServer(flask, producer, topic)
        return app


def _open_configs(path: Path):
    with open(path) as file:
        config = json.load(file)
    return config
