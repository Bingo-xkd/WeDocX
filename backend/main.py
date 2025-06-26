"""
WeDocX FastAPI 主应用
"""

import secrets

from app.api.endpoints import router as api_router
from app.core.config import settings
from app.core.database import SessionLocal, engine
from app.core.exceptions import (
    TaskNotFoundException,
    ValidationException,
    general_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    wechat_exception_handler,
)
from app.core.logging import get_logger, setup_logging
from app.models import Log, Task, User
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from pydantic import ValidationError
from sqladmin import Admin, ModelView
from sqlalchemy.orm import Session
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
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)
app.add_exception_handler(HTTPException, wechat_exception_handler)
app.add_exception_handler(TaskNotFoundException, wechat_exception_handler)
app.add_exception_handler(ValidationException, wechat_exception_handler)


# 自定义 Task 管理视图
class TaskAdmin(ModelView, model=Task):
    column_list = [
        Task.id,
        Task.url,
        Task.status,
        Task.created_at,
        Task.updated_at,
        Task.pdf_path,
        Task.error_message,
    ]
    column_searchable_list = [Task.id, Task.url]
    column_filters = [Task.status, Task.created_at]
    can_export = True
    can_view_details = True
    name = "任务"
    name_plural = "任务列表"


# 自定义 User 管理视图
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.username,
        User.email,
        User.is_active,
        User.is_superuser,
        User.created_at,
    ]
    column_searchable_list = [User.username, User.email]
    column_filters = [User.is_active, User.is_superuser]
    can_export = True
    can_view_details = True
    name = "用户"
    name_plural = "用户列表"
    form_excluded_columns = [User.hashed_password]
    form_extra_fields = {
        "password": {"type": "password", "label": "密码", "required": False}
    }

    async def on_model_change(self, data, model, is_created, request):
        password = data.get("password")
        if password:
            model.hashed_password = pwd_context.hash(password)


# 自定义 Log 管理视图
class LogAdmin(ModelView, model=Log):
    column_list = [Log.id, Log.user_id, Log.action, Log.detail, Log.created_at]
    column_searchable_list = [Log.action, Log.detail]
    column_filters = [Log.user_id, Log.action, Log.created_at]
    can_export = True
    can_view_details = True
    name = "日志"
    name_plural = "日志列表"


# 注册API路由
app.include_router(api_router, prefix=settings.API_V1_STR)

security = HTTPBasic()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def authenticate(
    credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == credentials.username).first()
    if (
        not user
        or not user.is_active
        or not secrets.compare_digest(user.hashed_password, credentials.password)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="认证失败",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user


# SQLAdmin认证钩子
from sqladmin.authentication import AuthenticationBackend


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        credentials = await security(request)
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.username == credentials.username).first()
            if (
                user
                and user.is_active
                and secrets.compare_digest(user.hashed_password, credentials.password)
            ):
                return True
        finally:
            db.close()
        return False


# 集成 SQLAdmin 后台管理（替换原有admin = Admin(app, engine)）
admin = Admin(
    app, engine, authentication_backend=BasicAuthBackend(secret_key=settings.SECRET_KEY)
)
admin.add_view(TaskAdmin)
admin.add_view(UserAdmin)
admin.add_view(LogAdmin)


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


@app.exception_handler(HTTPException)
async def api_exception_handler(request: Request, exc: HTTPException):
    # 保持原有处理逻辑
    return await wechat_exception_handler(request, exc)


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
