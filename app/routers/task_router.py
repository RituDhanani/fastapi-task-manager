from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.task import Task
from app.schemas.task_schema import TaskCreate
from app.services.task_service import create_task, get_tasks, update_task, delete_task
from app.services.deps import get_current_user
from app.models.user import User
from app.tasks.task_logs import create_activity_log

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/create")
def create(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_task = create_task(db, task.title, task.description, current_user.id)

    create_activity_log.delay(
        "created",
        new_task.title,
        current_user.name
    )

    return new_task


@router.get("/list")
def read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "admin":
        return db.query(Task).all()  

    return db.query(Task).filter(Task.user_id == current_user.id).all()  


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

    create_activity_log.delay(
        "updated",
        task.title,
        current_user.name
    )

    return updated


@router.delete("/delete/{task_id}")
def delete(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can delete tasks")

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    create_activity_log.delay(
        "deleted",
        task.title,
        current_user.name
    )

    return {"message": "Task deleted"}