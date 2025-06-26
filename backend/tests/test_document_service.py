"""文档服务测试模块"""

import os
import shutil
import tempfile

import pytest
from app.services.document_service import convert_html_to_docx, convert_html_to_txt
from app.services.pdf_service import (
    OUTPUT_DIR,
    backup_output_dir,
    cleanup_file,
    restore_output_dir,
)


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


def test_cleanup_file(temp_output_dir):
    # 创建临时文件
    file_path = temp_output_dir / "test_cleanup.pdf"
    file_path.write_text("test")
    assert file_path.exists()
    # 清理
    ok = cleanup_file(str(file_path))
    assert ok
    assert not file_path.exists()


def test_backup_and_restore_output_dir(temp_output_dir):
    # 在output目录创建测试文件
    test_file = temp_output_dir / "test_backup.pdf"
    test_file.write_text("backup-test")
    backup_dir = tempfile.mkdtemp()
    # 备份
    backup_path = backup_output_dir(backup_dir)
    assert os.path.exists(backup_path)
    # 删除output内容
    shutil.rmtree(temp_output_dir)
    os.makedirs(temp_output_dir)
    # 恢复
    ok = restore_output_dir(backup_path)
    assert ok
    # 恢复后文件应存在
    restored_file = os.path.join(OUTPUT_DIR, "test_backup.pdf")
    assert os.path.exists(restored_file)
    # 清理备份
    shutil.rmtree(backup_path)
    shutil.rmtree(backup_dir)
