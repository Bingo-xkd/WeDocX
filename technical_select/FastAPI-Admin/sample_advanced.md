# FastAPI-Admin 高级用法与集成建议

## 1. 自定义页面与组件
可通过自定义模板和组件扩展后台功能，例如添加统计报表页面。

```python
# 参考官方文档自定义页面
# https://fastapi-admin.github.io/guide/custom_page.html
```

## 2. 权限与认证体系
支持基于角色的权限管理，可自定义 Admin 用户模型和权限分组。

```python
# 定义自定义 Admin 用户模型，配置不同角色权限
```

## 3. 多数据库支持
可配置多种数据库，适合复杂业务场景。

## 4. 与主业务系统解耦
- 推荐将 FastAPI-Admin 作为主 FastAPI 应用的子应用（app.mount），实现统一认证和路由管理。
- 可通过 API 与主业务系统交互，实现数据同步和业务联动。

## 5. 常见问题（FAQ）
- Q: FastAPI-Admin 支持哪些 ORM？
  A: 仅支持 Tortoise-ORM。
- Q: 如何与现有 SQLAlchemy 项目集成？
  A: 需评估 ORM 兼容性，或考虑 SQLAdmin。
- Q: 如何自定义主题和前端样式？
  A: 支持 Ant Design 主题自定义，可参考官方文档。
- Q: 如何实现多用户、多角色权限管理？
  A: 通过自定义 Admin 用户模型和权限分组实现。

## 6. 与本项目集成建议
- 若项目 ORM 选型为 Tortoise-ORM，推荐直接集成 FastAPI-Admin。
- 若已采用 SQLAlchemy，建议优先考虑 SQLAdmin。
- 可通过统一认证体系和 API 实现与主业务系统的数据联动。
- 生产环境建议使用 Docker 部署，便于维护和扩展。 