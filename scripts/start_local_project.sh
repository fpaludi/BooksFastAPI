#!/bin/bash
GREEN='\033[0;32m'
NC='\033[0m'

echo -e '${GREEN}Installing, creating and activiting virtualenv...${NC}';
pip3 install --user virtualenv;
python3 -m virtualenv .venv --python $(PYTHON_PATH);
source .venv/bin/activate

echo -e '${GREEN}Installing and configuring poetry...${NC}';
pip3 install poetry &> /dev/null;
poetry config virtualenvs.create true;
poetry config virtualenvs.in-project true;

echo -e '${GREEN}Installing project dependencies...${NC}';
poetry install -vv;

echo -e '${GREEN}Configuring pre-commit hooks...${NC}';
pre-commit install;
