import time
import redis.asyncio as redis
from fastapi import BackgroundTasks, FastAPI, Request, HTTPException

from celery_app import process_document, celery_app

app = FastAPI()
redis = redis.from_url("redis://localhost")

# Rate limit configuration
# RATE_LIMIT = 5  # requests
# TIME_WINDOW = 60  # seconds

# async def is_rate_limited(ip: str) -> bool:
#     current_time = int(time.time())
#     key = f"rate-limit:{ip}"
    
#     # Increment the counter and set an expiry if it's a new key
#     count = await redis.incr(key)
#     if count == 1:
#         await redis.expire(key, TIME_WINDOW)
    
#     # Check if limit exceeded
#     if count > RATE_LIMIT:
#         return True
#     return False

# @app.middleware("http")
# async def rate_limit_middleware(request: Request, call_next):
#     ip = request.client.host
#     if await is_rate_limited(ip):
#         raise HTTPException(status_code=429, detail="Rate limit exceeded")
#     response = await call_next(request)
#     return 

# 1. Define a Pydantic model for the request body
from pydantic import BaseModel

class DocumentRequest(BaseModel):
    doc_id: str

# 2. Use the model in the endpoint

@app.post("/process-doc/")
async def process_doc(request: DocumentRequest, background_tasks: BackgroundTasks):
    if not request.doc_id:
        raise HTTPException(status_code=404, detail="Document ID not provided")
    
    # Enqueue task
    task = process_document.delay(request.doc_id) # This is the Celery task
    
    # Optionally, return a task ID or status immediately to user
    return {
        "status": "Processing started", 
        "task_id": task.id, 
        "message": f"This task will take {task} seconds to complete"
    }

@app.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    from celery.result import AsyncResult
    try:
        result = AsyncResult(task_id, app=celery_app)
    except HTTPException as e:
        print(">>> e:", e)
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    return {"task_id": task_id, "status": result.status, "result": result.result}
