"""
日志数据模型定义
- 用于描述操作日志在数据库中的结构
- 依赖 SQLAlchemy ORM
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from .task import Base


class Log(Base):
    """
    日志表模型
    - 映射到数据库 logs 表
    - 记录用户操作、系统事件等
    """

    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.id"), nullable=True, index=True
    )  # 可关联用户
    action = Column(String(64), nullable=False)  # 操作类型
    detail = Column(Text, nullable=True)  # 详细内容
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Log(id={self.id}, action='{self.action}')>"

    def __str__(self):
        return f"日志: {self.action}"
