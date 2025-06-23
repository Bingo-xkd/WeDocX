"""
Celery 应用配置
"""

from app.core.config import settings
from celery import Celery

celery_app = Celery("WeDocX", broker=settings.REDIS_URL, backend=settings.REDIS_URL)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Asia/Shanghai",
    enable_utc=True,
)
