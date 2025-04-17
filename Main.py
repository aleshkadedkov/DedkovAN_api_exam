from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()

class Task(BaseModel):
    id: int
    title: str = Field(..., description="Название задачи")
    description: Optional[str] = Field(None, description="Описание задачи")
    status: str = Field(..., description="Статус задачи", example="в процессе")

tasks = []
task_id_counter = 1

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    """Получить список всех задач."""
    return tasks

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    """Создать новую задачу."""
    global task_id_counter
    task_dict = task.dict()
    task_dict['id'] = task_id_counter
    tasks.append(task_dict)
    task_id_counter += 1
    return task_dict

@app.put("/tasks/{id}", response_model=Task)
def update_task(id: int, task: Task):
    """Обновить существующую задачу."""
    for t in tasks:
        if t['id'] == id:
            t['title'] = task.title
            t['description'] = task.description
            t['status'] = task.status
            return t
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{id}")
def delete_task(id: int):
    """Удалить задачу по ID."""
    global tasks
    tasks = [t for t in tasks if t['id'] != id]
    return {"detail": "Task deleted"}

# Запуск приложения
# uvicorn main:app --reload