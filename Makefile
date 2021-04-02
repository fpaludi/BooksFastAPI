# Just colors
RED=\033[0;31m
GREEN=\033[0;32m
NC=\033[0m

# Network name (default: booksapi)
NETWORK?=booksapi
export NETWORK_NAME=$(NETWORK)
NETWORKS=$(shell docker network ls --filter name=^${NETWORK_NAME} --format="{{ .Name }}")

# Compose Files
BASE_FILE=docker/docker-compose.yml
DEV_FILE=docker/docker-compose-dev.yml
PROD_FILE=docker/docker-compose.dev.yml
PROD_COMPOSE_CMD=docker-compose -f $(CURDIR)/$(BASE_FILE) -f $(CURDIR)/$(PROD_FILE)
DEV_COMPOSE_CMD=docker-compose -f $(CURDIR)/$(BASE_FILE) -f $(CURDIR)/$(DEV_FILE)


create_network:
	@if [ -z $(NETWORKS) ]; then \
		echo "${GREEN}Creating network '$(NETWORK_NAME)'${NC}"; \
		docker network create $(NETWORK_NAME); \
	fi;

create_tables:
	$(PROD_COMPOSE_CMD) exec api bash /app/prestart.sh

build: create_network
	$(PROD_COMPOSE_CMD) build

run:
	$(PROD_COMPOSE_CMD) up -d

build_dev: create_network
	$(DEV_COMPOSE_CMD) build --build-arg INSTALL_DEV=true

run_dev:
	$(DEV_COMPOSE_CMD) up -d

run_tests: run_dev
	$(DEV_COMPOSE_CMD) exec api pytest tests/ -vv -s \
	--cov src/ \
	--cov-report html --cov-report term

run_tests_ci: run_dev
	$(DEV_COMPOSE_CMD) exec -T api pytest tests/ -vv -s \
	--cov src/ \
	--cov-report=xml

run_api: run
	$(PROD_COMPOSE_CMD) exec api /start-reload.sh

stop:
	$(PROD_COMPOSE_CMD) down --remove-orphans

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
	@pre-commit install;	@echo '${GREEN}Configuring pre-commit hooks...${NC}';
	@pre-commit install;
