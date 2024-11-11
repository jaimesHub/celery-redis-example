# app/celery_config.py
from celery import Celery

celery_app = Celery(
    "tasks",
    broker="redis://redis:6379/0",  # Redis broker within Docker network
    backend="redis://redis:6379/0"
)
