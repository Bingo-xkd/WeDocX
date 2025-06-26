"""
任务数据模型定义
- 用于描述任务在数据库中的结构和状态
- 依赖 SQLAlchemy ORM
"""

import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class TaskStatus(enum.Enum):
    """任务状态枚举，描述任务的生命周期"""

    PENDING = "PENDING"  # 等待中
    STARTED = "STARTED"  # 已开始执行
    SUCCESS = "SUCCESS"  # 执行成功
    FAILURE = "FAILURE"  # 执行失败
    RETRY = "RETRY"  # 重试中


class Task(Base):
    """
    任务表模型
    - 映射到数据库 tasks 表
    - 记录每个任务的详细信息、状态和结果
    """

    __tablename__ = "tasks"

    id = Column(String(36), primary_key=True, index=True)  # 任务唯一ID（UUID）
    url = Column(String, nullable=False)  # 任务处理的目标URL
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)  # 当前任务状态
    created_at = Column(DateTime, default=datetime.utcnow)  # 创建时间
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )  # 更新时间
    pdf_path = Column(String, nullable=True)  # 生成的PDF文件路径
    error_message = Column(Text, nullable=True)  # 错误信息（如任务失败时）

    def __repr__(self):
        return f"<Task(id='{self.id}', status='{self.status}')>"
