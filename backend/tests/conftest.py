"""
pytest配置文件，提供全局fixture
"""

import json
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest


def pytest_addoption(parser):
    """添加命令行选项"""
    parser.addoption(
        "--keep-files",
        action="store_true",
        default=False,
        help="保留测试生成的文件（默认：测试后删除）",
    )
    parser.addoption(
        "--test-url",
        action="store",
        default="https://www.baidu.com",
        help="指定用于PDF转换测试的URL，默认使用百度首页",
    )


@pytest.fixture(scope="session")
def keep_files(request, file_config):
    """是否保留测试生成的文件"""
    return request.config.getoption("--keep-files")


@pytest.fixture(scope="session")
def root_dir():
    """提供项目根目录的绝对路径"""
    # conftest.py位于 backend/tests/，所以根目录是上三级
    return Path(__file__).resolve().parent.parent.parent


@pytest.fixture(scope="session")
def test_config(root_dir):
    """从JSON文件加载测试配置"""
    config_path = root_dir / "backend" / "tests" / "test_config.json"
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def valid_urls(test_config):
    """获取有效的测试URL"""
    return test_config["urls"]["valid"]


@pytest.fixture(scope="session")
def invalid_urls(test_config):
    """获取无效的测试URL"""
    return test_config["urls"]["invalid"]


@pytest.fixture(scope="session")
def email_config(test_config):
    """获取邮件配置，并进行参数名映射"""
    smtp_config = test_config["email"]["smtp"]
    return {
        "smtp_server": smtp_config["server"],
        "smtp_port": smtp_config["port"],
        "smtp_user": smtp_config["user"],
        "smtp_password": smtp_config["password"],
        "sender_email": smtp_config["sender_email"],
    }


@pytest.fixture(scope="session")
def email_test_cases(test_config):
    """获取邮件测试用例"""
    return test_config["email"]["test_cases"]


@pytest.fixture(scope="session")
def file_config(test_config):
    """提供文件配置"""
    return test_config["file"]


@pytest.fixture(scope="session")
def document_config(test_config):
    """提供文档配置"""
    return test_config["document"]


@pytest.fixture(scope="session")
def api_config(test_config):
    """提供API配置"""
    return test_config["api"]


@pytest.fixture(scope="session")
def api_url(api_config):
    """提供完整的API端点URL"""
    return f"{api_config['base_url']}{api_config['process_url_endpoint']}"


@pytest.fixture(scope="function")
def client(monkeypatch):
    """
    提供一个模拟了Celery的TestClient实例。
    通过模拟app.celery_app，防止在测试期间尝试连接Redis。
    """
    monkeypatch.setitem(sys.modules, "app.celery_app", MagicMock())

    from fastapi.testclient import TestClient
    from main import app as fastapi_app

    with TestClient(fastapi_app) as c:
        yield c


@pytest.fixture(scope="function")
def temp_output_dir(file_config, tmp_path):
    """创建一个临时输出目录并进行清理"""
    # 从配置中获取目录名，但总是在一个临时目录内创建它
    output_dir_name = file_config.get("output_dir", "output")
    temp_dir = tmp_path / output_dir_name
    temp_dir.mkdir()
    return temp_dir
