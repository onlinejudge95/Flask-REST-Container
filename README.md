Flask-REST-Container
====================


![Gitlab pipeline status](https://img.shields.io/gitlab/pipeline/onlinejudge95/Flask-REST-Container)
![GitHub language count](https://img.shields.io/github/languages/count/onlinejudge95/Flask-REST-Container)
![GitHub top language](https://img.shields.io/github/languages/top/onlinejudge95/Flask-REST-Container)
![GitHub issues](https://img.shields.io/github/issues-raw/onlinejudge95/Flask-REST-Container)
![GitHub pull requests](https://img.shields.io/github/issues-pr-raw/onlinejudge95/Flask-REST-Container)
![GitHub](https://img.shields.io/github/license/onlinejudge95/Flask-REST-Container)
![GitHub last commit](https://img.shields.io/github/last-commit/onlinejudge95/Flask-REST-Container)
![GitHub repo size](https://img.shields.io/github/repo-size/onlinejudge95/Flask-REST-Container)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/onlinejudge95/Flask-REST-Container)
![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/onlinejudge95/Flask-REST-Container)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/onlinejudge95/Flask-REST-Container)
[![Beerpay](https://beerpay.io/onlinejudge95/Flask-REST-Container/badge.svg)](https://beerpay.io/onlinejudge95/Flask-REST-Container)

## Code Of Conduct
To read the Code of Conduct please go [here](https://github.com/onlinejudge95/Flask-REST-Container/tree/master/.github/CODE_OF_CONDUCT.md)

## License
To read the License please go [here](https://github.com/onlinejudge95/Flask-REST-Container/tree/master/LICENSE)

## Contributing
To read the Contributing guidelines please go [here](https://github.com/onlinejudge95/Flask-REST-Container/tree/master/.github/CONTRIBUTING.md)

## Feature Request / Bug Report
To report a bug go [here](https://github.com/onlinejudge95/Flask-REST-Container/tree/master/.github/ISSUE_TEMPLATE/bug-report.md)

To request for a feature please go [here](https://github.com/onlinejudge95/Flask-REST-Container/tree/master/.github/ISSUE_TEMPLATE/feature_request.md)

## Info
This template aims to provide a boilerplate ready **REST API Server** using `Flask`.
The server is orchestrated through a `Dockerfile`.

## Dependencies
Dependencies of the server are defined in `Pipfile`.
Mostly if you would be using `docker`, dependency management would be taken care of.

## Pipelines
For pipeline and providing Continuous Integration along with Continuous Delievery, the pipeline is
running in [GitLab CI/CD](https://gitlab.com/onlinejudge95/Flask-REST-Container/pipelines).
Following steps are present.
* **test**
    In this section, first the unit tests are run followed by functional tests.
* **build**
    In this section, docker image is built and pushed to the container registry at gitlab,
    to see whether the docker container can be built.

If the branch that is currently running is **master** then the last **deploy** stage also executes
* **deploy**
    In this section, the code is deployed to [heroku](https://rest-container-staging.herokuapp.com/).

## Containers
* For *Visual Studio Code*

If you are using *Visual Studio Code* you can directly launch the container by the following.
There is a `.devcontainer/devcontainer.json` file provided, use this to open the folder in a container.
* For *Else*
1. Make sure your `docker` demon is **up**.
2. Build the docker image.
    ```
    $ docker-compose build
    ```
3. Start the docker container.
    ```
    $ docker-compose up --build --detach
    ```
4. For running tests run the following command
    ```
    $ docker-compose exec users pipenv run pytest
    ```
5. For linting your code run
    ```
    $ pipenv run black --config pyproject.toml app/**/*.py
    ```
6. For creating a new database run
    ```
    $ docker-compose exec users pipenv run python manage.py init_db
    ```
7. For seeding a new database run
    ```
    $ docker-compose exec users pipenv run python manage.py seed_db
    ```
For dev environment the dependency management is done by `pipenv`, so prefix all commands with `pipenv run`

## Contact
In case of any issues reach out to [onlinejudge95](https://github.com/onlinejudge95)
