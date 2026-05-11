from celery import Celery
from app.config import settings

celery_app = Celery(
    "zk_credential",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.proof_task"],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    worker_prefetch_multiplier=1,  # one heavy ZK task at a time
)
