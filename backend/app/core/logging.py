"""
日志系统模块
"""

import sys
from pathlib import Path

from loguru import logger

from .config import settings


def setup_logging():
    """设置日志系统"""
    # 移除默认的日志处理器
    logger.remove()
    
    # 添加控制台日志处理器
    logger.add(
        sys.stdout,
        format=settings.LOG_FORMAT,
        level=settings.LOG_LEVEL,
        colorize=True,
        backtrace=True,
        diagnose=True,
    )
    
    # 添加文件日志处理器
    logger.add(
        settings.LOG_FILE,
        format=settings.LOG_FORMAT,
        level=settings.LOG_LEVEL,
        rotation=settings.LOG_ROTATION,
        retention=settings.LOG_RETENTION,
        compression="zip",
        backtrace=True,
        diagnose=True,
    )
    
    # 为第三方库设置日志级别
    logger.add(
        "logs/error.log",
        format=settings.LOG_FORMAT,
        level="ERROR",
        rotation=settings.LOG_ROTATION,
        retention=settings.LOG_RETENTION,
        compression="zip",
        backtrace=True,
        diagnose=True,
    )


def get_logger(name: str = None):
    """获取日志记录器"""
    if name:
        return logger.bind(name=name)
    return logger


# 初始化日志系统
setup_logging() 