AI at NC State Website
==================

A one stop website to find all news, updates, and much more regarding the Artificial Intelligence Club at North Carolina State University.

<a href="https://github.com/vchaptsev/cookiecutter-django-vue">
    <img src="https://img.shields.io/badge/built%20with-Cookiecutter%20Django%20Vue-blue.svg" />
</a>

### Table of Contents

- [Development](#Development)
- [Running Tests](#Running Tests)
  - [Backend Testing](#Backend Testing)
  - [Frontend Testing](#Frontend Testing)

## Development

Install [Docker](https://docs.docker.com/install/) and [Docker-Compose](https://docs.docker.com/compose/). Start your virtual machines with the following shell command:

`docker-compose up --build`

If all works well, you should be able to create an admin account with:

`docker-compose run --rm backend python manage.py createsuperuser`


## Running Tests

### Backend Testing

Run the unit tests with:

`docker-compose run --rm backend coverage run --omit='*/venv/*','*/migrations/*','*/tests/*' manage.py test`

Run the following to view the test coverage breakdown in the terminal:

`docker-compose run --rm backend coverage report`

If you wish to view a more detailed breakdown of the test coverage report, you can generate an HTML version of the report which allows you to explore which lines of code were run, missed or excluded. After running the following command, open the `index.html` file in the `backend/htmlcov` directory in your browser:

`docker-compose run --rm backend coverage html`

### Frontend Testing
TODO
