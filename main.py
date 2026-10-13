"""Simple Notes API - a container-friendly FastAPI application."""

import logging
import os
from datetime import datetime, timezone
from threading import Lock

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# --- Configuration (all via environment variables, Docker-friendly) ---
APP_NAME = os.getenv("APP_NAME", "Notes API")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("notes-api")

app = FastAPI(title=APP_NAME, version="1.0.0")


# --- Models ---
class NoteIn(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = ""


class Note(NoteIn):
    id: int
    created_at: datetime


# --- In-memory storage ---
_notes: dict[int, Note] = {}
_next_id = 1
_lock = Lock()


# --- Routes ---
@app.get("/")
def root():
    return {"app": APP_NAME, "docs": "/docs", "health": "/health"}


@app.get("/health")
def health():
    """Use this for Docker HEALTHCHECK."""
    return {"status": "ok"}


@app.get("/notes", response_model=list[Note])
def list_notes():
    return list(_notes.values())


@app.post("/notes", response_model=Note, status_code=201)
def create_note(note: NoteIn):
    global _next_id
    with _lock:
        new = Note(id=_next_id, created_at=datetime.now(timezone.utc), **note.model_dump())
        _notes[_next_id] = new
        _next_id += 1
    logger.info("Created note %s", new.id)
    return new


@app.get("/notes/{note_id}", response_model=Note)
def get_note(note_id: int):
    if note_id not in _notes:
        raise HTTPException(status_code=404, detail="Note not found")
    return _notes[note_id]


@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int):
    with _lock:
        if _notes.pop(note_id, None) is None:
            raise HTTPException(status_code=404, detail="Note not found")
    logger.info("Deleted note %s", note_id)
