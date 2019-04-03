from pathlib import Path
import json

import flask

from producer.server import FlaskServerCreator, FlaskServer
from producer.gitlab.creator import GitlabProducerCreator
from producer.gitlab.producer import GitlabProducer

_CONFIG_PATH = Path(__file__).parents[1] / 'config.json'


def _open_configs(path: Path):
    with open(path) as file:
        config = json.load(file)
    return config

def main():
    configs = _open_configs(_CONFIG_PATH)
    producer = GitlabProducerCreator().create(configs['kafka'])

    server = FlaskServer(Flask(__file__), producer, 'gitlab')
    server.run(configs)

if __name__ == '__main__':
    main()
