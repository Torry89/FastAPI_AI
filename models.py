from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """Модель для создания задачи."""

    title: str = Field(
        ..., 
        min_length=3, 
        max_length=100, 
        description="Заголовок задачи (обязательный, от 3 до 100 символов)"
    )
    description: str = Field(
        "", 
        description="Описание задачи (необязательное)"
    )
    priority: int = Field(
        1, 
        ge=1, 
        le=5, 
        description="Приоритет задачи (от 1 до 5)"
    )


class TaskResponse(BaseModel):
    """Модель ответа с данными задачи."""

    id: int = Field(..., description="Уникальный идентификатор задачи")
    title: str = Field(..., description="Заголовок задачи")
    description: str = Field("", description="Описание задачи")
    priority: int = Field(1, ge=1, le=5, description="Приоритет задачи (от 1 до 5)")
    completed: bool = Field(False, description="Статус выполнения задачи")
