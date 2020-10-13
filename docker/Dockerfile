FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
WORKDIR /app/

# Install Poetry
COPY pyproject.toml /app/
RUN python -m pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN  poetry install

# Create app
# App is munting by using a docker volume for 
# development/testing purpose
