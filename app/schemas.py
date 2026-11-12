import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None


class TaskResponse(TaskBase):
    id: int
    status: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class DeploymentLogCreate(BaseModel):
    environment: str = "production"
    version: str = "1.0.0"
    commit_sha: Optional[str] = None
    status: str = "success"
    deployed_by: str = "AI-DevOps-Agent"
    summary: Optional[str] = None


class DeploymentLogResponse(DeploymentLogCreate):
    id: int
    timestamp: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
    environment: str
    database_connected: bool
    timestamp: datetime.datetime
