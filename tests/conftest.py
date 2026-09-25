import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).parent.parent))

import database
from main import app, get_db

@pytest.fixture
def client(tmp_path):
    db_path = tmp_path / "test.db"

    def get_test_db():
        conn = database.connect(db_path)
        try:
            yield conn
        finally:
            conn.close()

    app.dependency_overrides[get_db] = get_test_db
    yield TestClient(app)
    app.dependency_overrides.clear()
