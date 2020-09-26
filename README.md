# Book App
It is mini WebApp for book reviews which use FastAPI as framework

# Running the project
In order to get the project working you need to run

```bash
sudo apt install python3.7
source scripts/start_project.sh
```

# Running APP
uvicorn main:app --reload

# Running Tests
pytest -v -s --cov src/ --cov-report html --cov-report term

