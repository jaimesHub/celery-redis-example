# SETUP IDEA USING Rate Limiting and Queueing

## Overview

```
Implement a queue system with rate limiting. 
Using a task queue (e.g., Celery or Redis Queue) offloads the AI task from FastAPI, improving the perceived response time. You can notify users when their request is completed, perhaps through WebSocket or a polling mechanism.

Using Redis for rate limiting and Celery with Redis as a task queue for handling background tasks
```

## 1. Rate Limiting with Redis

```
Using Redis, we can create a simple rate-limiting middleware to limit the number of requests a user can make in a specific time period.
```

### Step 1: Install Redis and FastAPI dependencies

```
pip install fastapi redis aioredis
```

### Step 2: Create Rate Limiting Middleware

```
Using Redis to store request counts and set an expiration time for rate limits.
```

## 2. Queueing with Celery for Background Tasks

```
Using Celery, we can offload requests to a background worker, allowing FastAPI to respond quickly while the heavy task is processed asynchronously.
```

### Step 1: Install Celery and Redis dependencies
```
pip install celery[redis] fastapi
```

### Step 2: Set Up Celery with Redis as Broker
```
Configure Celery with Redis.
celery_app.py
```

### Step 3: Integrate Celery into FastAPI
```
Add an endpoint that enqueues a task in Celery.
main.py
```

### Step 4: Monitor Task Status 
```
Add an endpoint to check the status of a task.
main.py
```

## Testing Steps

### Example Data
```
For testing, let’s assume we have a document ID that we want to process, which might represent a DOCX or PDF file.

Example Document IDs:
1. doc_1
2. doc_2
3. doc_3
4. doc_4

Each request will simulate the processing of one of these documents.
```

### Testing Steps
#### Step 1: Start Required Services
```
1. Start the Redis server (for both rate limiting and Celery queueing).
redis-server

2. Start Celery with Redis as the broker
celery -A celery_app worker --loglevel=info

```
#### Step 2: Start FastAPI Application
```
uvicorn main:app --reload
```

#### Step 3: Test Rate Limiting
```
1. Open a tool like Postman or curl to send requests to the endpoint.
2. Send requests to /process-doc/ with different document IDs and observe the response.
curl -X POST "http://127.0.0.1:8000/process-doc/" -H "Content-Type: application/json" -d '{"doc_id": "doc_1"}'
3. If you send requests more than RATE_LIMIT times (e.g., 5 times) within the time window (e.g., 60 seconds), you should start seeing a 429 Rate limit exceeded error. This verifies that the rate limiting is working.
```

#### Step 4: Test Background Processing with Celery
```
1. Send a request to /process-doc/ to start processing doc_1 (or any document ID).
2. Check the response for a task_id.
3. To confirm that Celery is processing in the background:
    - Check the Celery worker logs. You should see logs indicating that a task for doc_1 is being processed.
    - Verify that FastAPI returned a response immediately, without waiting for the task to complete.
```

#### Step 5: Check Task Status
```
1. Use the task_id from the previous step and send a request to the /task-status/{task_id} endpoint.
curl -X GET "http://127.0.0.1:8000/task-status/some_unique_task_id"

2. You’ll see one of the following statuses:
    - PENDING: The task is waiting to be processed.
    - STARTED: The task is currently being processed.
    - SUCCESS: The task completed successfully, and you’ll see the result.
    - FAILURE: There was an error processing the task.

3. Wait for Celery to finish processing (or simulate a shorter task for testing), then check the task status again to see the result.
```

#### Step 6: Simulate High Load
```
1. Use a load testing tool like 'locust' or 'artillery' to simulate multiple concurrent users calling /process-doc/.
2. Observe how FastAPI responds to high loads:
    - Users should immediately receive a response with a task_id, indicating that tasks are being queued.
    - Verify in Celery logs that tasks are being processed sequentially in the background.
    - Ensure that rate limiting is triggered if a single IP exceeds the allowed number of requests within the defined window.
```

### Expected Outcomes
- Rate Limiting: Requests exceeding the limit within the set time frame should return a 429 error.
- Immediate Response with Task ID: Users should receive a response quickly with a task_id, even if the actual processing takes time.
- Queue Processing: Tasks should be processed in the background without blocking FastAPI, as confirmed by Celery logs.
- Task Status Checking: Users should be able to check the status and result of their task at /task-status/{task_id}.

- These tests confirm that the application can handle high loads, manage rate limits effectively, and use background processing to provide a better user experience under load conditions.

## Summary

```
- Rate Limiting: Prevents overload from too many requests by limiting request rates per user.
- Queueing with Celery: Offloads time-consuming tasks, freeing up FastAPI to serve more requests without blocking.
- This setup enhances your application’s ability to handle high loads, and users can get responses faster while heavy processing runs in the background. That means:
    1. Fast Initial Response: When a user sends a request that triggers a heavy, time-consuming task (like using the AI Service to process a document), the application doesn’t wait for the task to complete before responding. Instead, it quickly returns a message saying that the task has started and provides a task ID or status update link. This gives users immediate feedback, making the application feel more responsive.

    2. Background Processing: The heavy processing is handled in the background by Celery workers. FastAPI doesn’t have to wait for the AI Service to finish, so it stays free to handle other incoming requests. This is essential when the AI Service has long response times (e.g., over 2 minutes), as it prevents users from waiting for the response and allows FastAPI to serve more users concurrently.

    3. Efficient High Load Handling: Rate limiting prevents overload by ensuring each user can only make a set number of requests within a specific time window. Queueing with Celery ensures that even when multiple users make requests at the same time, the FastAPI application can efficiently manage them by offloading the processing to background workers. This setup makes it possible for FastAPI to handle high loads without slowing down, enabling you to reach your goal of supporting at least 30 users at once.
```