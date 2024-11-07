import time
from celery import Celery

# Configure Celery to use Redis as the message broker and backend
celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

def process_document(document_data):
    # Simulate a 5-minute processing delay
    time.sleep(300)  # 300 seconds = 5 minutes

    # Mock result to return after delay
    result = {"status": "Processed", "data": document_data}
    return result

# Define a long-running task for document processing
@celery_app.task
def process_document_w_celery(document_data):
    # Simulate a long-running processing task (5 minutes)
    time.sleep(300) # 300 seconds = 5 minutes

    result = {"status": "Processed", "data": document_data}

    # Return a mock result after the delay
    return result