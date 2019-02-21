# Base image
FROM python:alpine3.7

# Expose port 5000
EXPOSE 5000

# Copying files from the correct folders
COPY /consumer/email/EmailConsumer.py ./Butterfly/consumer/email/
COPY /consumer/email/requirements.txt ./Butterfly/consumer/email/
COPY /consumer/email/__init__.py ./Butterfly/consumer/email/
COPY /consumer/consumer.py ./Butterfly/consumer/
COPY /consumer/config.json ./Butterfly/consumer/
COPY /webhook/webhook.py ./Butterfly/webhook/
COPY topics.json ./Butterfly/
 
# Change current directory
WORKDIR Butterfly

# Installing dependencies
RUN pip3 install --upgrade pip ; pip3 install -r consumer/email/requirements.txt

# Run after the dependencies have been installed
CMD python3 -m consumer.email.EmailConsumer
