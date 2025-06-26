"""
日志配置模块
"""

import sys

from loguru import logger

from .config import settings


def setup_logging():
    """
    配置loguru日志系统
    """
    logger.remove()  # 移除默认的控制台输出

    # 添加控制台输出
    logger.add(
        sys.stdout,
        level=settings.LOG_LEVEL.upper(),
        format=settings.LOG_FORMAT,
        colorize=True,
    )

    # 添加文件输出
    logger.add(
        settings.LOG_FILE,
        level=settings.LOG_LEVEL.upper(),
        format=settings.LOG_FORMAT,
        rotation=settings.LOG_ROTATION,  # 例如 "1 day", "500 MB"
        retention=settings.LOG_RETENTION,  # 例如 "30 days"
        enqueue=True,  # 使日志写入异步，防止阻塞
        backtrace=True,  # 完整的回溯信息
        diagnose=True,  # 详细的异常诊断信息
        serialize=False,  # 如果需要JSON格式日志，可以设为True
    )

    logger.info("日志系统配置完成.")


def get_logger(name=None):
    """
    获取配置好的logger实例
    :param name: 可选的logger名称（兼容logging风格）
    """
    if name:
        return logger.bind(name=name)
    return logger


# 初始化日志系统
setup_logging()
