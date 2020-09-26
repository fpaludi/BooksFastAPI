#!/bin/bash
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}Installing virtualenv and poetry${NC}"
pip3 install virtualenv poetry &> /dev/null

echo -e "${GREEN}Creating and activiting virtualenv ${NC}"
virtualenv .venv --python $which python3.7
source .venv/bin/activate

echo -e "${GREEN}Configuring poetry${NC}"
poetry config virtualenvs.create false

echo -e "${GREEN}Installing project dependencies${NC}"
poetry install
