# Notes API

A small FastAPI app, ready to containerize. No Dockerfile included — write your own.

## Project layout

```
notes-api/
├── app/
│   ├── __init__.py
│   └── main.py          # the application
├── requirements.txt
├── .dockerignore
└── README.md
```

## What your Dockerfile needs to know

| Item | Value |
|---|---|
| Python version | 3.10+ (3.12-slim recommended) |
| Install deps | `pip install --no-cache-dir -r requirements.txt` |
| Start command | `uvicorn app.main:app --host 0.0.0.0 --port 8000` |
| Port | `8000` |
| Health check URL | `GET /health` → `{"status":"ok"}` |
| Working dir | project root (the folder containing `app/`) |

Bind to `0.0.0.0`, not `127.0.0.1`, or the app won't be reachable from outside the container.

## Environment variables

| Variable | Default | Purpose |
|---|---|---|
| `APP_NAME` | `Notes API` | Name shown at `/` and in docs |
| `LOG_LEVEL` | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR` |

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/` | App info |
| GET | `/health` | Health check |
| GET | `/docs` | Interactive Swagger UI |
| GET | `/notes` | List notes |
| POST | `/notes` | Create note `{"title": "...", "content": "..."}` |
| GET | `/notes/{id}` | Get a note |
| DELETE | `/notes/{id}` | Delete a note |

Notes are stored in memory, so they reset when the container restarts.

## Run locally (without Docker)

```bash
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Quick test

```bash
curl -X POST localhost:8000/notes -H "Content-Type: application/json" \
     -d '{"title":"Hello","content":"From Docker"}'
curl localhost:8000/notes
```
