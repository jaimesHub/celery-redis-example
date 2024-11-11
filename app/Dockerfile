# app/Dockerfile
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . /app

# Install dependencies, including Gunicorn and Uvicorn
RUN pip install fastapi uvicorn gunicorn celery redis

# Start the FastAPI app with Gunicorn and Uvicorn workers
CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
