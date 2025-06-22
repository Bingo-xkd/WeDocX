# 微信文件助手 (WeDocX)

微信文件助手 **WeDocX** 一款以内嵌式微信聊天机器人为载体的效率工具。它旨在解决用户在微信生态内快速收集、整理、消化和检索各类网页/文档信息的痛点。

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
- ⏳ **Phase 2: MVP 开发 (v0.1)** *(进行中)*
- ⬜ **Phase 3: 产品化与体验优化 (v0.2)**
- ⬜ **Phase 4: AI能力增强 (v0.3 - v0.6)**
- ⬜ **Phase 5: 公开测试版 (v1.0)**

    *更详细的产品设计规划、核心场景分析和功能路线图，请参阅我们的 **[产品需求文档 (PRD)](./produce_degsin/WeFileAssistant_degsin.md)**。*

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
│  └─ 📄 WeFileAssistant_degsin.md
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