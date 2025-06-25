"""
API端点单元测试
"""

import json
import os
from unittest.mock import patch, MagicMock
import sys

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from app.core.config import settings

# 加载测试配置
test_config_path = os.path.join(os.path.dirname(__file__), "test_config.json")
with open(test_config_path, "r", encoding="utf-8") as f:
    test_config = json.load(f)

client = TestClient(app)


@pytest.mark.parametrize("url_key", ["simple", "complex"])
def test_process_url_endpoint_success(client, monkeypatch, valid_urls, email_test_cases, url_key):
    """测试 /api/v1/process-url 端点 - 成功场景"""
    # mock chain
    mock_task_result = MagicMock()
    mock_task_result.id = f"mock-task-id-{url_key}"
    mock_chain = MagicMock()
    mock_chain.return_value.apply_async.return_value = mock_task_result
    monkeypatch.setattr("app.api.endpoints.chain", mock_chain)

    data = {"url": valid_urls[url_key], "email": email_test_cases["recipient"]}
    response = client.post("/api/v1/process-url", json=data)
    assert response.status_code == 200
    resp_json = response.json()
    assert resp_json["status"] == "success"
    assert resp_json["task_id"] == f"mock-task-id-{url_key}"
    assert resp_json["pdf_file"].endswith(".pdf")


def test_process_url_endpoint_invalid_payload(client, email_test_cases):
    """测试 /api/v1/process-url 端点 - 无效的请求体"""
    # 无效URL
    data_invalid_url = {"url": "not-a-valid-url", "email": email_test_cases["recipient"]}
    response = client.post("/api/v1/process-url", json=data_invalid_url)
    assert response.status_code == 422
    # 无效Email
    data_invalid_email = {"url": "https://example.com", "email": "not-an-email"}
    response = client.post("/api/v1/process-url", json=data_invalid_email)
    assert response.status_code == 422
    # 缺少字段
    data_missing = {"url": "https://example.com"}
    response = client.post("/api/v1/process-url", json=data_missing)
    assert response.status_code == 422


def test_task_status_endpoint_success(client, monkeypatch):
    """测试 /api/v1/task-status/{task_id} 端点 - 成功场景"""
    mock_result = MagicMock()
    mock_result.status = "SUCCESS"
    mock_result.result = {"pdf_file": "test.pdf", "file_size": 1024}
    monkeypatch.setattr("app.api.endpoints.AsyncResult", lambda tid: mock_result)
    response = client.get("/api/v1/task-status/mock-task-id")
    assert response.status_code == 200
    resp_json = response.json()
    assert resp_json["task_id"] == "mock-task-id"
    assert resp_json["status"] == "SUCCESS"
    assert resp_json["progress"] == 100.0


def test_task_status_endpoint_not_found(client, monkeypatch):
    """测试 /api/v1/task-status/{task_id} 端点 - 任务不存在"""
    monkeypatch.setattr("app.api.endpoints.AsyncResult", lambda tid: None)
    response = client.get("/api/v1/task-status/not-exist-id")
    assert response.status_code == 404


def test_retry_task_endpoint_success(client, monkeypatch):
    """测试 /api/v1/retry-task 端点 - 成功场景"""
    mock_result = MagicMock()
    mock_result.status = "FAILURE"
    monkeypatch.setattr("app.api.endpoints.AsyncResult", lambda tid: mock_result)
    data = {"task_id": "mock-task-id"}
    response = client.post("/api/v1/retry-task", json=data)
    assert response.status_code == 200
    resp_json = response.json()
    assert resp_json["success"] is True
    assert resp_json["task_id"] == "mock-task-id"


def test_retry_task_endpoint_not_found(client, monkeypatch):
    """测试 /api/v1/retry-task 端点 - 任务不存在"""
    monkeypatch.setattr("app.api.endpoints.AsyncResult", lambda tid: None)
    data = {"task_id": "not-exist-id"}
    response = client.post("/api/v1/retry-task", json=data)
    assert response.status_code == 404


def test_retry_task_endpoint_invalid_status(client, monkeypatch):
    """测试 /api/v1/retry-task 端点 - 非FAILURE状态不可重试"""
    mock_result = MagicMock()
    mock_result.status = "SUCCESS"
    monkeypatch.setattr("app.api.endpoints.AsyncResult", lambda tid: mock_result)
    data = {"task_id": "mock-task-id"}
    response = client.post("/api/v1/retry-task", json=data)
    assert response.status_code == 400


def test_health_check_endpoint(client):
    """测试 /api/v1/health 端点"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "0.2.0"
    assert data["environment"] == "development"


class TestRootEndpoint:
    """根端点测试"""
    
    def test_root_endpoint(self):
        """测试根端点"""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "ok"
        assert "Welcome to WeDocX API" in data["message"]
        assert data["version"] == "0.2.0" 