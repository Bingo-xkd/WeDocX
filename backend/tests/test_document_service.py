"""文档服务测试模块"""

from app.services.document_service import convert_html_to_docx, convert_html_to_txt


def test_convert_html_to_txt(file_config, temp_output_dir):
    """测试HTML转TXT功能"""
    html_content = file_config["test_content"]["html"]
    filename = "test.txt"
    output_path = temp_output_dir / filename
    test_title = "Test Document Title"

    convert_html_to_txt(html_content, str(output_path), title=test_title)

    assert output_path.exists()
    content = output_path.read_text(encoding="utf-8")
    assert test_title in content
    assert "Test HTML" in content


def test_convert_html_to_docx(file_config, temp_output_dir):
    """测试HTML转DOCX功能"""
    html_content = file_config["test_content"]["html"]
    filename = "test.docx"
    output_path = temp_output_dir / filename
    test_title = "Test Document Title"

    convert_html_to_docx(html_content, str(output_path), title=test_title)

    assert output_path.exists()
    assert output_path.stat().st_size > 0  # 确保文件不为空
