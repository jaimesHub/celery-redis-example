# app/tasks.py
from celery_config import celery_app

@celery_app.task
def process_document(doc_id: int):
    # Simulated long-running AI service task
    import time
    time.sleep(180)  # Simulate a delay
    return f"Document {doc_id} processed"
