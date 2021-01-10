<p align="center">
  <a href="https://github.com/fpaludi/BooksFastAPI/actions?query=workflow%3ABuild">
  <img src="https://github.com/fpaludi/BooksFastAPI/workflows/Build/badge.svg">
  </a>
  <a href="https://github.com/fpaludi/BooksFastAPI/actions?query=workflow%3ATest">
  <img src="https://github.com/fpaludi/BooksFastAPI/workflows/Test/badge.svg">
  </a>
  <a href="https://codecov.io/gh/fpaludi/BooksFastAPI">
  <img src="https://img.shields.io/codecov/c/github/fpaludi/BooksFastAPI">
  </a>
</p>


# Book API

## Introduction

This project is about creating a REST API using [Fast API](https://fastapi.tiangolo.com) 
as a python framework. The main goal is showing how to create a development/testing docker 
based environment to run the API, its unit and integration tests in a easy and confortable way.

The API is a services useful to consult a review a Books database. It also has reviews
from an outside source: [Good Reads](https://www.goodreads.com).

The service support user Sign In and Log In, look for certain a book based on its ISBN,
title or author. The users can insert reviews and comments about the read books. All 
this data is stored in a PostgreSQL data base.


## Running the API
### Prerequisites
The project that system has installed:
  * Docker
  * Docker Compose
  * Makefile
  * Python >= 3.7

### Running with docker
The first step is to create a **app/.env** file, for that it is recommended to use
**app/.example.env** as a guide.

Then, it is necessary to build the images for the project. From the project root 
path run (it can take several minutes):

```bash
make build
```

One you have the images created you can start the API by running:

```bash
make run
```

and in you browser access to **http://127.0.0.1:8000/docs**. This URL provides
documentation about the different endpoints available. Also, note that the code is 
mounted in the docker container as volume, so it is possible to develop the 
application without rebuilding the images with each code change.


Finally you can stop it with simply running:
```bash
make stop
```

### Running with docker: Development and testing
Other alternative is to run the API with development and testing purposes. In order to do that you need to run: 

```bash
make build_dev
make run_dev
```

The test are run with
```bash
make run_tests
```

The previous commands run unit tests for each service and integration test for the 
entire API

### Details about docker images
The docker-compose file, which is used indirectly through the Makefile, creates 4 
images/services:
  1. The API based on FAST API
  1. PostgreSQL database for development
  1. PostgreSQL database for integration testing
  1. PgAdmin as PostgreSQL database administrator

The project has 2 database because. One of them is used to run the integration tests 
and it is cleaned after each test process. In that way, the test guarantee that start 
always with the same conditions.

The other one is used to develop the app and do some manual trials. This database
use a docker volume in order to be able to persist the data.

Finally, it is possible to enter to the database administrator by accessing to 
**http://127.0.0.1:5050** with credentials:
  * user: admin@example.com
  * password: password

Yes, I know, security first!

### Other details...
The project used poetry as a tool to install and manage python dependencies. Poetry 
bases on **pyproject.toml** file to obtain dependencies. This file also allows 
to configure other tools like:
  * Black
  * Flakehell
  * and others...

The project uses black and flakehell (with some extensions) as pre-commit hooks. In order to run 
this hooks it is necessary to install the python dependencies locally inside a virtual env. 
All the dependencies and hooks can be installed and configured easily by running 
(assuming you have python >= 3.7 already installed):

```bash
make start_project
```

## Next Steps
