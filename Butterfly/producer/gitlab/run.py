from pathlib import Path
import json

from flask import Flask

from producer.server import FlaskServer
from producer.creator import KafkaProducerCreator
from producer.gitlab.producer import GitlabProducer
from webhook.gitlab.factory import GitlabWebhookFactory

_CONFIG_PATH = Path(__file__).parents[1] / 'config.json'


def _open_configs(path: Path):
    with open(path) as file:
        config = json.load(file)
    return config


def main():
    configs = _open_configs(_CONFIG_PATH)
    kafka = KafkaProducerCreator().create(configs['kafka'])
    producer = GitlabProducer(kafka, GitlabWebhookFactory())

    server = FlaskServer(Flask(__name__), producer, 'gitlab')
    server.run(configs)


if __name__ == '__main__':
    main()
