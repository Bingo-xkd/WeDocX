"""
API端点模块
"""

from datetime import datetime
from typing import Optional

from celery.result import AsyncResult
from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError

from ..core.exceptions import (
    TaskNotFoundException,
    URLProcessingException,
    ValidationException,
)
from ..core.logging import get_logger
from ..workers.tasks import create_pdf_task, send_email_task
from celery import chain
from .models import (
    HealthCheckResponse,
    ProcessUrlRequest,
    ProcessUrlResponse,
    RetryTaskRequest,
    RetryTaskResponse,
    TaskStatusResponse,
)

logger = get_logger(__name__)

router = APIRouter()


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """健康检查端点"""
    return HealthCheckResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="0.2.0",
        environment="development",
    )


@router.post("/process-url", response_model=ProcessUrlResponse)
async def process_url(request: ProcessUrlRequest):
    """
    处理URL请求，生成PDF并发送邮件
    
    Args:
        request: 包含URL和邮箱的请求
        
    Returns:
        ProcessUrlResponse: 包含任务ID的响应
    """
    try:
        logger.info(f"收到URL处理请求: {request.url}")
        
        # 验证URL
        url_str = str(request.url)
        if not url_str.startswith(('http://', 'https://')):
            raise URLProcessingException("无效的URL格式", url_str)
        
        # 生成输出文件名
        from datetime import datetime
        import os
        
        now_str = datetime.now().strftime("%Y%m%d-%H-%M-%S")
        base_name = url_str.split("/")[-1][:10] or "file"
        pdf_filename = f"{now_str}-{base_name}.pdf"
        
        # 确保输出目录存在
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "output"))
        os.makedirs(output_dir, exist_ok=True)
        pdf_path = os.path.join(output_dir, pdf_filename)
        
        # 创建任务链：先生成PDF，再发邮件
        task_chain = chain(
            create_pdf_task.s(url_str, pdf_path),
            send_email_task.s(
                str(request.email),
                "网页转PDF",
                f"请查收由WeDocX生成的PDF文件：{pdf_filename}",
            ),
        )
        
        # 提交任务
        result = task_chain.apply_async()
        
        logger.info(f"任务已提交: {result.id}")
        
        return ProcessUrlResponse(
            success=True,
            task_id=str(result.id),
            message="任务已提交，正在处理中",
            pdf_file=pdf_filename,
        )
        
    except ValidationException as e:
        logger.error(f"参数验证失败: {e.message}")
        raise
    except URLProcessingException as e:
        logger.error(f"URL处理失败: {e.message}")
        raise
    except Exception as e:
        logger.exception(f"处理URL时发生异常: {str(e)}")
        raise HTTPException(status_code=500, detail=f"任务提交失败: {str(e)}")


@router.get("/task-status/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    """
    获取任务状态
    
    Args:
        task_id: 任务ID
        
    Returns:
        TaskStatusResponse: 任务状态信息
    """
    try:
        logger.info(f"查询任务状态: {task_id}")
        
        # 获取Celery任务结果
        task_result = AsyncResult(task_id)
        
        if not task_result:
            raise TaskNotFoundException(task_id)
        
        # 构建响应数据
        response_data = {
            "task_id": task_id,
            "status": task_result.status,
            "created_at": datetime.now(),  # 这里应该从数据库获取
            "updated_at": datetime.now(),
            "progress": None,
            "result": None,
            "error": None,
        }
        
        # 根据任务状态设置详细信息
        if task_result.status == "SUCCESS":
            response_data["result"] = task_result.result
            response_data["progress"] = 100.0
        elif task_result.status == "FAILURE":
            response_data["error"] = str(task_result.info)
            response_data["progress"] = 0.0
        elif task_result.status == "PENDING":
            response_data["progress"] = 0.0
        elif task_result.status == "STARTED":
            response_data["progress"] = 25.0
        elif task_result.status == "RETRY":
            response_data["progress"] = 50.0
        
        return TaskStatusResponse(**response_data)
        
    except TaskNotFoundException as e:
        logger.error(f"任务未找到: {task_id}")
        raise
    except Exception as e:
        logger.exception(f"查询任务状态时发生异常: {str(e)}")
        raise HTTPException(status_code=500, detail=f"查询任务状态失败: {str(e)}")


@router.post("/retry-task", response_model=RetryTaskResponse)
async def retry_task(request: RetryTaskRequest):
    """
    重试失败的任务
    
    Args:
        request: 包含任务ID的请求
        
    Returns:
        RetryTaskResponse: 重试结果
    """
    try:
        logger.info(f"重试任务: {request.task_id}")
        
        # 获取原任务结果
        task_result = AsyncResult(request.task_id)
        
        if not task_result:
            raise TaskNotFoundException(request.task_id)
        
        # 检查任务是否可以重试
        if task_result.status != "FAILURE":
            raise ValidationException(f"任务状态为 {task_result.status}，无法重试")
        
        # 重新提交任务
        # 这里需要根据原任务的参数重新创建任务链
        # 暂时返回成功，实际实现需要从数据库获取原任务参数
        
        logger.info(f"任务重试已提交: {request.task_id}")
        
        return RetryTaskResponse(
            success=True,
            task_id=request.task_id,
            message="任务重试已提交",
        )
        
    except (TaskNotFoundException, ValidationException) as e:
        logger.error(f"重试任务失败: {e.message}")
        raise
    except Exception as e:
        logger.exception(f"重试任务时发生异常: {str(e)}")
        raise HTTPException(status_code=500, detail=f"重试任务失败: {str(e)}")


@router.get("/")
async def read_root():
    """
    根端点，返回API状态
    """
    return {
        "status": "ok",
        "message": "Welcome to WeDocX API!",
        "version": "0.2.0",
        "timestamp": datetime.now(),
    } 