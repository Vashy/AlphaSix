from producer.server import FlaskServerCreator
from producer.gitlab.creator import GitlabProducerCreator


def main():
    topic = 'gitlab'
    creator = FlaskServerCreator(GitlabProducerCreator())
    app = creator.initialize_app(topic)
    app.run()


if __name__ == '__main__':
    main()
