# SETUP IDEA USING CELERY & REDIS & FASTAPI

## Step 1: Install Required Packages
```
pip install fastapi celery redis uvicorn
```

## Step 2: Set Up the Celery Application
```
celery_app.py
Configure Celery with Redis as the broker.
```

## Step 3: Set Up FastAPI Application with Endpoints

```
1. POST /submit-document/: Task run normally without Celery & Redis Setup
2. POST /submit-document-w-celery/: Enqueues the document processing task.
3. GET /task-status/{task_id}: Checks the status of the task.
```

## Step 4: Start the Celery Worker
```
Start a Celery worker
celery -A celery_app worker --loglevel=info
```

## Step 5: Run the FastAPI Application
```
uvicorn main:app --reload
```

## Example Usage
```
1. Submit a Document for Processing: POST /submit-document/
curl -X POST "http://localhost:8000/submit-document/" -H "Content-Type: application/json" -d '{"document_data": {"content": "Sample text to process"}}'

2. Submit a Document with Celery & Redis for Processing: POST /submit-document-w-celery/
curl -X POST "http://localhost:8000/submit-document-w-celery/" -H "Content-Type: application/json" -d '{"document_data": {"content": "Sample text to process"}}'

3. Check Task Status: GET /task-status/{task_id}
curl "http://localhost:8000/task-status/some_unique_task_id"
```