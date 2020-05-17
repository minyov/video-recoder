FROM python:3.8

MAINTAINER Minev

ENV CONTAINER_PROJECT=/opt/stepik

WORKDIR $CONTAINER_PROJECT

RUN apt-get update && apt-get install -y daemon

COPY . $CONTAINER_PROJECT

RUN pip3 install -r $CONTAINER_PROJECT/requirements.txt