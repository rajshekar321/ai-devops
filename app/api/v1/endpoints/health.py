import datetime
from fastapi import APIRouter
from app.config import settings
from app.database import check_db_health
from app.schemas import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def get_health():
    """Service health and readiness check."""
    db_ok = check_db_health()
    status = "healthy" if db_ok else "degraded"
    return HealthResponse(
        status=status,
        app_name=settings.APP_NAME,
        version="1.0.0",
        environment=settings.APP_ENV,
        database_connected=db_ok,
        timestamp=datetime.datetime.utcnow()
    )


@router.get("/ping")
def ping():
    """Lightweight alive check for load balancers and container orchestrators."""
    return {"ping": "pong", "timestamp": datetime.datetime.utcnow().isoformat()}
