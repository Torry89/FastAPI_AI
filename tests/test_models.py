import pytest
from pydantic import ValidationError
from models import TaskCreate, TaskResponse


class TestTaskCreate:
    """Тесты модели TaskCreate."""

    def test_valid_task_create(self):
        task = TaskCreate(title="Test task")
        assert task.title == "Test task"
        assert task.description == ""
        assert task.priority == 1

    def test_valid_task_create_with_all_fields(self):
        task = TaskCreate(title="Test", description="Desc", priority=3)
        assert task.title == "Test"
        assert task.description == "Desc"
        assert task.priority == 3

    @pytest.mark.parametrize("title", ["", "ab"])
    def test_title_too_short(self, title):
        with pytest.raises(ValidationError, match="string_too_short"):
            TaskCreate(title=title)

    @pytest.mark.parametrize(
        "title",
        ["a" * 101, "a" * 200],
    )
    def test_title_too_long(self, title):
        with pytest.raises(ValidationError, match="string_too_long"):
            TaskCreate(title=title)

    @pytest.mark.parametrize("priority", [0, -1, -100])
    def test_priority_too_low(self, priority):
        with pytest.raises(ValidationError, match="greater_than_equal"):
            TaskCreate(title="Test", priority=priority)

    @pytest.mark.parametrize("priority", [6, 10, 100])
    def test_priority_too_high(self, priority):
        with pytest.raises(ValidationError, match="less_than_equal"):
            TaskCreate(title="Test", priority=priority)


class TestTaskResponse:
    """Тесты модели TaskResponse."""

    def test_valid_task_response(self):
        task = TaskResponse(
            id=1, title="Test", description="Desc", priority=3, completed=True
        )
        assert task.id == 1
        assert task.completed is True

    def test_task_response_defaults(self):
        task = TaskResponse(id=1, title="Test")
        assert task.description == ""
        assert task.priority == 1
        assert task.completed is False

    @pytest.mark.parametrize("priority", [0, -1, 6, 10])
    def test_task_response_invalid_priority(self, priority):
        with pytest.raises(ValidationError, match="priority"):
            TaskResponse(id=1, title="Test", priority=priority)
