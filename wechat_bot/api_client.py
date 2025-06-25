"""
API Client for WeDocX Backend
"""

from typing import Any, Dict, Optional

import httpx

from .logging_config import get_bot_logger

logger = get_bot_logger()

# 从环境变量或配置文件中获取后端的地址
BACKEND_URL = "http://localhost:8000/api/v1"


async def start_task(url: str, email: Optional[str] = None) -> Dict[str, Any]:
    """
    Call the /process-url endpoint to start a new task.
    """
    async with httpx.AsyncClient() as client:
        payload = {"url": url}
        if email:
            payload["email"] = email

        logger.info(f"Calling start_task API with URL: {url}")
        response = await client.post(f"{BACKEND_URL}/process-url", json=payload)
        response.raise_for_status()
        logger.info(f"start_task API call successful for URL: {url}")
        return response.json()


async def get_task_status(task_id: str) -> Dict[str, Any]:
    """
    Call the /task-status endpoint to get the status of a task.
    """
    async with httpx.AsyncClient() as client:
        logger.info(f"Calling get_task_status API for Task ID: {task_id}")
        response = await client.get(f"{BACKEND_URL}/task-status/{task_id}")
        response.raise_for_status()
        logger.info(f"get_task_status API call successful for Task ID: {task_id}")
        return response.json()


async def retry_task(task_id: str) -> Dict[str, Any]:
    """
    Call the /retry-task endpoint to retry a failed task.
    """
    async with httpx.AsyncClient() as client:
        logger.info(f"Calling retry_task API for Task ID: {task_id}")
        response = await client.post(
            f"{BACKEND_URL}/retry-task", json={"task_id": task_id}
        )
        response.raise_for_status()
        logger.info(f"retry_task API call successful for Task ID: {task_id}")
        return response.json()
