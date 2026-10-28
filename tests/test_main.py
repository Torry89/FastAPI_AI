import pytest
from fastapi.testclient import TestClient
from main import app, store


@pytest.fixture(autouse=True)
def _clear_store():
    """Очищает хранилище между тестами."""
    store._tasks.clear()
    store._next_id = 1


@pytest.fixture
def client():
    return TestClient(app)


class TestCreateTask:
    """Тесты POST /task."""

    def test_create_task_success(self, client):
        resp = client.post(
            "/task",
            json={"title": "Test task", "description": "Desc", "priority": 3},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["id"] == 1
        assert data["title"] == "Test task"
        assert data["description"] == "Desc"
        assert data["priority"] == 3
        assert data["completed"] is False

    def test_create_task_defaults(self, client):
        resp = client.post("/task", json={"title": "Test"})
        assert resp.status_code == 201
        data = resp.json()
        assert data["description"] == ""
        assert data["priority"] == 1

    def test_create_task_title_too_short(self, client):
        resp = client.post("/task", json={"title": "ab"})
        assert resp.status_code == 422

    def test_create_task_title_too_long(self, client):
        resp = client.post("/task", json={"title": "a" * 101})
        assert resp.status_code == 422

    def test_create_task_priority_too_low(self, client):
        resp = client.post("/task", json={"title": "Test", "priority": 0})
        assert resp.status_code == 422

    def test_create_task_priority_too_high(self, client):
        resp = client.post("/task", json={"title": "Test", "priority": 6})
        assert resp.status_code == 422


class TestGetTask:
    """Тесты GET /task/{task_id}."""

    def test_get_task_success(self, client):
        client.post("/task", json={"title": "Get test"})
        resp = client.get("/task/1")
        assert resp.status_code == 200
        assert resp.json()["title"] == "Get test"

    def test_get_task_not_found(self, client):
        resp = client.get("/task/999")
        assert resp.status_code == 404
        assert resp.json()["detail"] == "Task not found"
