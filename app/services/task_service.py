from sqlalchemy.orm import Session
from app.models.task import Task

def create_task(db: Session, title: str, description: str, user_id: int):
    task = Task(
        title=title,
        description=description,
        user_id=user_id
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_tasks(db: Session, user_id: int):
    return db.query(Task).filter(Task.user_id == user_id).all()


def update_task(db: Session, task_id: int, title: str, description: str, user_id: int):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

    if not task:
        return None

    task.title = title
    task.description = description
    db.commit()
    return task


def delete_task(db: Session, task_id: int, user_id: int):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

    if not task:
        return None

    db.delete(task)
    db.commit()
    return task