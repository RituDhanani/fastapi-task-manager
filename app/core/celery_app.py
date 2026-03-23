from celery import Celery

celery = Celery(
    "task_manager",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

celery.conf.update(
    imports=["app.tasks.task_logs"]
)