FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

## Install Poetry
COPY pyproject.toml /app/
RUN cd /app/
RUN python -m pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install -vv

## Adding necessary scripts
COPY scripts/prestart.sh /app/

## Update Workdir. A volumen is mounted there by compose file
WORKDIR /app/app/

## Create app
# App is munting by using a docker volume for 
# development/testing purpose
