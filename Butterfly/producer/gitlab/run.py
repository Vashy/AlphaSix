from producer.server import FlaskServerCreator
from producer.gitlab.creator import GitlabProducerCreator
# from webhook.gitlab.GLIssueWebhook import GLIssueWebhook


def main():
    application = 'gitlab'
    creator = FlaskServerCreator(GitlabProducerCreator())
    app = creator.initialize_app(application)
    app.run()


if __name__ == '__main__':
    main()
