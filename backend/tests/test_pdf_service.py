"""
PDF服务测试模块
"""

import os

import pytest
from app.services.pdf_service import url_to_pdf_sync, url_to_txt_sync, url_to_word_sync


def clean_file(file_path: str, keep_files: bool = False):
    """清理文件的辅助函数"""
    if not keep_files and os.path.exists(file_path):
        os.remove(file_path)


def test_url_to_pdf_sync_success(valid_urls, temp_output_dir, keep_files):
    """测试URL转PDF功能 - 成功场景"""
    url = valid_urls["simple"]
    pdf_path = url_to_pdf_sync(url)
    assert os.path.exists(pdf_path)
    assert pdf_path.endswith(".pdf")
    clean_file(pdf_path, keep_files)


def test_url_to_word_sync_success(valid_urls, temp_output_dir, keep_files):
    """测试URL转Word功能 - 成功场景"""
    url = valid_urls["simple"]
    word_path = url_to_word_sync(url)
    assert os.path.exists(word_path)
    assert word_path.endswith(".docx")
    clean_file(word_path, keep_files)


def test_url_to_txt_sync_success(valid_urls, temp_output_dir, keep_files):
    """测试URL转TXT功能 - 成功场景"""
    url = valid_urls["simple"]
    txt_path = url_to_txt_sync(url)
    assert os.path.exists(txt_path)
    assert txt_path.endswith(".txt")
    clean_file(txt_path, keep_files)


@pytest.mark.parametrize("url_key", ["malformed", "nonexistent", "wrong_protocol"])
def test_url_conversion_with_invalid_urls(invalid_urls, url_key):
    """测试无效URL的异常处理"""
    url = invalid_urls[url_key]
    with pytest.raises(RuntimeError):
        url_to_pdf_sync(url)
    with pytest.raises(RuntimeError):
        url_to_word_sync(url)
    with pytest.raises(RuntimeError):
        url_to_txt_sync(url)


def test_custom_filename(valid_urls, file_config, temp_output_dir, keep_files):
    """测试自定义文件名功能"""
    url = valid_urls["simple"]
    custom_names = file_config["custom_names"]

    # 测试PDF自定义文件名
    pdf_path = url_to_pdf_sync(url, filename=custom_names["pdf"])
    assert os.path.basename(pdf_path) == custom_names["pdf"]
    clean_file(pdf_path, keep_files)

    # 测试Word自定义文件名
    word_path = url_to_word_sync(url, filename=custom_names["docx"])
    assert os.path.basename(word_path) == custom_names["docx"]
    clean_file(word_path, keep_files)

    # 测试TXT自定义文件名
    txt_path = url_to_txt_sync(url, filename=custom_names["txt"])
    assert os.path.basename(txt_path) == custom_names["txt"]
    clean_file(txt_path, keep_files)


def test_complex_webpage_conversion(valid_urls, temp_output_dir, keep_files):
    """测试复杂网页的转换"""
    url = valid_urls["complex"]

    # 测试PDF转换
    pdf_path = url_to_pdf_sync(url)
    assert os.path.exists(pdf_path)
    assert os.path.getsize(pdf_path) > 0
    clean_file(pdf_path, keep_files)

    # 测试Word转换
    word_path = url_to_word_sync(url)
    assert os.path.exists(word_path)
    assert os.path.getsize(word_path) > 0
    clean_file(word_path, keep_files)

    # 测试TXT转换
    txt_path = url_to_txt_sync(url)
    assert os.path.exists(txt_path)
    assert os.path.getsize(txt_path) > 0
    clean_file(txt_path, keep_files)
