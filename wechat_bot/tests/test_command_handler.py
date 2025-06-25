"""
Unit tests for wechat_bot/command_handler.py
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from wechaty.user import Message

from wechat_bot.command_handler import handle_start, handle_status, poll_task_status

# Mock responses
MOCK_TASK_RESPONSE = {
    "task_id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "PENDING"
}

MOCK_STATUS_RESPONSE = {
    "task_id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "SUCCESS",
    "result": "path/to/file.pdf"
}

@pytest.fixture
def mock_message():
    """Create a mock Message object"""
    message = AsyncMock(spec=Message)
    message.say = AsyncMock()
    return message

@pytest.mark.asyncio
async def test_handle_start_success(mock_message):
    """Test successful start command handling"""
    url = "https://example.com"
    
    with patch("wechat_bot.command_handler.start_task") as mock_start_task, \
         patch("wechat_bot.command_handler.asyncio.create_task") as mock_create_task:
        
        mock_start_task.return_value = MOCK_TASK_RESPONSE
        
        await handle_start(mock_message, url)
        
        mock_start_task.assert_called_once_with(url)
        mock_message.say.assert_called_once()
        mock_create_task.assert_called_once()

@pytest.mark.asyncio
async def test_handle_start_invalid_url(mock_message):
    """Test start command with invalid URL"""
    url = "invalid-url"
    
    await handle_start(mock_message, url)
    mock_message.say.assert_called_once_with("Please provide a valid URL.")

@pytest.mark.asyncio
async def test_handle_start_api_error(mock_message):
    """Test start command with API error"""
    url = "https://example.com"
    
    with patch("wechat_bot.command_handler.start_task") as mock_start_task:
        mock_start_task.side_effect = Exception("API Error")
        
        await handle_start(mock_message, url)
        
        mock_message.say.assert_called_once()
        assert "Error starting task" in mock_message.say.call_args[0][0]

@pytest.mark.asyncio
async def test_handle_status_success(mock_message):
    """Test successful status command handling"""
    task_id = "123e4567-e89b-12d3-a456-426614174000"
    
    with patch("wechat_bot.command_handler.get_task_status") as mock_get_status:
        mock_get_status.return_value = MOCK_STATUS_RESPONSE
        
        await handle_status(mock_message, task_id)
        
        mock_get_status.assert_called_once_with(task_id)
        mock_message.say.assert_called_once()
        assert "SUCCESS" in mock_message.say.call_args[0][0]

@pytest.mark.asyncio
async def test_handle_status_invalid_task_id(mock_message):
    """Test status command with invalid task ID"""
    task_id = "invalid-id"
    
    await handle_status(mock_message, task_id)
    mock_message.say.assert_called_once_with("Please provide a valid task ID.")

@pytest.mark.asyncio
async def test_handle_status_api_error(mock_message):
    """Test status command with API error"""
    task_id = "123e4567-e89b-12d3-a456-426614174000"
    
    with patch("wechat_bot.command_handler.get_task_status") as mock_get_status:
        mock_get_status.side_effect = Exception("API Error")
        
        await handle_status(mock_message, task_id)
        
        mock_message.say.assert_called_once()
        assert "Error checking status" in mock_message.say.call_args[0][0]

@pytest.mark.asyncio
async def test_poll_task_status_success(mock_message):
    """Test successful task status polling"""
    task_id = "123e4567-e89b-12d3-a456-426614174000"
    
    with patch("wechat_bot.command_handler.get_task_status") as mock_get_status, \
         patch("wechat_bot.command_handler.asyncio.sleep", return_value=None):
        
        # First call returns PENDING, second call returns SUCCESS
        mock_get_status.side_effect = [
            {"status": "PENDING"},
            {"status": "SUCCESS", "result": "path/to/file.pdf"}
        ]
        
        await poll_task_status(mock_message, task_id)
        
        assert mock_get_status.call_count == 2
        assert mock_message.say.call_count == 1
        assert "completed successfully" in mock_message.say.call_args[0][0]

@pytest.mark.asyncio
async def test_poll_task_status_failure(mock_message):
    """Test task status polling with failure"""
    task_id = "123e4567-e89b-12d3-a456-426614174000"
    
    with patch("wechat_bot.command_handler.get_task_status") as mock_get_status, \
         patch("wechat_bot.command_handler.asyncio.sleep", return_value=None):
        
        mock_get_status.side_effect = [
            {"status": "PENDING"},
            {"status": "FAILURE", "details": "Error occurred"}
        ]
        
        await poll_task_status(mock_message, task_id)
        
        assert mock_get_status.call_count == 2
        assert mock_message.say.call_count == 1
        assert "failed" in mock_message.say.call_args[0][0]

@pytest.mark.asyncio
async def test_poll_task_status_api_error(mock_message):
    """Test task status polling with API error"""
    task_id = "123e4567-e89b-12d3-a456-426614174000"
    
    with patch("wechat_bot.command_handler.get_task_status") as mock_get_status:
        mock_get_status.side_effect = Exception("API Error")
        
        await poll_task_status(mock_message, task_id)
        
        mock_message.say.assert_called_once()
        assert "Error polling status" in mock_message.say.call_args[0][0] 