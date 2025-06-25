"""
Unit tests for wechat_bot/api_client.py
"""

from unittest.mock import AsyncMock, patch

import httpx
import pytest

from wechat_bot.api_client import get_task_status, retry_task, start_task

# Mock responses
MOCK_TASK_RESPONSE = {
    "task_id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "PENDING",
}

MOCK_STATUS_RESPONSE = {
    "task_id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "SUCCESS",
    "result": "path/to/file.pdf",
}


@pytest.mark.asyncio
async def test_start_task_success():
    """Test successful task creation"""
    url = "https://example.com"

    # Mock the httpx.AsyncClient
    with patch("httpx.AsyncClient") as mock_client:
        mock_response = AsyncMock()
        mock_response.raise_for_status = AsyncMock()
        mock_response.json.return_value = MOCK_TASK_RESPONSE

        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            return_value=mock_response
        )

        result = await start_task(url)
        assert result == MOCK_TASK_RESPONSE
        assert result["task_id"] == "123e4567-e89b-12d3-a456-426614174000"


@pytest.mark.asyncio
async def test_start_task_with_email():
    """Test task creation with email"""
    url = "https://example.com"
    email = "test@example.com"

    with patch("httpx.AsyncClient") as mock_client:
        mock_response = AsyncMock()
        mock_response.raise_for_status = AsyncMock()
        mock_response.json.return_value = MOCK_TASK_RESPONSE

        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            return_value=mock_response
        )

        result = await start_task(url, email)
        assert result == MOCK_TASK_RESPONSE


@pytest.mark.asyncio
async def test_start_task_failure():
    """Test task creation failure"""
    url = "https://example.com"

    with patch("httpx.AsyncClient") as mock_client:
        mock_response = AsyncMock()
        mock_response.raise_for_status.side_effect = httpx.HTTPError("API Error")

        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            return_value=mock_response
        )

        with pytest.raises(httpx.HTTPError):
            await start_task(url)


@pytest.mark.asyncio
async def test_get_task_status_success():
    """Test successful task status retrieval"""
    task_id = "123e4567-e89b-12d3-a456-426614174000"

    with patch("httpx.AsyncClient") as mock_client:
        mock_response = AsyncMock()
        mock_response.raise_for_status = AsyncMock()
        mock_response.json.return_value = MOCK_STATUS_RESPONSE

        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=mock_response
        )

        result = await get_task_status(task_id)
        assert result == MOCK_STATUS_RESPONSE
        assert result["status"] == "SUCCESS"


@pytest.mark.asyncio
async def test_get_task_status_failure():
    """Test task status retrieval failure"""
    task_id = "123e4567-e89b-12d3-a456-426614174000"

    with patch("httpx.AsyncClient") as mock_client:
        mock_response = AsyncMock()
        mock_response.raise_for_status.side_effect = httpx.HTTPError("API Error")

        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=mock_response
        )

        with pytest.raises(httpx.HTTPError):
            await get_task_status(task_id)


@pytest.mark.asyncio
async def test_retry_task_success():
    """Test successful task retry"""
    task_id = "123e4567-e89b-12d3-a456-426614174000"

    with patch("httpx.AsyncClient") as mock_client:
        mock_response = AsyncMock()
        mock_response.raise_for_status = AsyncMock()
        mock_response.json.return_value = MOCK_TASK_RESPONSE

        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            return_value=mock_response
        )

        result = await retry_task(task_id)
        assert result == MOCK_TASK_RESPONSE


@pytest.mark.asyncio
async def test_retry_task_failure():
    """Test task retry failure"""
    task_id = "123e4567-e89b-12d3-a456-426614174000"

    with patch("httpx.AsyncClient") as mock_client:
        mock_response = AsyncMock()
        mock_response.raise_for_status.side_effect = httpx.HTTPError("API Error")

        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            return_value=mock_response
        )

        with pytest.raises(httpx.HTTPError):
            await retry_task(task_id)
