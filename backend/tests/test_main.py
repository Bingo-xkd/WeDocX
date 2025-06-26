from unittest.mock import MagicMock

import pytest


@pytest.mark.parametrize("url_key", ["simple", "complex"])
def test_process_url_endpoint_success(
    client, monkeypatch, valid_urls, email_test_cases, url_key
):
    """测试 /api/v1/process-url 端点 - 成功场景"""
    # 模拟 chain 的行为
    mock_task_result = MagicMock()
    mock_task_result.id = f"mock-task-id-{url_key}"
    mock_chain = MagicMock()
    mock_chain.return_value.apply_async.return_value = mock_task_result
    monkeypatch.setattr("app.api.endpoints.chain", mock_chain)

    # 准备测试数据
    test_url = valid_urls[url_key]
    test_email = email_test_cases["recipient"]
    data = {"url": test_url, "email": test_email}

    # 发起请求
    response = client.post("/api/v1/process-url", json=data)

    # 断言
    assert response.status_code == 200
    resp_json = response.json()
    assert resp_json["success"] is True
    assert resp_json["task_id"] == f"mock-task-id-{url_key}"
    assert resp_json["pdf_file"].endswith(".pdf")


def test_process_url_endpoint_invalid_payload(client, email_test_cases):
    """测试 /api/v1/process-url 端点 - 无效的请求体"""
    # 无效URL
    data_invalid_url = {
        "url": "not-a-valid-url",
        "email": email_test_cases["recipient"],
    }
    response = client.post("/api/v1/process-url", json=data_invalid_url)
    assert response.status_code == 422  # Unprocessable Entity

    # 无效Email
    data_invalid_email = {"url": "https://example.com", "email": "not-an-email"}
    response = client.post("/api/v1/process-url", json=data_invalid_email)
    assert response.status_code == 422
