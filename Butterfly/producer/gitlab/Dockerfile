# Base image
FROM python:3.7

# Expose port 5000
EXPOSE 5000

# Copying files from the correct folders
COPY /producer/gitlab/GLProducer.py ./Butterfly/producer/gitlab/
COPY /producer/gitlab/requirements.txt ./Butterfly/producer/gitlab/
COPY /producer/gitlab/__init__.py ./Butterfly/producer/gitlab/
COPY /producer/producer.py ./Butterfly/producer/
COPY /producer/__init__.py ./Butterfly/producer/
COPY /producer/config.json ./Butterfly/producer/
COPY /webhook/gitlab/GLIssueWebhook.py ./Butterfly/webhook/gitlab/
COPY /webhook/webhook.py ./Butterfly/webhook/
COPY /webhook/webhook.json ./Butterfly/webhook/
COPY topics.json ./Butterfly/

# Change current directory
WORKDIR /Butterfly

# Installing dependencies
RUN ls -la producer ; pip3 install --upgrade pip ; pip3 install -r producer/gitlab/requirements.txt

# Run after the dependencies have been installed
CMD python3 -m producer.gitlab.GLProducer
