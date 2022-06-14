FROM python:3.9.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV TZ="Europe/Moscow"
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY ./config/pip/requirements.txt /tmp/requirements.txt

RUN pip install -U pip
RUN pip install -Ur /tmp/requirements.txt
RUN mkdir /tmp/data-proj

COPY ./config/docker-env/.env /tmp/data-proj/.env

RUN chmod -R 777 /tmp/data-proj

WORKDIR /