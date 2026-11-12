import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from app.database import Base


class DevOpsTask(Base):
    __tablename__ = "devops_tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="pending", index=True)  # pending, in_progress, completed, failed
    priority = Column(String(50), default="medium")  # low, medium, high, critical
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class DeploymentLog(Base):
    __tablename__ = "deployment_logs"

    id = Column(Integer, primary_key=True, index=True)
    environment = Column(String(50), default="production", index=True)
    version = Column(String(50), default="1.0.0")
    commit_sha = Column(String(64), nullable=True)
    status = Column(String(50), default="success")  # success, in_progress, failed
    deployed_by = Column(String(100), default="AI-DevOps-Agent")
    summary = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
