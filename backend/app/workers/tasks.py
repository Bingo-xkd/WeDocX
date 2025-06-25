"""
Celery 任务定义
"""

import os
from typing import Optional

from celery import current_task
from celery.utils.log import get_task_logger

from app.celery_app import celery_app
from app.core.config import settings
from app.core.exceptions import PDFGenerationException, EmailSendException
from app.core.logging import get_logger
from app.services.email_service import EmailConfig, EmailService, send_email_with_attachment
from app.services.pdf_service import url_to_pdf_sync
from app.services.document_service import process_url_to_pdf

logger = get_logger()
celery_logger = get_task_logger(__name__)


@celery_app.task(
    bind=True,
    max_retries=settings.CELERY_TASK_MAX_RETRIES,
    default_retry_delay=60,  # 1分钟后重试
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
)
def create_pdf_task(self, url: str):
    """
    Celery task to create a PDF from a URL.
    """
    try:
        logger.info(f"[{self.request.id}] Starting PDF creation for URL: {url}")
        output_path = process_url_to_pdf(url, task_id=str(self.request.id))
        logger.info(
            f"[{self.request.id}] PDF created successfully. Path: {output_path}"
        )
        return {"status": "SUCCESS", "file_path": str(output_path)}
    except Exception as e:
        logger.error(
            f"[{self.request.id}] Error creating PDF for URL {url}: {e}", exc_info=True
        )
        raise self.retry(exc=e)


@celery_app.task(
    bind=True,
    max_retries=settings.CELERY_TASK_MAX_RETRIES,
    default_retry_delay=30,  # 30秒后重试
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
)
def send_email_task(self, recipient_email: str, file_path: str):
    """
    Celery task to send an email with a PDF attachment.
    """
    try:
        logger.info(
            f"[{self.request.id}] Sending PDF to {recipient_email} from path: {file_path}"
        )
        send_email_with_attachment(
            subject="Your PDF is ready",
            recipient_email=recipient_email,
            body="Please find your generated PDF attached.",
            file_path=file_path,
        )
        logger.info(
            f"[{self.request.id}] Email sent successfully to {recipient_email}."
        )
        return {"status": "SUCCESS", "recipient": recipient_email}
    except Exception as e:
        logger.error(
            f"[{self.request.id}] Error sending email to {recipient_email}: {e}",
            exc_info=True,
        )
        raise self.retry(exc=e)


@celery_app.task(bind=True)
def cleanup_task(self, pdf_path: str) -> dict:
    """
    清理任务 - 删除临时文件
    
    Args:
        pdf_path: PDF文件路径
        
    Returns:
        dict: 清理结果
    """
    task_id = self.request.id
    logger.info(f"开始清理任务 {task_id}: {pdf_path}")
    
    try:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
            logger.info(f"文件已删除: {pdf_path}")
        
        return {
            "cleaned": True,
            "file_path": pdf_path,
        }
        
    except Exception as exc:
        logger.error(f"清理任务失败 {task_id}: {str(exc)}")
        return {
            "cleaned": False,
            "file_path": pdf_path,
            "error": str(exc),
        }
