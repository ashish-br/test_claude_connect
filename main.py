from datetime import datetime, timezone
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field

import database

STATIC_DIR = Path(__file__).parent / "static"

app = FastAPI(title="To-do API")

def get_db():
    conn = database.connect()
    try:
        yield conn
    finally:
        conn.close()

class TodoCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    title: str = Field(min_length=1, max_length=200)

class TodoUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    title: str | None = Field(default=None, min_length=1, max_length=200)
    done: bool | None = None

class Todo(BaseModel):
    id: int
    title: str
    done: bool
    created_at: datetime

def to_todo(row):
    # SQLite stores CURRENT_TIMESTAMP in UTC without a timezone, so mark it as UTC
    created_at = datetime.fromisoformat(row["created_at"]).replace(tzinfo=timezone.utc)
    return Todo(id=row["id"], title=row["title"], done=bool(row["done"]), created_at=created_at)

def find_todo(db, todo_id):
    row = db.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return row

@app.get("/api/todos")
def list_todos(db=Depends(get_db)) -> list[Todo]:
    rows = db.execute("SELECT * FROM todos ORDER BY done, id").fetchall()
    return [to_todo(row) for row in rows]

@app.post("/api/todos", status_code=201)
def create_todo(todo: TodoCreate, db=Depends(get_db)) -> Todo:
    cursor = db.execute("INSERT INTO todos (title) VALUES (?)", (todo.title,))
    db.commit()
    return to_todo(find_todo(db, cursor.lastrowid))

@app.patch("/api/todos/{todo_id}")
def update_todo(todo_id: int, changes: TodoUpdate, db=Depends(get_db)) -> Todo:
    find_todo(db, todo_id)
    if changes.title is not None:
        db.execute("UPDATE todos SET title = ? WHERE id = ?", (changes.title, todo_id))
    if changes.done is not None:
        db.execute("UPDATE todos SET done = ? WHERE id = ?", (int(changes.done), todo_id))
    db.commit()
    return to_todo(find_todo(db, todo_id))

@app.delete("/api/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, db=Depends(get_db)):
    find_todo(db, todo_id)
    db.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    db.commit()
    return Response(status_code=204)

# Serve the front end last so the /api routes take priority
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
