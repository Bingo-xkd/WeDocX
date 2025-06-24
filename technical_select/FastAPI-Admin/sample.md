# FastAPI-Admin 基础用法示例

以下为 FastAPI-Admin 的基础集成示例，演示如何在 FastAPI 项目中集成后台管理界面。

```python
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider

app = FastAPI()

# 注册 Tortoise-ORM
register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['your_project.models']},
    generate_schemas=True,
    add_exception_handlers=True,
)

# 配置 FastAPI-Admin
@app.on_event('startup')
async def startup():
    await admin_app.configure(
        logo_url="https://fastapi-admin.github.io/img/logo.png",
        template_folders=[],
        providers=[
            UsernamePasswordProvider(
                admin_model='your_project.models.Admin',
            )
        ],
        admin_path="/admin",
    )

app.mount('/admin', admin_app)
```

## 说明
- 需先安装 `fastapi-admin`、`tortoise-orm` 等依赖。
- 需定义 Admin 用户模型。
- 访问 `/admin` 即可进入后台管理界面。
- 更多高级用法请参考官方文档。 