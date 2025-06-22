import asyncio
from playwright.async_api import async_playwright
import os
from datetime import datetime
import re
from typing import Optional

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../output'))
os.makedirs(OUTPUT_DIR, exist_ok=True)

def sanitize_filename(name: str) -> str:
    # 移除非法字符，保留中英文、数字、下划线、短横线
    return re.sub(r'[^\w\u4e00-\u9fa5-]', '', name)

async def url_to_pdf(
    url: str,
    filename: str = None,
    save_word: bool = False,
    save_txt: bool = False,
    word_saver: Optional[callable] = None,
    txt_saver: Optional[callable] = None
) -> str:
    """
    使用Playwright将指定URL页面渲染为PDF，保存到本地output目录。
    可选：通过参数控制是否额外保存word和txt文件，文件名与pdf一致。
    :param url: 需要转换的网页链接
    :param filename: 可选，指定PDF文件名
    :param save_word: 是否保存为word
    :param save_txt: 是否保存为txt
    :param word_saver: 负责保存word的外部函数，签名(word_path, html, title)
    :param txt_saver: 负责保存txt的外部函数，签名(txt_path, text, title)
    :return: PDF文件的绝对路径
    """
    now_str = datetime.now().strftime('%Y%m%d-%H-%M')
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(url, timeout=10000, wait_until="domcontentloaded")
            # 获取页面标题
            title = await page.title()
            if title:
                title = sanitize_filename(title.strip())[:10]
                pdf_filename = f"{now_str}-{title}.pdf"
            else:
                pdf_filename = f"{now_str}.pdf"
            if filename:
                pdf_filename = filename
            pdf_path = os.path.join(OUTPUT_DIR, pdf_filename)
            # 分段滚动页面，确保所有图片都进入可视区域
            await page.evaluate("""
                async () => {
                    const scrollStep = window.innerHeight / 2;
                    const scrollHeight = document.body.scrollHeight;
                    let pos = 0;
                    while (pos < scrollHeight) {
                        window.scrollTo(0, pos);
                        await new Promise(r => setTimeout(r, 100));
                        pos += scrollStep;
                    }
                    window.scrollTo(0, document.body.scrollHeight);
                    await new Promise(r => setTimeout(r, 1000));
                }
            """)
            # 等待所有图片加载完成
            await page.evaluate("""
                () => {
                    return Promise.all(Array.from(document.images).map(img => {
                        if (img.complete) return true;
                        return new Promise(resolve => {
                            img.onload = img.onerror = resolve;
                        });
                    }));
                }
            """)
            # 生成PDF
            await page.pdf(path=pdf_path, format="A4")
            # 额外保存word和txt
            if save_word and word_saver:
                html = await page.content()
                word_path = pdf_path.replace('.pdf', '.docx')
                word_saver(word_path, html, title or "")
            if save_txt and txt_saver:
                text = await page.inner_text('body')
                txt_path = pdf_path.replace('.pdf', '.txt')
                txt_saver(txt_path, text, title or "")
            await browser.close()
        return pdf_path
    except Exception as e:
        raise RuntimeError(f"PDF转换失败: {e}")

# 用于同步调用的包装
def url_to_pdf_sync(url: str, filename: str = None, save_word=False, save_txt=False, word_saver=None, txt_saver=None) -> str:
    return asyncio.run(url_to_pdf(url, filename, save_word, save_txt, word_saver, txt_saver)) 