from typing import Any, Dict, Optional
from enum import Enum
from pydantic import BaseModel, Field


class JobType(str, Enum):
    DATA_PROCESSING = "data_processing"
    REPORT_GENERATION = "report_generation"
    NOTIFICATION = "notification"


class JobCreateRequest(BaseModel):
    job_type: JobType = Field(..., description="Type of job to execute")
    payload: Dict[str, Any] = Field(default_factory=dict, description="Job parameters/payload")


class JobResponse(BaseModel):
    job_id: str
    status: str
    message: str


class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    result: Optional[Any] = None
    error: Optional[str] = None


class HealthCheckResponse(BaseModel):
    status: str
    rabbitmq_connected: bool
    version: str
