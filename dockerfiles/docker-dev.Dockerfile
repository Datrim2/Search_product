FROM solovyev/python-base:latest

RUN mkdir /code
RUN mkdir /logs
RUN chmod -R 777 /logs

WORKDIR /code/ParseSite/