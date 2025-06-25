"""
WeDocX FastAPI 主应用
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from app.api.endpoints import router as api_router
from app.core.config import settings
from app.core.exceptions import (
    WeDocXException,
    general_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    wechat_exception_handler,
)
from app.core.logging import get_logger

logger = get_logger(__name__)

# 全局FastAPI实例，供服务启动和测试用例import
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="WeDocX - 网页转PDF服务API",
    version="0.2.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册异常处理器
app.add_exception_handler(WeDocXException, wechat_exception_handler)
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# 注册API路由
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    logger.info(f"启动 {settings.PROJECT_NAME} v0.2.0")
    logger.info(f"环境: {settings.ENVIRONMENT}")
    logger.info(f"调试模式: {settings.DEBUG}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"关闭 {settings.PROJECT_NAME}")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Welcome to WeDocX API!", "version": settings.VERSION}

# 支持直接python main.py本地运行
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG, workers=settings.WORKERS)
