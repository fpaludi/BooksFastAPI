#!/bin/bash
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}Installing, creating and activiting virtualenv...${NC}"
pip3 install virtualenv &> /dev/null
virtualenv .venv --python $which python3.7
source .venv/bin/activate

echo -e "${GREEN}Installing and configuring poetry...${NC}"
pip3 install poetry &> /dev/null
poetry config virtualenvs.create false
poetry config virtualenvs.in-project true

echo -e "${GREEN}Installing project dependencies...${NC}"
poetry install

echo -e "${GREEN}Configuring pre-commit hooks...${NC}"
pre-commit install
