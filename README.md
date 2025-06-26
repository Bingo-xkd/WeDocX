# WeDocX

[English](./README.en.md) | [中文](./README.md) | 

**WeDocX** 是一款以内嵌式微信聊天机器人为载体的效率工具。它旨在解决用户在微信生态内快速收集、整理、消化和检索各类网页/文档信息的痛点。

我们致力于为知识工作者和重度内容消费者，解决在微信生态中信息过载与知识沉淀困难的核心痛点。产品设计的核心原则是：
- **无缝体验**: 深度集成于微信，以最少的步骤完成核心操作。
- **高质量存档**: 确保内容（特别是图片和布局）的高保真度，还原阅读体验。
- **智能驱动**: 通过AI技术，从简单的"收藏"进化为智能的"消化"与"应用"。

## ✨ 核心功能 (Core Features)

- **高保真网页存档**: 将微信公众号文章或任意网页链接，一键转换为排版精良、无广告干扰的PDF文件。
- **智能内容处理**: (规划中) 利用AI能力，实现文章摘要生成、关键词提取、全文问答。
- **自动化流程**: (规划中) 支持将生成的PDF自动转发到指定邮箱。
- **个人知识库**: (规划中) 将存档的文档构建为可检索的个人知识库。

    

## 🚧 开发进度 (Development Progress)

- ✅ **Phase 1: 奠基与规划 (Foundation & Planning)**
- ✅ **Phase 2: MVP 开发 (v0.1)**
- 🟧 **Phase 3: 产品化与体验优化 (v0.2)** *(部分已完成，已实现API接口、核心业务逻辑、Celery任务链、单元测试等，部分配置与日志功能待完善)*
- ⬜ **Phase 4: AI能力增强 (v0.3 - v0.6)**
- ⬜ **Phase 5: 公开测试版 (v1.0)**

    *更详细的产品设计规划、核心场景分析和功能路线图，请参阅我们的 **[产品需求文档 (PRD)](./produce_degsin/WeDocX_degsin.md)**。*

## 🛠️ 技术栈 (Tech Stack)

- **后端**: Python (FastAPI)
- **核心转换引擎**: Playwright (无头浏览器技术)
- **任务队列**: Celery + Redis
- **数据库**: PostgreSQL
- **AI/ML**: LangChain, Transformers

## 📂 目录结构 (Project Structure)

<details>
<summary>点击展开/折叠查看项目结构</summary>

```
.
├─ 📁 backend/
│  ├─ 📁 app/
│  │  ├─ 📄 __init__.py
│  │  ├─ 📁 api/
│  │  │  └─ 📄 __init__.py
│  │  ├─ 📁 core/
│  │  │  └─ 📄 __init__.py
│  │  ├─ 📁 services/
│  │  │  └─ 📄 __init__.py
│  │  └─ 📁 workers/
│  │     └─ 📄 __init__.py
│  ├─ 📁 tests/
│  │  └─ 📄 __init__.py
│  ├─ 📄 .gitignore
│  ├─ 📄 main.py
│  └─ 📄 requirements.txt
├─ 📁 produce_degsin/
│  ├─ 📄 DEVELOPMENT_WORKFLOW.md
│  └─ 📄 WeDocX_degsin.md
└─ 📄 README.md
```

</details>

## 🚀 快速开始 (Getting Started)

> 项目正在早期开发阶段，以下为初步的开发环境设置指南。

1.  **克隆仓库**
    ```bash
    git clone git@github.com:Bingo-xkd/WeFileAssistant.git
    cd WeFileAssistant
    ```
    *注意：GitHub上的仓库名称可能与项目名 `WeDocX` 不一致。*

2.  **进入后端目录**
    ```bash
    cd backend
    ```

