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
from app.services.email_service import EmailConfig, EmailService
from app.services.pdf_service import url_to_pdf_sync

logger = get_logger(__name__)
celery_logger = get_task_logger(__name__)


@celery_app.task(
    bind=True,
    max_retries=settings.CELERY_TASK_MAX_RETRIES,
    default_retry_delay=60,  # 1分钟后重试
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
)
def create_pdf_task(self, url: str, output_path: str) -> dict:
    """
    异步生成PDF文件
    
    Args:
        url: 要转换的网页URL
        output_path: PDF输出路径
        
    Returns:
        dict: 包含PDF文件信息的字典
    """
    task_id = self.request.id
    logger.info(f"开始生成PDF任务 {task_id}: {url}")
    
    try:
        # 更新任务状态
        current_task.update_state(
            state="STARTED",
            meta={"progress": 0, "message": "开始生成PDF"}
        )
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 更新进度
        current_task.update_state(
            state="PROGRESS",
            meta={"progress": 25, "message": "正在访问网页"}
        )
        
        # 生成PDF
        url_to_pdf_sync(url, output_path)
        
        # 检查文件是否生成成功
        if not os.path.exists(output_path):
            raise PDFGenerationException("PDF文件生成失败", url)
        
        # 获取文件大小
        file_size = os.path.getsize(output_path)
        
        # 更新进度
        current_task.update_state(
            state="PROGRESS",
            meta={"progress": 100, "message": "PDF生成完成"}
        )
        
        result = {
            "pdf_path": output_path,
            "pdf_file": os.path.basename(output_path),
            "file_size": file_size,
            "url": url,
        }
        
        logger.info(f"PDF生成成功 {task_id}: {result['pdf_file']} ({file_size} bytes)")
        return result
        
    except Exception as exc:
        logger.exception(f"PDF生成失败 {task_id}: {str(exc)}")
        
        # 如果是重试次数未达到上限，则重试
        if self.request.retries < self.max_retries:
            logger.info(f"准备重试PDF生成任务 {task_id}，第 {self.request.retries + 1} 次重试")
            raise self.retry(exc=exc)
        else:
            # 重试次数已达上限，记录失败
            logger.error(f"PDF生成任务 {task_id} 重试次数已达上限，任务失败")
            raise PDFGenerationException(f"PDF生成失败: {str(exc)}", url)


@celery_app.task(
    bind=True,
    max_retries=settings.CELERY_TASK_MAX_RETRIES,
    default_retry_delay=30,  # 30秒后重试
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
)
def send_email_task(self, pdf_result: dict, to_email: str, subject: str, body: str) -> dict:
    """
    异步发送邮件
    
    Args:
        pdf_result: 上一个任务(create_pdf_task)的结果
        to_email: 收件人邮箱
        subject: 邮件主题
        body: 邮件正文
        
    Returns:
        dict: 邮件发送结果
    """
    task_id = self.request.id
    logger.info(f"开始发送邮件任务 {task_id}: {to_email}")
    
    try:
        # 更新任务状态
        current_task.update_state(
            state="STARTED",
            meta={"progress": 0, "message": "开始发送邮件"}
        )
        
        # 验证PDF文件是否存在
        pdf_path = pdf_result.get("pdf_path")
        if not pdf_path or not os.path.exists(pdf_path):
            raise EmailSendException("PDF文件不存在", to_email)
        
        # 更新进度
        current_task.update_state(
            state="PROGRESS",
            meta={"progress": 50, "message": "正在配置邮件服务"}
        )
        
        # 配置邮件服务
        config = EmailConfig(
            smtp_server=settings.SMTP_SERVER,
            smtp_port=settings.SMTP_PORT,
            smtp_user=settings.SMTP_USER,
            smtp_password=settings.SMTP_PASSWORD,
            sender_email=settings.SENDER_EMAIL or settings.SMTP_USER,
            use_tls=settings.SMTP_USE_TLS,
            use_ssl=settings.SMTP_USE_SSL,
        )
        
        service = EmailService(config)
        
        # 更新进度
        current_task.update_state(
            state="PROGRESS",
            meta={"progress": 75, "message": "正在发送邮件"}
        )
        
        # 发送邮件
        service.send_email(
            to_email=to_email,
            subject=subject,
            body=body,
            attachments=[pdf_path]
        )
        
        # 更新进度
        current_task.update_state(
            state="PROGRESS",
            meta={"progress": 100, "message": "邮件发送完成"}
        )
        
        result = {
            "email_sent": True,
            "to_email": to_email,
            "subject": subject,
            "pdf_file": pdf_result.get("pdf_file"),
            "file_size": pdf_result.get("file_size"),
        }
        
        logger.info(f"邮件发送成功 {task_id}: {to_email}")
        return result
        
    except Exception as exc:
        logger.exception(f"邮件发送失败 {task_id}: {str(exc)}")
        
        # 如果是重试次数未达到上限，则重试
        if self.request.retries < self.max_retries:
            logger.info(f"准备重试邮件发送任务 {task_id}，第 {self.request.retries + 1} 次重试")
            raise self.retry(exc=exc)
        else:
            # 重试次数已达上限，记录失败
            logger.error(f"邮件发送任务 {task_id} 重试次数已达上限，任务失败")
            raise EmailSendException(f"邮件发送失败: {str(exc)}", to_email)


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
