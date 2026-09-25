# test_claude_connect

A test repo for writing code from the Claude desktop app and pushing it from Git Bash.

## Run the app

```bash
python server.py
```

Then open http://127.0.0.1:8000 in your browser. Press Ctrl+C in the terminal to stop the server.

## Run the script on its own

```bash
python hello.py
```

## Files

- `hello.py` – builds the greeting (used by the server and runnable on its own)
- `server.py` – backend: serves the UI and the `/api/hello` endpoint
- `static/` – front-end: `index.html`, `style.css`, `app.js`
