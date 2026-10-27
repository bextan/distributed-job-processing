import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.celery_app import celery_app


@pytest.fixture(autouse=True)
def enable_celery_eager_mode():
    """Configure Celery to run tasks synchronously in-memory for testing."""
    celery_app.conf.update(
        task_always_eager=True,
        task_eager_propagates=True,
        task_store_eager_result=True,  # Сохраняет статус/результат синхронных задач
        result_backend="cache+memory://",  # Локальное хранилище в памяти для тестов
    )
    yield


@pytest.fixture
def client():
    """FastAPI TestClient fixture."""
    with TestClient(app) as test_client:
        yield test_client