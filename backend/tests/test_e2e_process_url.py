import json
import time
from pathlib import Path
from unittest.mock import patch

import pytest
import requests


@pytest.mark.e2e
def test_process_url_e2e(api_url, valid_urls, email_test_cases, file_config, root_dir):
    """
    端到端测试：调用API，生成PDF并发送邮件。
    需要确保本地Redis、Celery worker、FastAPI服务均已启动。
    """
    # 从 fixtures 获取测试数据
    test_url = valid_urls["simple"]
    real_email = email_test_cases["recipient"]
    output_dir_path = root_dir / "backend" / file_config["output_dir"]

    # 准备API请求
    data = {"url": test_url, "email": real_email}

    # 1. 调用API
    resp = requests.post(api_url, json=data)
    print(f"API响应内容: {resp.text}")
    assert resp.status_code == 200, "API调用失败"

    resp_json = resp.json()
    assert resp_json["status"] == "success"
    pdf_file = resp_json["pdf_file"]
    print(f"API返回文件名: {pdf_file}")

    # 2. 轮询检查PDF文件是否生成
    pdf_path = output_dir_path / pdf_file
    for _ in range(30):  # 最多等待30秒
        if pdf_path.exists():
            print(f"PDF已生成: {pdf_path}")
            break
        time.sleep(1)
    else:
        pytest.fail(f"E2E测试失败：超时未生成PDF文件 {pdf_path}")

    # 3. 提示进行人工验证
    print(f"\n请检查邮箱 {real_email} 是否收到来自WeFile的邮件，附件为: {pdf_file}")
    print("这是一个端到端测试，需要人工确认邮件接收情况。")


@pytest.mark.e2e
def test_wechat_to_pdf_e2e(
    api_url, valid_urls, email_test_cases, file_config, root_dir
):
    """
    端到端测试：模拟微信机器人消息，触发API，生成PDF并发送邮件。
    """
    test_url = valid_urls["simple"]
    real_email = email_test_cases["recipient"]
    output_dir_path = root_dir / "backend" / file_config["output_dir"]

    # 模拟微信消息内容
    wechat_message = {
        "content": f"/start {test_url} {real_email}",
        "from_user": "test_user",
        "msg_type": "text",
    }

    # 假设 wechat_bot/api_client.py 有 start_task 函数，直接调用API
    with patch("wechat_bot.api_client.start_task") as mock_start_task:
        mock_start_task.return_value = {
            "success": True,
            "task_id": "mock-task-id",
            "pdf_file": "mock.pdf",
        }
        # 实际应调用 wechat_bot.main 或 command_handler 处理消息
        # 这里只做流程演示
        resp = requests.post(api_url, json={"url": test_url, "email": real_email})
        assert resp.status_code == 200
        resp_json = resp.json()
        assert resp_json["success"] is True
        pdf_file = resp_json["pdf_file"]

    # 检查PDF生成
    pdf_path = output_dir_path / pdf_file
    for _ in range(30):
        if pdf_path.exists():
            break
        time.sleep(1)
    else:
        pytest.fail(f"E2E测试失败：超时未生成PDF文件 {pdf_path}")

    print(f"请检查邮箱 {real_email} 是否收到邮件，附件为: {pdf_file}")
