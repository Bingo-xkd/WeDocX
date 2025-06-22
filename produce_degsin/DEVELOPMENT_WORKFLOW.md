# 产品开发全景蓝图

我们将整个产品的开发过程划分为四个核心阶段，确保项目系统化、专业化地推进。

1.  **Phase 1: 奠基与规划 (Foundation & Planning)**
2.  **Phase 2: MVP开发 (MVP Development)**
3.  **Phase 3: 测试与部署 (Testing & Deployment)**
4.  **Phase 4: 上线与迭代 (Launch & Iteration)**

---

## Phase 1: 奠基与规划 (项目启动前)

在编写第一行产品代码之前，此阶段的目标是搭建好项目的基础设施和技术蓝图。

### A. 项目管理与协作

*   **版本控制 (Version Control)**: 这是现代开发的基石。
    *   **行动**: 使用 `Git`。建议在 `GitHub`, `GitLab` 或 `Gitee`上创建一个私有项目仓库。
    *   **原因**: 追踪每一次代码变更，便于团队协作和版本回滚。

*   **任务管理 (Task Management)**:
    *   **行动**: 使用项目管理工具，如 `Trello`, `Jira`, `Notion`或 `GitHub Projects`。
    *   **原因**: 将PRD中的功能点拆解成可执行的开发任务（Tasks/Stories），清晰地追踪进度。

### B. 技术栈选型 (Tech Stack Selection)

根据产品需求文档(PRD)，初步技术选型如下：

*   **后端服务**: 负责接收请求、处理任务、与数据库交互。
    *   **推荐**: **Python** (使用 `FastAPI` 或 `Flask` 框架)。
    *   **理由**: 开发效率高，AI生态库（如 `LangChain`, `Transformers`）非常丰富，为未来的AI功能扩展提供无缝支持。

*   **核心功能：网页转PDF**:
    *   **技术方案**: **无头浏览器 (Headless Browser)**。
    *   **具体工具**: **Playwright** (Microsoft)。它提供了强大的API，能够精准控制页面渲染，实现最高保真度的PDF转换。

*   **任务队列 (Task Queue)**:
    *   **推荐**: **Celery** (配合Python) + **Redis** (作为消息中间件)。
    *   **理由**: PDF转换和邮件发送是耗时操作。异步任务队列能瞬间响应用户请求，避免微信机器人超时，极大提升用户体验和系统稳定性。

*   **数据库**:
    *   **关系型数据库 (SQL)**: **PostgreSQL**。功能强大，适合存储用户信息、任务状态、文件元数据等结构化信息。
    *   **向量数据库 (Vector DB)**: (v0.5后引入) `Chroma`, `Milvus`, 或 `Pinecone`。

### C. 系统架构设计 (System Architecture Design)

明确各个组件如何协同工作。

*   **初步架构图**:
    ```mermaid
    graph TD
        A[微信客户端] --> B{API网关};
        B --> C[后端服务 API];
        C --> D[任务队列 Redis];
        D --> E[PDF转换Worker];
        D --> F[邮件发送Worker];
        E --> G[云存储 S3/OSS];
        C --> H[数据库 PostgreSQL];
        E --> H;
        F --> H;
    ```

*   **核心数据流**:
    1.  用户在微信中发送链接。
    2.  后端服务接收请求，校验链接，将"PDF转换任务"推入任务队列，并立即回复用户"处理中"。
    3.  PDF转换Worker从队列中获取任务，启动Playwright进行转换。
    4.  成功后，将PDF文件存入云存储，并将文件信息（URL、元数据）更新到数据库。
    5.  触发一个"邮件发送任务"。
    6.  邮件发送Worker获取任务，从云存储下载PDF，作为附件发送。
    7.  通过微信消息通知用户"任务已完成"。


*   **初步代码架构**:
    ```mermaid
    WeFileAssistant/
        ├── backend/
        │   ├── app/
        │   │   ├── api/
        │   │   │   └── __init__.py
        │   │   ├── core/
        │   │   │   └── __init__.py
        │   │   ├── services/
        │   │   │   └── __init__.py
        │   │   ├── workers/
        │   │   │   └── __init__.py
        │   │   └── __init__.py
        │   ├── tests/
        │   │   └── __init__.py
        │   ├── .gitignore
        │   ├── main.py
        │   └── requirements.txt
        └── produce_degsin/
            ├── DEVELOPMENT_WORKFLOW.md
            └── WeFileAssistant_degsin.md
    ```
*   **目录结构说明**
- backend/: 存放所有后端代码的根目录。
    - app/: 项目的核心应用代码目录。
        - __ init__.py: 这些空文件将目录标记为Python可导入的“包”，是Python项目的标准做法。
        - api/: 存放API接口定义（在我们的技术栈中是FastAPI的Routers）。这能让接口层与业务逻辑分离，使代码更清晰。
        - core/: 存放项目的核心配置，如数据库连接、认证信息、全局设置等。
        - services/: 存放具体的业务逻辑层。例如，pdf_service.py 将封装所有与PDF转换相关的函数或类。
        - workers/: 存放所有异步后台任务（Celery Tasks）。例如，pdf_worker.py 会定义处理PDF转换和邮件发送的耗时任务。
    - tests/: 存放所有单元测试和集成测试代码，是保证代码质量和功能稳定性的关键。
    - .gitignore: 一个特殊文件，用于告诉Git哪些文件或目录不需要被追踪。我们稍后会填充它。
    - main.py: 整个后端服务的启动入口文件。
    - requirements.txt: 用于声明项目所需的所有Python依赖包及其版本，方便环境复现。

---

## Phase 2, 3, 4 ...

后续的 **MVP开发、测试部署、上线迭代** 阶段，我们会在完成第一阶段后逐步展开。每个阶段我都会为你提供同样详尽的指引，包括如何进行任务拆分、代码规范、测试策略、部署方案以及如何收集用户反馈等。 