AI at NC State Website
==================

A one-stop website to find all news, updates, and much more regarding the Artificial Intelligence Club at North Carolina State University.

<a href="https://github.com/vchaptsev/cookiecutter-django-vue">
    <img src="https://img.shields.io/badge/built%20with-Cookiecutter%20Django%20Vue-blue.svg" alt="Built with cookie cutter badge"/>
</a>

### Table of Contents

- [Development](#Development)
  - [Getting Started](#Getting-Started)
  - [Loading Development Database Fixtures](#Loading-Development-Database-Fixtures)
- [Backend Testing](#Backend-Testing)
  - [Running All Backend Tests](#Running-All-Backend-Tests)
  - [Running a Subset of Backend Tests](#Running-a-Subset-of-Backend-Tests)
  - [Generating Test Coverage Reports](#Generating-Test-Coverage-Reports)
- [Frontend Testing](#Frontend-Testing)

## Development

### Getting Started

Install [Docker](https://docs.docker.com/install/) and [Docker-Compose](https://docs.docker.com/compose/) or make sure they are updated to the latest version if they are already installed. Build and start the development Docker containers with the following command:

`docker-compose up --build`

If all works well, you should be able to create an admin account with:

`docker-compose run --rm backend python manage.py createsuperuser`

### Loading Development Database Fixtures

`docker-compose run --rm backend python manage.py loaddata dev-fixtures.json`

### Dumping Development Database Fixtures

`docker-compose run --rm backend python manage.py dumpdata --exclude=auth --exclude=contenttypes --exclude=admin --exclude=sessions --exclude=users -o dev-fixtures.json`

## Backend Testing

### Running All Backend Tests
You can run all the backend unit tests at once with the following command:

`docker-compose run --rm backend coverage run manage.py test`

### Running a Subset of Backend Tests
Every backend unit test should be decorated with the [Django tag decorator](https://docs.djangoproject.com/en/3.2/topics/testing/tools/#tagging-tests) to enable the running of smaller subsets tests that are common in some way. Tags should be defined as attributes of the `Tags` enumeration in the `core.testcases` module. The following is an example of tagging a test:
```
from core.testcases import Tags, VerboseTestCase

class ExampleTestCase(VerboseTestCase):
    @tag(Tags.MODEL)
    def test_model_example(self):
        self.fail('Not yet implemented.')
```
Following from this example, in order to only run units tests with the `MODEL` tag, you can run the following command:

`docker-compose run --rm backend python manage.py test --tag=model`

Note that you use the enumeration member *value* `'model'` rather than the name of the member `MODEL`. Also note that coverage cannot be used when running tests in this manner.

For more complex usage of Django tags (e.g., tagging a test with multiple tags, and excluding tests by tag when running tests) please refer to the [official documentation](https://docs.djangoproject.com/en/3.2/topics/testing/tools/#tagging-tests).

### Generating Test Coverage Reports

In order to view the test coverage breakdown of the most recent test execution, run the following command after doing a full run of all the tests:

`docker-compose run --rm backend coverage report`

Alternatively, if you wish to view a more detailed breakdown of the test coverage report, you can generate an HTML version of the report which allows you to explore which lines of code were run, missed or excluded. First, run the following command:

`docker-compose run --rm backend coverage html`

Then, open the generated `index.html` file in the `backend/htmlcov` directory with your preferred web browser.

## Frontend Testing

TODO
