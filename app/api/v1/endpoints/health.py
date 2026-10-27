from fastapi import APIRouter
import kombu
from app.config import settings
from app.models.schemas import HealthCheckResponse

router = APIRouter()


@router.get("/health", response_model=HealthCheckResponse)
def health_check():
    rabbitmq_connected = False
    try:
        conn = kombu.Connection(settings.CELERY_BROKER_URL)
        conn.connect()
        rabbitmq_connected = conn.connected
        conn.close()
    except Exception:
        rabbitmq_connected = False

    return HealthCheckResponse(
        status="healthy" if rabbitmq_connected else "degraded",
        rabbitmq_connected=rabbitmq_connected,
        version=settings.VERSION
    )
