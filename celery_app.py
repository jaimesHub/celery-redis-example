from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

HALF_MINUTE = 30
ONE_MINUTE = 60
TWO_MINUTES = 120
THREE_MINUTES = 180

@celery_app.task
def process_document(doc_id: str):
    # Simulate a long-running AI service
    # Here we would have the AI Service call and processing logic
    import time
    import random
    sleep_time = random.randint(HALF_MINUTE, THREE_MINUTES)
    time.sleep(sleep_time)
    return f"Processed document {doc_id} in {sleep_time} seconds"
