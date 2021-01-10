GREEN=\033[0;32m
NC=\033[0m
PYTHON_PATH=$(shell which python3.7)

BASE_COMPOSE_FILE=docker/docker-compose.yml
PROD_COMPOSE_FILE=docker/docker-compose.prod.yml
DEV_COMPOSE_FILE=docker/docker-compose.dev.yml

export NETWORK_NAME=booksapi
NETWORKS=$(shell docker network ls --filter name=^${NETWORK_NAME} --format="{{ .Name }}")

BASE_COMPOSE_CMD=docker-compose -f $(CURDIR)/$(BASE_COMPOSE_FILE)
PROD_COMPOSE_CMD=$(BASE_COMPOSE_CMD) -f $(CURDIR)/$(PROD_COMPOSE_FILE)
DEV_COMPOSE_CMD=$(BASE_COMPOSE_CMD) -f $(CURDIR)/$(DEV_COMPOSE_FILE)

create_network:
	@if [ -z $(NETWORKS) ]; then \
		echo '${GREEN}Creating network '$(NETWORK_NAME)'${NC}'; \
		docker network create $(NETWORK_NAME); \
	else \
		echo '${GREEN} Network '$(NETWORK_NAME)' already exists${NC}'; \
	fi;

build: create_network
	$(PROD_COMPOSE_CMD) build

stop:
	$(PROD_COMPOSE_CMD) down --remove-orphans

run:
	$(PROD_COMPOSE_CMD) up -d

build_dev: create_network
	$(DEV_COMPOSE_CMD) build

up_dev:
	$(DEV_COMPOSE_CMD) up -d

run_dev: up_dev
	$(DEV_COMPOSE_CMD) exec api bash

run_tests: up_dev
	$(DEV_COMPOSE_CMD) exec api pytest tests/ -vv -s -x \
	--cov src/ \
	--cov-report html --cov-report term

run_tests_nohtml: up_dev
	$(DEV_COMPOSE_CMD) exec api pytest tests/ -vv -s -x \
	--cov src/ \
	--cov-report term

stop_dev:
	$(DEV_COMPOSE_CMD) down --remove-orphans

start_project:
	@echo '${GREEN}Installing, creating and activiting virtualenv...${NC}';
	@pip3 install virtualenv > /dev/null;
	@python3 -m virtualenv .venv --python $(PYTHON_PATH) > /dev/null;
	$(shell source .venv/bin/activate)

	@echo '${GREEN}Installing and configuring poetry...${NC}';
	@pip3 install poetry > /dev/null;
	@poetry config virtualenvs.create true;
	@poetry config virtualenvs.in-project false;

	@echo '${GREEN}Installing project dependencies...${NC}';
	@poetry install -vv;

	@echo '${GREEN}Configuring pre-commit hooks...${NC}';
	@pre-commit install;
