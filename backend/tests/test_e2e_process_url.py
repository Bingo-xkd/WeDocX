import time
from pathlib import Path

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
