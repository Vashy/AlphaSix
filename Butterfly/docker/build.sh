#!/bin/bash

# Costruzione delle immagini
docker build --no-cache --tag producer_redmine -f ../producer/redmine/Dockerfile . ;
docker build --no-cache --tag producer_gitlab -f ../producer/gitlab/Dockerfile . ;
docker build --no-cache --tag consumer_telegram -f ../consumer/telegram/Dockerfile . ;
docker build --no-cache --tag consumer_email -f ../consumer/email/Dockerfile . ;

#
docker-compose -f gitlab.yml up ;
docker-compose -f redmine.yml up ;
docker-compose -f kafka.yml up ;
# docker-compose -f jenkins.yml up ;

sleep 1m ;

# 
docker-compose -f producer-gitlab.yml up ;
docker-compose -f producer-redmine.yml up ;

# 
docker-compose -f comsumer-email.yml up ;
docker-compose -f consumer-telegram.yml up ;