"""
邮件服务测试模块
"""

import os
from unittest.mock import MagicMock, patch

import pytest
from app.services.email_service import EmailConfig, EmailService


def test_email_config_validation(email_config):
    """测试邮件配置验证"""
    # 测试完整配置
    config = EmailConfig(**email_config)
    assert config.is_configured is True
    assert config.smtp_server == email_config["smtp_server"]
    assert config.smtp_port == email_config["smtp_port"]
    assert config.smtp_user == email_config["smtp_user"]
    assert config.smtp_password == email_config["smtp_password"]
    assert config.sender_email == email_config["sender_email"]

    # 测试不完整配置
    with pytest.raises(ValueError) as exc_info:
        EmailService(EmailConfig())
    assert "邮件服务配置不完整" in str(exc_info.value)


def test_email_service_initialization(email_config):
    """测试邮件服务初始化"""
    # 测试有效配置
    config = EmailConfig(**email_config)
    service = EmailService(config)
    assert service.config == config

    # 测试无效配置 - 缺少必要参数
    invalid_config = email_config.copy()
    invalid_config["smtp_user"] = ""
    with pytest.raises(ValueError) as exc_info:
        EmailService(EmailConfig(**invalid_config))
    assert "邮件服务配置不完整" in str(exc_info.value)


def test_send_email_validation(email_config, email_test_cases):
    """测试邮件发送参数验证"""
    service = EmailService(EmailConfig(**email_config))

    # 测试无效的收件人邮箱格式
    with pytest.raises(ValueError) as exc_info:
        service.send_email(
            to_email=email_test_cases["invalid"],
            subject="Test Subject",
            body="Test Body",
        )
    assert "无效的邮箱地址" in str(exc_info.value)

    # 测试空主题
    with pytest.raises(ValueError) as exc_info:
        service.send_email(
            to_email=email_test_cases["recipient"], subject="", body="Test Body"
        )
    assert "邮件主题不能为空" in str(exc_info.value)


def _patch_smtp_all():
    """同时 patch smtplib.SMTP 和 smtplib.SMTP_SSL 的装饰器"""
    return patch("smtplib.SMTP"), patch("smtplib.SMTP_SSL")


@patch("smtplib.SMTP")
@patch("smtplib.SMTP_SSL")
def test_send_email_with_attachment(
    mock_smtp_ssl,
    mock_smtp,
    email_config,
    email_test_cases,
    temp_output_dir,
    file_config,
):
    """测试发送带附件的邮件"""
    # 准备测试文件
    test_file = temp_output_dir / "test.txt"
    test_file.write_text(file_config["test_content"]["txt"])

    # 配置 SMTP mock
    mock_smtp_instance = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_smtp_instance
    mock_smtp_ssl.return_value.__enter__.return_value = mock_smtp_instance

    service = EmailService(EmailConfig(**email_config))
    result = service.send_email(
        to_email=email_test_cases["recipient"],
        subject="Test Subject",
        body="Test Body",
        attachments=[str(test_file)],
    )

    # 验证结果
    assert result is True
    assert mock_smtp_instance.login.called
    assert mock_smtp_instance.send_message.called

    # 验证附件处理
    call_args = mock_smtp_instance.send_message.call_args[0][0]
    assert len(call_args.get_payload()) == 2  # 正文 + 1个附件
    assert call_args.get_payload()[1].get_filename() == test_file.name


@patch("smtplib.SMTP")
@patch("smtplib.SMTP_SSL")
def test_send_email_with_nonexistent_attachment(
    mock_smtp_ssl, mock_smtp, email_config, email_test_cases
):
    """测试发送不存在的附件"""
    service = EmailService(EmailConfig(**email_config))

    # 测试不存在的附件
    with pytest.raises(FileNotFoundError) as exc_info:
        service.send_email(
            to_email=email_test_cases["recipient"],
            subject="Test Subject",
            body="Test Body",
            attachments=["nonexistent.pdf"],
        )
    assert "附件文件不存在" in str(exc_info.value)
    assert not mock_smtp.called  # 确保没有尝试发送邮件
    assert not mock_smtp_ssl.called


@patch("smtplib.SMTP")
@patch("smtplib.SMTP_SSL")
def test_send_email_with_html_content(
    mock_smtp_ssl, mock_smtp, email_config, email_test_cases, file_config
):
    """测试发送HTML格式的邮件"""
    # 配置 SMTP mock
    mock_smtp_instance = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_smtp_instance
    mock_smtp_ssl.return_value.__enter__.return_value = mock_smtp_instance

    service = EmailService(EmailConfig(**email_config))
    result = service.send_email(
        to_email=email_test_cases["recipient"],
        subject="Test HTML Email",
        body=file_config["test_content"]["html"],
        body_type="html",
    )

    # 验证结果
    assert result is True
    assert mock_smtp_instance.send_message.called

    # 验证HTML内容
    call_args = mock_smtp_instance.send_message.call_args[0][0]
    assert call_args.get_payload()[0].get_content_type() == "text/html"


@patch("smtplib.SMTP")
@patch("smtplib.SMTP_SSL")
def test_send_email_with_multiple_recipients(
    mock_smtp_ssl, mock_smtp, email_config, email_test_cases
):
    """测试发送给多个收件人"""
    # 配置 SMTP mock
    mock_smtp_instance = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_smtp_instance
    mock_smtp_ssl.return_value.__enter__.return_value = mock_smtp_instance

    service = EmailService(EmailConfig(**email_config))
    recipients = [email_test_cases["recipient"], email_test_cases["sender"]]

    result = service.send_email(
        to_email=recipients, subject="Test Multiple Recipients", body="Test Body"
    )

    # 验证结果
    assert result is True
    assert mock_smtp_instance.send_message.called

    # 验证收件人列表
    call_args = mock_smtp_instance.send_message.call_args[0][0]
    assert all(r in call_args["To"] for r in recipients)


@patch("smtplib.SMTP")
@patch("smtplib.SMTP_SSL")
def test_smtp_connection_error(
    mock_smtp_ssl, mock_smtp, email_config, email_test_cases
):
    """测试SMTP连接错误处理"""
    # 模拟SMTP连接错误
    mock_smtp.side_effect = ConnectionError("Connection refused")
    mock_smtp_ssl.side_effect = ConnectionError("Connection refused")

    service = EmailService(EmailConfig(**email_config))
    with pytest.raises(RuntimeError) as exc_info:
        service.send_email(
            to_email=email_test_cases["recipient"],
            subject="Test Subject",
            body="Test Body",
        )
    assert "发送邮件失败" in str(exc_info.value)
    assert "Connection refused" in str(exc_info.value)
