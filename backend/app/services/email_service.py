"""
邮件服务模块，负责处理邮件发送相关功能
"""

import logging
import os
import re
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import List, Optional, Union

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailConfig:
    """邮件配置类"""

    def __init__(
        self,
        smtp_server: str = os.getenv("SMTP_SERVER", "smtp.qq.com"),
        smtp_port: int = int(os.getenv("SMTP_PORT", "465")),
        smtp_user: str = os.getenv("SMTP_USER", ""),
        smtp_password: str = os.getenv("SMTP_PASSWORD", ""),
        sender_email: str = os.getenv("SENDER_EMAIL", ""),
    ):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.sender_email = sender_email or smtp_user

    @property
    def is_configured(self) -> bool:
        """检查是否所有必要的配置都已设置"""
        return all(
            [
                self.smtp_server,
                self.smtp_port,
                self.smtp_user,
                self.smtp_password,
                self.sender_email,
            ]
        )


class EmailService:
    """邮件服务类"""

    def __init__(self, config: EmailConfig):
        self.config = config
        if not config.is_configured:
            raise ValueError("邮件服务配置不完整，请检查配置参数")
        logger.info(
            f"初始化邮件服务: 服务器={config.smtp_server}, 端口={config.smtp_port}"
        )

    def send_email(
        self,
        to_email: Union[str, List[str]],
        subject: str,
        body: str,
        attachments: Optional[List[str]] = None,
        body_type: str = "plain",
    ) -> bool:
        """
        发送邮件

        Args:
            to_email: 收件人邮箱（单个字符串或列表）
            subject: 邮件主题
            body: 邮件正文
            attachments: 附件文件路径列表
            body_type: 邮件正文类型（plain或html）

        Returns:
            bool: 发送是否成功

        Raises:
            ValueError: 收件人邮箱格式无效或主题为空
            FileNotFoundError: 附件文件不存在
            RuntimeError: 发送失败
        """
        # 参数验证
        if not subject:
            raise ValueError("邮件主题不能为空")

        # 转换邮箱地址为列表格式
        to_list = [to_email] if isinstance(to_email, str) else to_email
        logger.info(f"准备发送邮件给: {', '.join(to_list)}")

        # 验证所有邮箱格式
        for email in to_list:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                raise ValueError(f"无效的邮箱地址: {email}")

        # 验证附件
        if attachments:
            logger.info(f"处理附件: {', '.join(attachments)}")
            for attachment_path in attachments:
                if not os.path.exists(attachment_path):
                    raise FileNotFoundError(f"附件文件不存在: {attachment_path}")

        try:
            msg = MIMEMultipart()
            msg["From"] = self.config.sender_email
            msg["To"] = ", ".join(to_list)
            msg["Subject"] = subject

            # 添加邮件正文
            msg.attach(MIMEText(body, body_type, "utf-8"))
            logger.info(f"已添加邮件正文，类型: {body_type}")

            # 添加附件
            if attachments:
                for attachment_path in attachments:
                    with open(attachment_path, "rb") as f:
                        attachment = MIMEApplication(f.read())
                        filename = Path(attachment_path).name
                        attachment.add_header(
                            "Content-Disposition", "attachment", filename=filename
                        )
                        msg.attach(attachment)
                        logger.info(f"已添加附件: {filename}")

            # 连接SMTP服务器并发送
            logger.info("正在连接SMTP服务器...")
            if self.config.smtp_port == 465:
                # 使用SSL连接
                try:
                    with smtplib.SMTP_SSL(
                        self.config.smtp_server, self.config.smtp_port
                    ) as server:
                        server.set_debuglevel(1)  # 开启SMTP debug日志
                        logger.info("使用SSL连接SMTP服务器")
                        server.login(self.config.smtp_user, self.config.smtp_password)
                        logger.info("SMTP登录成功")
                        server.send_message(msg)
                        logger.info("邮件发送成功")
                    return True
                except smtplib.SMTPResponseException as e:
                    if e.smtp_code == -1 and e.smtp_error == b"\x00\x00\x00":
                        logger.warning("SMTP QUIT阶段异常，但邮件已发送成功")
                        return True
                    error_msg = f"SMTP错误: {e.smtp_code} - {e.smtp_error}"
                    logger.error(error_msg)
                    raise RuntimeError(error_msg)
                except Exception as e:
                    error_msg = f"发送邮件失败: {str(e)}"
                    logger.error(error_msg)
                    raise RuntimeError(error_msg)
            else:
                # 使用TLS连接
                try:
                    with smtplib.SMTP(
                        self.config.smtp_server, self.config.smtp_port
                    ) as server:
                        server.set_debuglevel(1)  # 开启SMTP debug日志
                        logger.info("使用TLS连接SMTP服务器")
                        server.starttls()
                        server.login(self.config.smtp_user, self.config.smtp_password)
                        logger.info("SMTP登录成功")
                        server.send_message(msg)
                        logger.info("邮件发送成功")
                    return True
                except smtplib.SMTPResponseException as e:
                    if e.smtp_code == -1 and e.smtp_error == b"\x00\x00\x00":
                        logger.warning("SMTP QUIT阶段异常，但邮件已发送成功")
                        return True
                    error_msg = f"SMTP错误: {e.smtp_code} - {e.smtp_error}"
                    logger.error(error_msg)
                    raise RuntimeError(error_msg)
                except Exception as e:
                    error_msg = f"发送邮件失败: {str(e)}"
                    logger.error(error_msg)
                    raise RuntimeError(error_msg)
        except Exception as e:
            error_msg = f"发送邮件失败: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
