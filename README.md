# Book App
It is mini WebApp for book reviews.

# Running the project
In order to get the project working you need to run

```bash
sudo source create_project.sh
```

# Create Virtual Env
poetry install  
poetry update

# Running APP
uvicorn main:app --reload



# Running Tests
pytest -v -s --cov src/ --cov-report html --cov-report term

