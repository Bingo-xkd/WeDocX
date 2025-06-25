"""
异常处理模块
"""

from typing import Any, Dict, Optional

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from .logging import get_logger

logger = get_logger(__name__)


class WeDocXException(Exception):
    """WeDocX基础异常类"""

    def __init__(
        self,
        message: str,
        error_code: str = "INTERNAL_ERROR",
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationException(WeDocXException):
    """参数验证异常"""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=400,
            details=details,
        )


class TaskNotFoundException(WeDocXException):
    """任务未找到异常"""

    def __init__(self, task_id: str):
        super().__init__(
            message=f"任务 {task_id} 未找到",
            error_code="TASK_NOT_FOUND",
            status_code=404,
            details={"task_id": task_id},
        )


class PDFGenerationException(WeDocXException):
    """PDF生成异常"""

    def __init__(self, message: str, url: str):
        super().__init__(
            message=message,
            error_code="PDF_GENERATION_ERROR",
            status_code=500,
            details={"url": url},
        )


class EmailSendException(WeDocXException):
    """邮件发送异常"""

    def __init__(self, message: str, email: str):
        super().__init__(
            message=message,
            error_code="EMAIL_SEND_ERROR",
            status_code=500,
            details={"email": email},
        )


class URLProcessingException(WeDocXException):
    """URL处理异常"""

    def __init__(self, message: str, url: str):
        super().__init__(
            message=message,
            error_code="URL_PROCESSING_ERROR",
            status_code=400,
            details={"url": url},
        )


def create_error_response(
    status_code: int,
    error_code: str,
    message: str,
    details: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """创建统一的错误响应格式"""
    response = {
        "success": False,
        "error": {
            "code": error_code,
            "message": message,
        },
    }

    if details:
        response["error"]["details"] = details

    return response


async def wechat_exception_handler(
    request: Request, exc: WeDocXException
) -> JSONResponse:
    """WeDocX异常处理器"""
    logger.error(
        f"WeDocX异常: {exc.error_code} - {exc.message}",
        extra={
            "url": str(request.url),
            "method": request.method,
            "details": exc.details,
        },
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=create_error_response(
            status_code=exc.status_code,
            error_code=exc.error_code,
            message=exc.message,
            details=exc.details,
        ),
    )


async def validation_exception_handler(
    request: Request, exc: ValidationError
) -> JSONResponse:
    """Pydantic验证异常处理器"""
    logger.error(
        f"参数验证失败: {exc.errors()}",
        extra={
            "url": str(request.url),
            "method": request.method,
        },
    )

    return JSONResponse(
        status_code=422,
        content=create_error_response(
            status_code=422,
            error_code="VALIDATION_ERROR",
            message="参数验证失败",
            details={"errors": exc.errors()},
        ),
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """HTTP异常处理器"""
    logger.error(
        f"HTTP异常: {exc.status_code} - {exc.detail}",
        extra={
            "url": str(request.url),
            "method": request.method,
        },
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=create_error_response(
            status_code=exc.status_code,
            error_code="HTTP_ERROR",
            message=exc.detail,
        ),
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """通用异常处理器"""
    logger.exception(
        f"未处理的异常: {type(exc).__name__} - {str(exc)}",
        extra={
            "url": str(request.url),
            "method": request.method,
        },
    )

    return JSONResponse(
        status_code=500,
        content=create_error_response(
            status_code=500,
            error_code="INTERNAL_ERROR",
            message="服务器内部错误",
        ),
    )
