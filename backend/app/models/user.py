"""
用户数据模型定义
- 用于描述用户在数据库中的结构和状态
- 依赖 SQLAlchemy ORM
"""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from .task import Base


class User(Base):
    """
    用户表模型
    - 映射到数据库 users 表
    - 记录用户的基本信息和权限
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32), unique=True, nullable=False, index=True)
    email = Column(String(128), unique=True, nullable=False, index=True)
    hashed_password = Column(String(128), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

    def __str__(self):
        return f"用户: {self.username}"
