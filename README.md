[![Pipeline](https://github.com/taller2-grupo5-rostov-1c2022/messages-server/actions/workflows/pipeline.yml/badge.svg?branch=master)](https://github.com/taller2-grupo5-rostov-1c2022/messages-server/actions/workflows/pipeline.yml)
[![codecov](https://codecov.io/gh/taller2-grupo5-rostov-1c2022/messages-server/branch/master/graph/badge.svg?token=mUN5qQzBYJ)](https://codecov.io/gh/taller2-grupo5-rostov-1c2022/messages-server)
[![](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/)
[![](https://img.shields.io/badge/docs-fastapi-blue.svg)](https://fastapi.tiangolo.com/)


# Spotifiuby Messages Server


## Installing the project

The only dependency required to use this template is [poetry](https://python-poetry.org). The recommended method to install it is through [pip](https://pypi.org/project/pip/).

```bash
$ pip3 install poetry
$ poetry config virtualenvs.in-project true
```

Remember to commit to the repo the `poetry.lock` file generated by `poetry install`.


## Dependencies

The virtual environment is automatically created and activated via poetry.

```
$ cd to-project-path
$ poetry install
```

To make sure everything is set up correctly, run the following command which must show the virtual environment path:

```
$ poetry show -v
```

If still having problems, you can run `source` command to enable the virtual environment from the shell:

```
$ poetry show -v
Using virtualenv: /home/<User>/<path>/taller2/fastapi-template/.venv
$ source .venv/bin/activate
```

### Adding new dependencies

Check the [full poetry docs](https://python-poetry.org/docs/cli/), but here goes a quick reminder,

```bash
poetry add <dependency> [--dev]
```

### Style guide

This template follows [PEP8](https://www.python.org/dev/peps/pep-0008/).

For this purpose, we use:

- [black](https://github.com/psf/black): an opinionated code formatting tool
- [flake8](https://github.com/PyCQA/flake8): a tool to enforce style guide
- [pylint](https://github.com/PyCQA/pylint): a source code, bug and quality checker

**Linters**

```bash
flake8 && pylint <module_name>
```

**Formatter**
```bash
black .
```

## Running the server

- Development: `uvicorn src.main:app --reload`
- Production: `uvicorn src.main:app`

## Docker

You need [docker-compose](https://docs.docker.com/compose/) and [docker](https://docs.docker.com/) to run the following containers
and commands.

### Developing with container and database

```bash
$ sudo ./scripts/test-container.sh
```

### Running tests within container

You have two options here, one is simple running:

```bash
$ sudo ./scripts/coverage-container.sh
```

which will execute all the tests and will exit the container afterwards.

Alternately, you can also run a container which will run the app and will provide the database. In one terminal run:

```bash
$ sudo ./scripts/test-container.sh
```

Then in other terminal run `docker ps` and copy the `container ID` from the `docker_fastapi-server` image:

```bash
$ docker ps
CONTAINER ID   IMAGE                   COMMAND                  CREATED              STATUS              PORTS                                       NAMES
b1e9c7c4e040   docker_fastapi-server   "./docker-entrypoint…"   About a minute ago   Up About a minute   0.0.0.0:8082->8082/tcp, :::8082->8082/tcp   docker_fastapi-server_1
620c0b75ce2a   mongo                   "docker-entrypoint.s…"   About a minute ago   Up About a minute   0.0.0.0:5438->5432/tcp, :::5438->5432/tcp   docker_postgres_1
```

Finally, enter the container with `docker exec -it [container-id] bash` and run the tests within the container using `poetry run pytest`:

```bash
$ docker exec -it [container-id] bash
$ root@b1e9c7c4e040:/code# ls
docker-entrypoint.sh  poetry.lock  pyproject.toml  src  tests  scripts
$ root@b1e9c7c4e040:/code# poetry run pytest
```

## API Documentation

Documentation will be automatically generated at `{app}/docs`

## Tests

We use the [pytest framework](https://fastapi.tiangolo.com/tutorial/testing/) to test. The easiest way to run tests is `pytest`.
Remember to create functions with a name that starts with `test_` (this is standard pytest conventions).

## Github Actions

A few pipelines have been set to run on github actions to ensure code quality and deployment.

- Run Linter
- Run Tests
- Upload Test Coverage
- Deploy to Heroku using docker image

### Upload Coverage to Codecov

The pipeline automatically generates a coverage report and uploads it to [codecov](https://about.codecov.io/)

You'll need to set the following actions secrets:

- `CODECOV_TOKEN`: Repo Token. Can be obtained on codecov when setting up or on settings

## Heroku

You'll need to set the following actions secrets:

- `HEROKU_APP_NAME`: App name
- `HEROKU_EMAIL`: Account email
- `HEROKU_API_KEY`: Account [API key](https://dashboard.heroku.com/account)


## MongoDB

This server uses [MongoDB](https://www.mongodb.com/) as its database.
Set `MONGO_URL` as an environment variable and action secret to connect to the database.

## Firebase

To access the database and storage, you'll need to generate a Firebase private key.

To do so, go to **Project configuration** > **Service accounts** > **Generate new private key**. [[Link](https://console.firebase.google.com/u/0/project/rostov-spotifiuby/settings/serviceaccounts/adminsdk)]

Save the file as `google-credentials.json` in the root directory of the repository.

You can also set `TESTING=1` as an environment variable to use mocks of the database
and storage for testing purposes.

In order to load the credentials in Heroku, set `GOOGLE_CREDENTIALS` as an environment variable in Heroku, and paste the content of the `google-credentials.json` file.

## Datadog

The heroku Dockerfile includes the DataDog agent.  Create a new DataDog API Key from [here](https://app.datadoghq.com/organization-settings/api-keys).
Also, you need to set the following config vars in Heroku (you can use [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) if you want):
```bash
DD_API_KEY=<api_key_from_datadog>
DD_DYNO_HOST=false
HEROKU_APP_NAME=<app_name>
DD_TAGS=service:<meaningful_tag_for_datadog>
```
