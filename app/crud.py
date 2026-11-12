from sqlalchemy.orm import Session
from app import models, schemas


def get_task(db: Session, task_id: int):
    return db.query(models.DevOpsTask).filter(models.DevOpsTask.id == task_id).first()


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DevOpsTask).order_by(models.DevOpsTask.created_at.desc()).offset(skip).limit(limit).all()


def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.DevOpsTask(
        title=task.title,
        description=task.description,
        priority=task.priority,
        status="pending"
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate):
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    update_data = task_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if not db_task:
        return False
    db.delete(db_task)
    db.commit()
    return True


def log_deployment(db: Session, log: schemas.DeploymentLogCreate):
    db_log = models.DeploymentLog(
        environment=log.environment,
        version=log.version,
        commit_sha=log.commit_sha,
        status=log.status,
        deployed_by=log.deployed_by,
        summary=log.summary
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


def get_deployment_logs(db: Session, limit: int = 10):
    return db.query(models.DeploymentLog).order_by(models.DeploymentLog.timestamp.desc()).limit(limit).all()
