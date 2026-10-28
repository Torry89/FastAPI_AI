from fastapi import FastAPI, HTTPException
from models import TaskCreate, TaskResponse
from storage import TaskStore

app = FastAPI(
    title="Task Manager API",
    description="REST API для управления задачами",
    version="1.0.0",
)

store = TaskStore()


@app.post(
    "/task",
    status_code=201,
    response_model=TaskResponse,
    summary="Создать задачу",
    description="Создает новую задачу с указанным заголовком, описанием и приоритетом.",
    responses={
        422: {"description": "Ошибка валидации входных данных"},
    },
)
def create_task(task_data: TaskCreate):
    """
    Создает новую задачу.

    - **title**: заголовок задачи (обязательный, от 3 до 100 символов)
    - **description**: описание задачи (необязательное)
    - **priority**: приоритет от 1 до 5 (по умолчанию 1)
    """
    task = store.create_task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
    )
    return task


@app.get(
    "/task/{task_id}",
    status_code=200,
    response_model=TaskResponse,
    summary="Получить задачу",
    description="Возвращает задачу по её уникальному идентификатору.",
    responses={
        404: {"description": "Задача не найдена"},
    },
)
def get_task(task_id: int):
    """
    Получает задачу по идентификатору.

    - **task_id**: уникальный идентификатор задачи
    """
    try:
        return store.get_task(task_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Task not found")
