import pytest
from models import TaskResponse
from storage import TaskStore


class TestTaskStore:
    """Тесты хранилища TaskStore."""

    def setup_method(self):
        self.store = TaskStore()

    def test_create_task(self):
        task = self.store.create_task("Test", "Desc", 3)
        assert task.id == 1
        assert task.title == "Test"
        assert task.description == "Desc"
        assert task.priority == 3
        assert task.completed is False

    def test_create_task_defaults(self):
        task = self.store.create_task("Test")
        assert task.id == 1
        assert task.description == ""
        assert task.priority == 1

    def test_create_multiple_tasks(self):
        t1 = self.store.create_task("Task 1")
        t2 = self.store.create_task("Task 2")
        assert t1.id == 1
        assert t2.id == 2

    def test_get_task(self):
        self.store.create_task("Test")
        task = self.store.get_task(1)
        assert task.title == "Test"

    def test_get_task_not_found(self):
        with pytest.raises(KeyError):
            self.store.get_task(999)

    def test_get_nonexistent_id(self):
        with pytest.raises(KeyError):
            self.store.get_task(0)
