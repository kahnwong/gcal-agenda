FROM python:3.8.6-slim-buster

WORKDIR /var/www/html

RUN apt update && apt install jq apache2 -y
COPY ./Pipfile.lock ./Pipfile.lock
RUN jq -r '.default | to_entries[] | .key + .value.version ' Pipfile.lock > requirements.txt
RUN pip install -r requirements.txt

COPY ./credentials.json ./credentials.json
COPY ./*.py ./
COPY ./token.pickle ./token.pickle

EXPOSE 80
CMD apachectl -D FOREGROUND