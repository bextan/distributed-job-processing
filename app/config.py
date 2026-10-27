from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Distributed Job Processing Platform (RabbitMQ)"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api/v1"
    
    # RabbitMQ Broker & RPC Result Backend
    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "guest"
    RABBITMQ_PASSWORD: str = "guest"
    RABBITMQ_VHOST: str = "/"
    
    CELERY_BROKER_URL: str = "amqp://guest:guest@localhost:5672//"
    CELERY_RESULT_BACKEND: str = "rpc://"
    
    # Task execution limits
    TASK_TIME_LIMIT: int = 300  # 5 minutes
    TASK_SOFT_TIME_LIMIT: int = 270

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
