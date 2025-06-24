# SQLAdmin 基础用法示例

以下为 SQLAdmin 的基础集成示例，演示如何在 FastAPI + SQLAlchemy 项目中集成后台管理界面。

```python
from fastapi import FastAPI
from sqladmin import Admin, ModelView
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from your_project.models import User, Task

app = FastAPI()

# 配置 SQLAlchemy 数据库
engine = create_engine('sqlite:///db.sqlite3')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 配置 SQLAdmin
admin = Admin(app, engine)

# 注册模型视图
admin.add_view(ModelView(User))
admin.add_view(ModelView(Task))
```

## 说明
- 需先安装 `sqladmin`、`sqlalchemy` 等依赖。
- 需定义 User、Task 等 SQLAlchemy 模型。
- 访问 `/admin` 即可进入后台管理界面。
- 支持自定义视图、权限、主题等高级功能，详见官方文档。 