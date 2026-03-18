from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.task_schema import TaskCreate
from app.services.task_service import create_task, get_tasks, update_task, delete_task
from app.services.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/create")
def create(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_task(db, task.title, task.description, current_user.id)


@router.get("/list")
def read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_tasks(db, current_user.id)


@router.put("/update/{task_id}")
def update(
    task_id: int,
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated = update_task(
        db,
        task_id,
        task.title,
        task.description,
        current_user.id
    )

    if not updated:
        raise HTTPException(status_code=404, detail="Task not found or not authorized")

    return updated


@router.delete("/delete/{task_id}")
def delete(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    deleted = delete_task(db, task_id, current_user.id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found or not authorized")

    return {"message": "Task deleted"}