def add(client, title):
    return client.post("/api/todos", json={"title": title}).json()

def test_list_starts_empty(client):
    response = client.get("/api/todos")
    assert response.status_code == 200
    assert response.json() == []

def test_create_todo(client):
    response = client.post("/api/todos", json={"title": "Buy milk"})
    assert response.status_code == 201
    assert response.json() == {"id": 1, "title": "Buy milk", "done": False}

def test_create_strips_whitespace(client):
    assert add(client, "  Buy milk  ")["title"] == "Buy milk"

def test_create_rejects_blank_title(client):
    response = client.post("/api/todos", json={"title": "   "})
    assert response.status_code == 422

def test_create_rejects_long_title(client):
    response = client.post("/api/todos", json={"title": "x" * 201})
    assert response.status_code == 422

def test_mark_done(client):
    todo = add(client, "Buy milk")
    response = client.patch(f"/api/todos/{todo['id']}", json={"done": True})
    assert response.status_code == 200
    assert response.json()["done"] is True

def test_rename(client):
    todo = add(client, "Buy milk")
    response = client.patch(f"/api/todos/{todo['id']}", json={"title": "Buy oat milk"})
    assert response.json()["title"] == "Buy oat milk"
    assert response.json()["done"] is False

def test_done_todos_listed_last(client):
    first = add(client, "First")
    add(client, "Second")
    client.patch(f"/api/todos/{first['id']}", json={"done": True})
    titles = [todo["title"] for todo in client.get("/api/todos").json()]
    assert titles == ["Second", "First"]

def test_delete(client):
    todo = add(client, "Buy milk")
    response = client.delete(f"/api/todos/{todo['id']}")
    assert response.status_code == 204
    assert client.get("/api/todos").json() == []

def test_missing_todo_returns_404(client):
    assert client.patch("/api/todos/99", json={"done": True}).status_code == 404
    assert client.delete("/api/todos/99").status_code == 404
