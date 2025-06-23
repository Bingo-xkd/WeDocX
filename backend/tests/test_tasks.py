from unittest.mock import MagicMock, patch

import pytest
from app.workers.tasks import create_pdf_task, send_email_task


@patch("app.workers.tasks.url_to_pdf_sync")
def test_create_pdf_task(mock_url_to_pdf_sync):
    # mock url_to_pdf_sync
    mock_url_to_pdf_sync.return_value = None
    url = "http://example.com"
    output_path = "/tmp/test.pdf"
    result = create_pdf_task(url, output_path)
    mock_url_to_pdf_sync.assert_called_once_with(url, output_path)
    assert result == output_path


@patch("app.workers.tasks.EmailService")
@patch("app.workers.tasks.EmailConfig")
def test_send_email_task(mock_email_config, mock_email_service):
    # mock EmailService.send_email
    service_instance = mock_email_service.return_value
    service_instance.send_email.return_value = True
    to_email = "test@example.com"
    subject = "Test Subject"
    body = "Test Body"
    attachments = ["/tmp/test.pdf"]
    result = send_email_task(to_email, subject, body, attachments)
    service_instance.send_email.assert_called_once_with(
        to_email=to_email, subject=subject, body=body, attachments=attachments
    )
    assert result is True
