"""
API模型定义
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, HttpUrl, Field


class ProcessUrlRequest(BaseModel):
    """处理URL请求模型"""
    url: HttpUrl = Field(..., description="要处理的网页URL")
    email: EmailStr = Field(..., description="接收PDF的邮箱地址")
    
    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://example.com/article",
                "email": "user@example.com"
            }
        }


class TaskStatusResponse(BaseModel):
    """任务状态响应模型"""
    task_id: str = Field(..., description="任务ID")
    status: str = Field(..., description="任务状态")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: Optional[datetime] = Field(None, description="更新时间")
    progress: Optional[float] = Field(None, description="进度百分比")
    result: Optional[dict] = Field(None, description="任务结果")
    error: Optional[str] = Field(None, description="错误信息")
    
    class Config:
        json_schema_extra = {
            "example": {
                "task_id": "abc123",
                "status": "PENDING",
                "created_at": "2024-01-01T12:00:00",
                "updated_at": "2024-01-01T12:01:00",
                "progress": 50.0,
                "result": {
                    "pdf_file": "20240101-120000-article.pdf",
                    "file_size": 1024000
                },
                "error": None
            }
        }


class ProcessUrlResponse(BaseModel):
    """处理URL响应模型"""
    success: bool = Field(..., description="是否成功")
    task_id: str = Field(..., description="任务ID")
    message: str = Field(..., description="响应消息")
    pdf_file: Optional[str] = Field(None, description="PDF文件名")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "task_id": "abc123",
                "message": "任务已提交，正在处理中",
                "pdf_file": "20240101-120000-article.pdf"
            }
        }


class RetryTaskRequest(BaseModel):
    """重试任务请求模型"""
    task_id: str = Field(..., description="要重试的任务ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "task_id": "abc123"
            }
        }


class RetryTaskResponse(BaseModel):
    """重试任务响应模型"""
    success: bool = Field(..., description="是否成功")
    task_id: str = Field(..., description="任务ID")
    message: str = Field(..., description="响应消息")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "task_id": "abc123",
                "message": "任务重试已提交"
            }
        }


class HealthCheckResponse(BaseModel):
    """健康检查响应模型"""
    status: str = Field(..., description="服务状态")
    timestamp: datetime = Field(..., description="检查时间")
    version: str = Field(..., description="API版本")
    environment: str = Field(..., description="运行环境")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2024-01-01T12:00:00",
                "version": "0.2.0",
                "environment": "development"
            }
        } 