from fastapi import APIRouter, HTTPException, status
from celery.result import AsyncResult

from app.models.schemas import (
    JobCreateRequest,
    JobResponse,
    JobStatusResponse,
    JobType
)
from app.workers.tasks import (
    process_data_task,
    generate_report_task,
    send_notification_task
)
from app.core.celery_app import celery_app

router = APIRouter()


@router.post("/jobs", response_model=JobResponse, status_code=status.HTTP_202_ACCEPTED)
def submit_job(request: JobCreateRequest):
    """
    Submits a new asynchronous job to RabbitMQ queue.
    """
    if request.job_type == JobType.DATA_PROCESSING:
        task = process_data_task.delay(request.payload)
    elif request.job_type == JobType.REPORT_GENERATION:
        task = generate_report_task.delay(request.payload)
    elif request.job_type == JobType.NOTIFICATION:
        task = send_notification_task.delay(request.payload)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported job type: {request.job_type}"
        )

    return JobResponse(
        job_id=task.id,
        status="QUEUED",
        message=f"Job of type '{request.job_type.value}' successfully submitted to RabbitMQ queue."
    )


@router.get("/jobs/{job_id}", response_model=JobStatusResponse)
def get_job_status(job_id: str):
    """
    Retrieves the status and result of a job by ID from RPC backend/Celery.
    """
    async_result = AsyncResult(job_id, app=celery_app)
    
    status_str = async_result.status
    result = None
    error_msg = None

    if async_result.successful():
        result = async_result.result
    elif async_result.failed():
        error_msg = str(async_result.result)

    return JobStatusResponse(
        job_id=job_id,
        status=status_str,
        result=result,
        error=error_msg
    )


@router.delete("/jobs/{job_id}", status_code=status.HTTP_200_OK)
def cancel_job(job_id: str):
    """
    Revokes/cancels an in-flight or pending job.
    """
    async_result = AsyncResult(job_id, app=celery_app)
    async_result.revoke(terminate=True)
    return {"job_id": job_id, "message": "Job cancellation request submitted."}
