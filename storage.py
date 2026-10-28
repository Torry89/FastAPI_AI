from models import TaskResponse


class TaskStore:
    def __init__(self):
        self._tasks: dict[int, TaskResponse] = {}
        self._next_id: int = 1

    def create_task(self, title: str, description: str = "", priority: int = 1) -> TaskResponse:
        task = TaskResponse(
            id=self._next_id,
            title=title,
            description=description,
            priority=priority,
        )
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def get_task(self, task_id: int) -> TaskResponse:
        if task_id not in self._tasks:
            raise KeyError(task_id)
        return self._tasks[task_id]
