from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task
def process_document(doc_id: str):
    # Simulate a long-running AI service
    # Here we would have the AI Service call and processing logic
    import time
    time.sleep(120)  # Simulating a 2-minute process
    return f"Processed document {doc_id}"
