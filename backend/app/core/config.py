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

    # 文件存储配置
    OUTPUT_DIR: Path = Path("output")

    # SMTP服务器配置
    SMTP_SERVER: str = "smtp.qq.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SENDER_EMAIL: Optional[str] = None

    # Redis配置（用于Celery）
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    @property
    def REDIS_URL(self) -> str:
        """获取Redis连接URL"""
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    class Config:
        env_file = ".env"
        case_sensitive = True


# 创建全局配置实例
settings = Settings()

# 确保输出目录存在
os.makedirs(settings.OUTPUT_DIR, exist_ok=True)
