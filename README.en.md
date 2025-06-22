# WeDocX

[English](./README.en.md) | [中文](./README.md) | 

**WeDocX** is an efficiency tool integrated as a WeChat chatbot. It's designed to solve the pain points of collecting, organizing, digesting, and retrieving various web pages and documents within the WeChat ecosystem.

We are dedicated to helping knowledge workers and heavy content consumers overcome the core challenges of information overload and knowledge consolidation. The core principles of our product design are:

-   **Seamless Experience**: Deeply integrated into WeChat to complete core tasks with minimal steps.
-   **High-Fidelity Archiving**: Ensure high fidelity of content (especially images and layout) to restore the original reading experience.
-   **AI-Driven**: Evolve from simple "bookmarking" to intelligent "digesting" and "applying" through AI technology.

## ✨ Core Features

-   **High-Fidelity Web Archiving**: Convert WeChat articles or any web links into well-formatted, ad-free PDF files with one click.
-   **Intelligent Content Processing**: (Planned) Utilize AI capabilities for summary generation, keyword extraction, and full-text Q&A.
-   **Automated Workflow**: (Planned) Support automatic forwarding of generated PDFs to a specified email address.
-   **Personal Knowledge Base**: (Planned) Build a searchable personal knowledge base from archived documents.

## 🚧 Development Progress

-   ✅ **Phase 1: Foundation & Planning**
-   ⏳ **Phase 2: MVP Development (v0.1)** *(In Progress)*
-   ⬜ **Phase 3: Productization & Experience Optimization (v0.2)**
-   ⬜ **Phase 4: AI Enhancement (v0.3 - v0.6)**
-   ⬜ **Phase 5: Public Beta (v1.0)**

*For a more detailed product design, core scenarios, and feature roadmap, please refer to our **[Product Requirements Document (PRD)](./produce_degsin/WeDocX_degsin.md)**.*

## 🛠️ Tech Stack

-   **Backend**: Python (FastAPI)
-   **Core Conversion Engine**: Playwright (Headless Browser)
-   **Task Queue**: Celery + Redis
-   **Database**: PostgreSQL
-   **AI/ML**: LangChain, Transformers

## 📂 Project Structure

<details>
<summary>Click to expand/collapse the project structure</summary>

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

## 🚀 Getting Started

> The project is in its early development stage. The following is a preliminary guide for setting up the development environment.

1.  **Clone the repository**
    ```bash
    git clone git@github.com:Bingo-xkd/WeFileAssistant.git
    cd WeFileAssistant
    ```
    *Note: The repository name on GitHub might differ from the project name `WeDocX`.*

2.  **Enter the backend directory**
    ```bash
    cd backend
    ```

3.  **Create and activate a virtual environment**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS / Linux
    source venv/bin/activate
    ```

4.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Start the service (development mode)**
    ```bash
    uvicorn app.main:app --reload
    ``` 