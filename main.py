from celery.result import AsyncResult
from fastapi import FastAPI

from celery_app import celery_app, process_document, process_document_w_celery

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/submit-document/")
async def submit_document(document_data: dict):
    """
    Submit a document for processing and return the task ID without Celery (synchronous).
    """
    # Enqueue the task and get the task ID
    task = process_document(document_data)
    # return {"task_id": task.id}
    return {"task_id": task}

@app.post("/submit-document-w-celery/")
async def submit_document_w_celery(document_data: dict):
    """
    Submit a document for processing and return the task ID with Celery (asynchronous).
    Enqueues the document processing task.
    """
    # Enqueue the task and get the task ID
    task = process_document_w_celery.delay(document_data)
    return {"task_id": task.id}

@app.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    """
    Get the status of a task by task ID.
    Checks the status of the task.
    """
    # Check the status of the task
    task_result = AsyncResult(task_id, app=celery_app)
    
    if task_result.state == "PENDING":
        # Task is in queue or waiting to start
        return {"status": "Processing", "task_id": task_id}
    elif task_result.state == "SUCCESS":
        # Task completed successfully
        return {"status": "Completed", "result": task_result.result}
    elif task_result.state == "FAILURE":
        # Task failed
        return {"status": "Failed", "error": str(task_result.info)}
    else:
        return {"status": task_result.state, "task_id": task_id}