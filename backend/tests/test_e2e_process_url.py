import json
import os
import time

import pytest
import requests

API_URL = "http://127.0.0.1:8000/api/v1/process-url"
OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../output"))
CONFIG_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "test_config.json")
)


@pytest.mark.e2e
def test_process_url_e2e():
    """
    端到端测试：调用API，生成PDF并发送邮件
    需确保本地Redis、Celery worker、FastAPI服务均已启动
    所有输入变量均通过test_config.json传入
    """
    # 读取配置
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)
    test_url = config["urls"]["valid"]["simple"]
    real_email = config["email"]["test_cases"]["recipient"]

    data = {"url": test_url, "email": real_email}
    # 1. 调用API
    resp = requests.post(API_URL, json=data)
    print("API响应内容：", resp.text)
    assert resp.status_code == 200
    resp_json = resp.json()
    assert resp_json["status"] == "success"
    task_id = resp_json["task_id"]
    pdf_file = resp_json["pdf_file"]
    print(f"API返回任务ID: {task_id}, PDF文件名: {pdf_file}")

    # 2. 轮询output目录，等待PDF生成
    pdf_path = os.path.join(OUTPUT_DIR, pdf_file)
    for _ in range(30):  # 最多等待30秒
        if os.path.exists(pdf_path):
            print(f"PDF已生成: {pdf_path}")
            break
        time.sleep(1)
    else:
        pytest.fail(f"超时未生成PDF: {pdf_path}")

    # 3. 提示用户检查邮箱
    print(
        f"请检查邮箱 {real_email} 是否收到主题为'网页转PDF'的邮件，附件为: {pdf_file}"
    )
    # 这里可人工辅助验证邮件送达
