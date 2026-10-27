import time
import random
from app.core.celery_app import celery_app
from app.core.logging import logger


@celery_app.task(bind=True, name="tasks.process_data", max_retries=3, default_retry_delay=5)
def process_data_task(self, payload: dict) -> dict:
    logger.info(f"Task {self.request.id}: Starting data processing with payload: {payload}")
    records = payload.get("records", 100)
    
    # Simulate processing work
    time.sleep(2.0)
    
    processed_count = records * 2
    logger.info(f"Task {self.request.id}: Data processing complete. Processed {processed_count} records.")
    return {
        "status": "COMPLETED",
        "processed_records": processed_count,
        "input_payload": payload
    }


@celery_app.task(bind=True, name="tasks.generate_report", max_retries=3, default_retry_delay=5)
def generate_report_task(self, payload: dict) -> dict:
    logger.info(f"Task {self.request.id}: Starting report generation...")
    report_title = payload.get("title", "Standard Analytics Summary")
    
    time.sleep(3.0)
    
    logger.info(f"Task {self.request.id}: Report '{report_title}' generated.")
    return {
        "status": "COMPLETED",
        "report_title": report_title,
        "download_url": f"/reports/{self.request.id}.pdf",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }


@celery_app.task(bind=True, name="tasks.send_notification", max_retries=3, default_retry_delay=5)
def send_notification_task(self, payload: dict) -> dict:
    logger.info(f"Task {self.request.id}: Sending notification...")
    recipient = payload.get("recipient", "user@example.com")
    
    time.sleep(1.0)
    
    logger.info(f"Task {self.request.id}: Notification sent to {recipient}.")
    return {
        "status": "SENT",
        "recipient": recipient,
        "timestamp": time.time()
    }
