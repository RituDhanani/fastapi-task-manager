from app.core.celery_app import celery
import logging

logger = logging.getLogger(__name__)

@celery.task(name="app.tasks.task_logs.create_activity_log")
def create_activity_log(action: str, task_title: str, user_name: str):
    
    if action == "created":
        message = f"[ActivityLog Created] Task '{task_title}' created by {user_name}"
    elif action == "updated":
        message = f"[ActivityLog Updated] Task '{task_title}' updated by {user_name}"
    elif action == "deleted":
        message = f"[ActivityLog Deleted] Task '{task_title}' deleted by {user_name}"
    else:
        message = f"[ActivityLog] Unknown action"

    logger.warning(message)