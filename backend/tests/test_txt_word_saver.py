import os
from app.services.txt_word_saver import save_as_txt, save_as_docx

def test_save_as_txt(tmp_path):
    txt_path = tmp_path / "test.txt"
    title = "测试标题"
    text = "这是正文内容。"
    save_as_txt(str(txt_path), text, title)
    assert txt_path.exists()
    content = txt_path.read_text(encoding="utf-8")
    assert title in content
    assert text in content


def test_save_as_docx(tmp_path):
    docx_path = tmp_path / "test.docx"
    title = "文档标题"
    html = """
    <html><body>
        <h1>一级标题</h1>
        <h2>二级标题</h2>
        <p>第一段内容。</p>
        <p>第二段内容。</p>
    </body></html>
    """
    save_as_docx(str(docx_path), html, title)
    assert docx_path.exists()
    # 进一步内容校验可用python-docx读取内容
    from docx import Document
    doc = Document(str(docx_path))
    all_text = "\n".join([p.text for p in doc.paragraphs])
    assert "一级标题" in all_text
    assert "第一段内容。" in all_text
    assert title in all_text 