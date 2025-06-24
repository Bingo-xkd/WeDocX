from unittest.mock import patch

from app.workers.tasks import create_pdf_task, send_email_task


@patch("app.workers.tasks.url_to_pdf_sync")
def test_create_pdf_task_success(mock_url_to_pdf_sync, valid_urls, temp_output_dir):
    """测试创建PDF任务 - 成功场景"""
    url = valid_urls["simple"]
    filename = "test_task.pdf"
    output_path = temp_output_dir / filename
    mock_url_to_pdf_sync.return_value = str(output_path)

    result = create_pdf_task(url, str(output_path))

    mock_url_to_pdf_sync.assert_called_once_with(url, str(output_path))
    assert result == str(output_path)


@patch("app.workers.tasks.EmailService")
def test_send_email_task_success(mock_email_service, email_test_cases, temp_output_dir):
    """测试发送邮件任务 - 成功场景"""
    service_instance = mock_email_service.return_value
    service_instance.send_email.return_value = True

    to_email = email_test_cases["recipient"]
    subject = email_test_cases["subject"]
    body = email_test_cases["body"]
    attachment_path = temp_output_dir / "attachment.pdf"
    attachment_path.touch()  # 创建一个虚拟附件文件
    pdf_path = str(attachment_path)

    result = send_email_task(pdf_path, to_email, subject, body)

    service_instance.send_email.assert_called_once_with(
        to_email=to_email, subject=subject, body=body, attachments=[pdf_path]
    )
    assert result is True
