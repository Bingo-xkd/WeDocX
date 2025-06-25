"""
WeDocX FastAPI 主应用
"""

from app.api.endpoints import router as api_router
from app.core.config import settings
from app.core.exceptions import (
    APIException,
    general_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    wechat_exception_handler,
)
from app.core.logging import get_logger, setup_logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.exceptions import HTTPException

logger = get_logger(__name__)

# 初始化日志
setup_logging()

# 全局FastAPI实例，供服务启动和测试用例import
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="WeDocX - 网页转PDF服务API",
    version="0.2.0",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册全局异常处理器
app.add_exception_handler(APIException, wechat_exception_handler)
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# 注册API路由
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup_event():
    """
    应用启动事件
    """
    logger.info(f"启动 {settings.PROJECT_NAME} v0.2.0")
    logger.info(f"环境: {settings.ENVIRONMENT}")
    logger.info(f"调试模式: {settings.DEBUG}")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"关闭 {settings.PROJECT_NAME}")


@app.get("/")
def read_root():
    return {
        "status": "ok",
        "message": "Welcome to WeDocX API!",
        "version": settings.VERSION,
    }


@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    # 在这里可以添加处理API异常的逻辑
    return JSONResponse(
        status_code=exc.status_code, content={"error": exc.error, "message": exc.detail}
    )


# 支持直接python main.py本地运行
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=settings.WORKERS,
    )
