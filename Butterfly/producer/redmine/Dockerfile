# Base image
FROM python:alpine3.7

# Copying files from the correct folders
COPY /producer/redmine/RedmineProducer.py ./Butterfly/producer/redmine/
COPY /producer/redmine/requirements.txt ./Butterfly/producer/redmine/
COPY /producer/redmine/__init__.py ./Butterfly/producer/redmine/
COPY /producer/producer.py ./Butterfly/producer/
COPY /producer/config.json ./Butterfly/producer/
COPY /webhook/redmine/RedmineIssueWebhook.py ./Butterfly/webhook/redmine/
COPY /webhook/redmine/open_issue_redmine_webhook.json ./Butterfly/webhook/redmine
COPY /webhook/webhook.py ./Butterfly/webhook/
COPY topics.json ./Butterfly/
 
# Change current directory
WORKDIR /Butterfly

# Installing dependencies
RUN pip3 install --upgrade pip ; pip3 install -r producer/redmine/requirements.txt

# Run after the dependencies have been installed
CMD python3 -m producer.redmine.RedmineProducer
