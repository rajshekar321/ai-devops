from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, crud

router = APIRouter()


@router.get("/tasks", response_model=list[schemas.TaskResponse])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieve list of DevOps tasks."""
    return crud.get_tasks(db, skip=skip, limit=limit)


@router.post("/tasks", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """Create a new DevOps task."""
    return crud.create_task(db, task)


@router.get("/tasks/{task_id}", response_model=schemas.TaskResponse)
def read_task(task_id: int, db: Session = Depends(get_db)):
    """Retrieve a single task by ID."""
    db_task = crud.get_task(db, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)):
    """Update task status, priority or details."""
    db_task = crud.update_task(db, task_id, task_update)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task."""
    success = crud.delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return None


@router.get("/deployments", response_model=list[schemas.DeploymentLogResponse])
def get_deployments(limit: int = 10, db: Session = Depends(get_db)):
    """Retrieve recent deployment event logs."""
    return crud.get_deployment_logs(db, limit=limit)


@router.post("/deployments", response_model=schemas.DeploymentLogResponse, status_code=status.HTTP_201_CREATED)
def log_deployment(log: schemas.DeploymentLogCreate, db: Session = Depends(get_db)):
    """Record a deployment event."""
    return crud.log_deployment(db, log)
