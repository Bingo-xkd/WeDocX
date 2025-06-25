"""
Logging configuration for Wechaty Bot
"""

import sys

from loguru import logger

LOG_LEVEL = "INFO"
LOG_FILE = "logs/wechat_bot.log"
LOG_FORMAT = (
    "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}"
)
LOG_ROTATION = "1 day"
LOG_RETENTION = "30 days"


def setup_bot_logging():
    """
    Setup loguru for the wechat bot.
    """
    logger.remove()

    # Console logger
    logger.add(
        sys.stdout,
        level=LOG_LEVEL.upper(),
        format=LOG_FORMAT,
        colorize=True,
    )

    # File logger
    logger.add(
        LOG_FILE,
        level=LOG_LEVEL.upper(),
        format=LOG_FORMAT,
        rotation=LOG_ROTATION,
        retention=LOG_RETENTION,
        enqueue=True,
        backtrace=True,
        diagnose=True,
    )
    logger.info("Wechat Bot logging configured.")


def get_bot_logger():
    """
    Get the configured logger instance.
    """
    return logger
