"""
配置管理模块
"""

import os
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置类"""

    # 项目基础配置
    PROJECT_NAME: str = "WeDocX"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"  # development, production, testing

    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1

    # 文件存储配置
    OUTPUT_DIR: Path = Path("output")
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS: list = [".pdf", ".html", ".txt"]

    # SMTP服务器配置
    SMTP_SERVER: str = "smtp.qq.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SENDER_EMAIL: Optional[str] = None
    SMTP_USE_TLS: bool = True
    SMTP_USE_SSL: bool = False

    # Redis配置（用于Celery）
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None

    # Celery配置
    CELERY_BROKER_URL: Optional[str] = None
    CELERY_RESULT_BACKEND: Optional[str] = None
    CELERY_TASK_SOFT_TIME_LIMIT: int = 300  # 5分钟
    CELERY_TASK_TIME_LIMIT: int = 600  # 10分钟
    CELERY_TASK_MAX_RETRIES: int = 3

    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/wedocx.log"
    LOG_FORMAT: str = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}"
    LOG_ROTATION: str = "1 day"
    LOG_RETENTION: str = "30 days"

    # 数据库配置（为后台管理准备）
    DATABASE_URL: Optional[str] = None
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "wedocx"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = ""

    # 安全配置
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # 微信机器人配置
    WECHAT_BOT_TOKEN: Optional[str] = None
    WECHAT_BOT_ENABLED: bool = False

    @property
    def REDIS_URL(self) -> str:
        """获取Redis连接URL"""
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    @property
    def CELERY_BROKER_URL_VALUE(self) -> str:
        """获取Celery Broker URL"""
        return self.CELERY_BROKER_URL or self.REDIS_URL

    @property
    def CELERY_RESULT_BACKEND_VALUE(self) -> str:
        """获取Celery Result Backend URL"""
        return self.CELERY_RESULT_BACKEND or self.REDIS_URL

    @property
    def DATABASE_URL_VALUE(self) -> str:
        """获取数据库连接URL"""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "ignore"


# 创建全局配置实例
settings = Settings()

# 确保输出目录存在
os.makedirs(settings.OUTPUT_DIR, exist_ok=True)

# 确保日志目录存在
log_dir = Path(settings.LOG_FILE).parent
os.makedirs(log_dir, exist_ok=True)
