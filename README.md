# Barbershop Web

The objective of this application is to provide a service to be used in self attendance projects.
This project will contain all the auth service and the rest API to be used by mobile apps.

## Requirements

- [Docker](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
- [Docker-Compose](https://docs.docker.com/compose/install/)

### How to use

First you should install the docker and docker-compose applications (links on requirements session).

- `docker-compose build` to build the container;
- `docker-compose up` to run the server (you can pass `-d` to run in backgroud);
- `docker-compose stop` to stop the server;
- `docker container prune -f` if you need to delete the container;
- `docker volume prune -f` if you need to delete the database;
- `docker network prune -f` if you need to delete the network;
- `docker kill $(docker ps -q)` if you need to kill all docker instances;

* The server will run on `localhost:8000`

#### Creating a superuser

You can create a superuser to access admin painel and other things, you just need to run:

- Install [python 3.x](https://www.python.org/downloads/);
- Install python-pip using `apt-get install python-pip`;
- Install the dependencies using `pip install -r requirements.txt`;
- Export the *SECRET_KEY* to env vars using `export SECRET_KEY="9d4#+**cl85%3zw0019s89j-*sfum1*o6mo((mq%caxd3cdyv3"` (Only Once);
- Create the user using `python manage.py createsuperuser`;

### Documentation

You can get all the documentation on docs folder.

### Code Quality

We use some tools to ensure our code quality.

- `pylint`
- `django-lint`
- `pytest`
