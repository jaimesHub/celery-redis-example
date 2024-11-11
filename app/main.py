# app/main.py
from fastapi import FastAPI
from celery.result import AsyncResult
from tasks import process_document

app = FastAPI()

@app.post("/process/")
async def process_request(doc_id: int):
    task = process_document.delay(doc_id)
    return {"task_id": task.id}

@app.get("/status/{task_id}")
async def check_status(task_id: str):
    result = AsyncResult(task_id)
    if result.ready():
        return {"status": "completed", "result": result.result}
    return {"status": "processing"}
