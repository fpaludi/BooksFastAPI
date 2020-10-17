build:
	docker-compose build

up:
	docker-compose up -d

run_tests: up
	docker-compose exec api pytest tests/ -vv -s -x \
	--cov src/ \
	--cov-report html --cov-report term

run_api: up
	docker-compose exec api /start-reload.sh

down:
	docker-compose down --remove-orphans

all_tests: down build run_tests
all_run: down build run_api
