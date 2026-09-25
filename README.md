# test_claude_connect

A simple to-do app: a FastAPI backend with a SQLite database, and a plain HTML/JavaScript front end.

## Setup (once)

Create a virtual environment and install the packages into it:

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements-dev.txt
```

In a new terminal, run `source .venv/Scripts/activate` again before the commands below.

## Run the app

```bash
uvicorn main:app --reload
```

Open http://127.0.0.1:8000 in your browser. `--reload` restarts the server when you save a file. Press Ctrl+C to stop it.

Interactive API docs are at http://127.0.0.1:8000/docs.

## Run the tests

```bash
pytest
```

## Files

- `main.py` – the API: list, add, update and delete to-dos under `/api/todos`
- `database.py` – opens the SQLite database (`todos.db`, created on first run)
- `static/` – front end: `index.html`, `style.css`, `app.js`
- `tests/` – automated tests for the API
- `requirements.txt` – packages the app needs; `requirements-dev.txt` adds the testing tools