3.  **创建并激活虚拟环境**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS / Linux
    source venv/bin/activate
    ```

4.  **安装依赖**
    ```bash
    pip install -r requirements.txt
    ```

5.  **启动服务 (开发模式)**
    ```bash
    uvicorn app.main:app --reload
    ``` 

## 端到端自动化测试流程（E2E）

本项目支持完整的端到端自动化测试，覆盖"API请求 → PDF生成 → 邮件发送"全链路。

### 一键测试脚本（推荐Linux/macOS）

1. **前提条件**：
   - 已安装并配置好 Redis 服务（需手动启动，Windows 用户请参考 Redis 官方文档）
   - 已安装 conda 环境，且已创建 WeDocX 环境并安装依赖
   - `test_config.json` 中配置了可用的测试邮箱和URL

2. **运行一键测试脚本**：

```bash
bash backend/run_e2e_test.sh
```

脚本会自动完成以下步骤：
- 激活 conda WeDocX 环境
- 启动 Celery worker（后台）
- 启动 FastAPI (Uvicorn) 服务（后台）
- 执行端到端自动化测试（pytest）
- 清理后台进程

> **注意：** Windows 用户请手动依次执行下述手动步骤。

---

### 手动端到端测试流程（适用于Windows或调试）

1. **启动 Redis 服务**
   - 请确保本地已安装并启动 Redis，端口与 `config.py` 保持一致

2. **激活 conda 环境**
   ```bash
   conda activate WeDocX
   ```

3. **启动 Celery worker**
   ```bash
   cd backend
   celery -A app.celery_app.celery_app worker --loglevel=info
   ```

4. **启动 FastAPI (Uvicorn) 服务**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

5. **执行端到端自动化测试**
   ```bash
   pytest backend/tests/test_e2e_process_url.py
   ```

6. **检查结果**
   - 终端输出应显示 API 返回的任务ID和PDF文件名
   - `backend/output/` 目录下应生成 PDF 文件
   - 测试邮箱应收到主题为"网页转PDF"的邮件，附件为 PDF 文件

---

### 注意事项
- 所有测试输入（如测试URL、收件邮箱）均通过 `backend/tests/test_config.json` 配置，便于统一管理和复用。
- 端到端测试需依赖真实的 Redis、Celery worker、SMTP 邮箱服务。
- 邮件送达需人工辅助验证（如需自动化校验可扩展IMAP收件脚本）。
- 若遇到端口占用、依赖未安装等问题，请根据终端提示排查。

---

如需进一步定制测试流程或遇到问题，请查阅项目文档或联系开发者。

## 🏗️ 环境变量说明

| 变量名 | 说明 | 示例 |
|--------|------|------|
| ENVIRONMENT | 运行环境 | development/production |
| DATABASE_URL | 数据库连接 | postgresql://postgres:postgres@db:5432/wedocx |
| REDIS_HOST | Redis主机 | redis |
| REDIS_PORT | Redis端口 | 6379 |
| SMTP_SERVER | SMTP服务器 | smtp.qq.com |
| SMTP_PORT | SMTP端口 | 587 |
| SMTP_USER | 邮箱账号 | your_email@qq.com |
| SMTP_PASSWORD | 邮箱密码 | your_password |
| SENDER_EMAIL | 发件人邮箱 | your_email@qq.com |

## 🐳 Docker一键部署

1. 安装 Docker & Docker Compose
2. 克隆本项目并进入目录
3. 执行：
   ```bash
   docker-compose up --build
   ```
4. 访问 http://localhost:8000 体验API，/admin 访问后台管理

## 🛠️ 常见问题（FAQ）

- **Q: 邮件收不到？**
  - 检查SMTP配置，建议使用QQ/163等主流邮箱，开启SMTP服务并使用授权码。
- **Q: PDF未生成？**
  - 检查output目录权限，确保Playwright依赖已安装。
- **Q: 容器启动失败？**
  - 检查端口占用、环境变量、依赖安装情况。
- **Q: 如何自定义环境变量？**
  - 可在docker-compose.yml或.env文件中覆盖默认配置。

如有更多问题请查阅源码或联系开发者。 