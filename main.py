import time
import redis.asyncio as redis
from fastapi import BackgroundTasks, FastAPI, Request, HTTPException

from celery_app import process_document, celery_app

app = FastAPI()
redis = redis.from_url("redis://localhost")

# Rate limit configuration
RATE_LIMIT = 5  # requests
TIME_WINDOW = 60  # seconds

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
#     return response

@app.post("/process-doc/")
async def process_doc(doc_id: str, background_tasks: BackgroundTasks):
    # Enqueue task
    task = process_document.delay(doc_id) # This is the Celery task
    
    # Optionally, return a task ID or status immediately to user
    return {"status": "Processing started", "task_id": task.id}

@app.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    from celery.result import AsyncResult
    try:
        result = AsyncResult(task_id, app=celery_app)
    except HTTPException as e:
        print(">>> e:", e)
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    return {"task_id": task_id, "status": result.status, "result": result.result}
