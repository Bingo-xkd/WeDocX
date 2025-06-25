"""
Celery 应用配置
"""

from app.core.config import settings
from app.core.logging import get_logger
from celery import Celery

logger = get_logger(__name__)

# 创建Celery应用
celery_app = Celery(
    "WeDocX",
    broker=settings.CELERY_BROKER_URL_VALUE,
    backend=settings.CELERY_RESULT_BACKEND_VALUE,
)

# Celery配置
celery_app.conf.update(
    # 序列化配置
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    
    # 时区配置
    timezone="Asia/Shanghai",
    enable_utc=True,
    
    # 任务配置
    task_soft_time_limit=settings.CELERY_TASK_SOFT_TIME_LIMIT,
    task_time_limit=settings.CELERY_TASK_TIME_LIMIT,
    task_max_retries=settings.CELERY_TASK_MAX_RETRIES,
    
    # 结果配置
    result_expires=3600,  # 1小时
    result_persistent=True,
    
    # 工作进程配置
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    
    # 重试配置
    task_acks_late=True,
    worker_disable_rate_limits=False,
    
    # 日志配置
    worker_log_format="[%(asctime)s: %(levelname)s/%(processName)s] %(message)s",
    worker_task_log_format="[%(asctime)s: %(levelname)s/%(processName)s][%(task_name)s(%(task_id)s)] %(message)s",
)

# 自动发现任务
celery_app.autodiscover_tasks(["app.workers"])

logger.info("Celery应用配置完成")
