"""
Celery 任务定义
"""

from app.celery_app import celery_app
from app.core.config import settings
from app.services.email_service import EmailConfig, EmailService
from app.services.pdf_service import url_to_pdf_sync


@celery_app.task
def create_pdf_task(url: str, output_path: str) -> str:
    """异步生成PDF文件"""
    url_to_pdf_sync(url, output_path)
    return output_path


@celery_app.task
def send_email_task(to_email: str, subject: str, body: str, attachments: list = None):
    """异步发送邮件"""
    config = EmailConfig(
        smtp_server=settings.SMTP_SERVER,
        smtp_port=settings.SMTP_PORT,
        smtp_user=settings.SMTP_USER,
        smtp_password=settings.SMTP_PASSWORD,
        sender_email=settings.SENDER_EMAIL or settings.SMTP_USER,
    )
    service = EmailService(config)
    service.send_email(
        to_email=to_email, subject=subject, body=body, attachments=attachments
    )
    return True
