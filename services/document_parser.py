#文档解析服务

import os
from pathlib import Path
from typing import Dict, List, Any

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt", ".md"}#集合

def read_text_file_with_fallback(file_path: str) -> str:#-> str:— 返回类型注解,表示该函数返回一个字符串
    """尝试用多种编码读取文本文件"""
    encodings = ["utf-8", "utf-16", "gbk", "gb2312", "cp1252", "latin-1"]
    for encoding in encodings:
        try:#开始一个异常处理块.下面的代码如果抛出指定类型的异常,会被捕获并执行 except 中的代码
            with open(file_path, "r", encoding=encoding) as f:
                content = f.read()
                # 去掉首尾空白字符.如果结果非空（即文件并非全是空白,则认为读取成功,立即返回 内容。
                if content.strip():
                    return content
        except (UnicodeDecodeError, IOError):#编码不匹配/文件读取过程中出现的 I/O 问题
            continue#跳过当前编码，尝试下一种编码
    #如果所有编码都失败了,for 循环正常结束（未被 return 中断），则抛出 ValueError 异常。
    raise ValueError(f"无法读取文件 {file_path}，尝试了编码: {encodings}")


def parse_pdf(file_path: str) -> List[str]:
    """使用 PyPDF2 解析 PDF 文件"""
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        raise ImportError("请安装 PyPDF2: pip install PyPDF2")
    
    pages = []
    with open(file_path, "rb") as f:
        reader = PdfReader(f)
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            if text and text.strip():
                pages.append(text)
    return pages


def parse_docx(file_path: str) -> List[str]:#返回整个文档拼接成 单元素列表;["段落1\n段落2\n段落3..."]
    """使用 python-docx 解析 DOCX 文件"""
    try:
        from docx import Document
    except ImportError:
        raise ImportError("请安装 python-docx: pip install python-docx")
    
    doc = Document(file_path)
    paragraphs = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            paragraphs.append(text)
    return ["\n".join(paragraphs)]

#是整个解析器的入口函数,根据文件类型调用对应的解析函数,并返回解析结果
def parse_document(file_path: str) -> Dict[str, Any]:#返回一个字典，键是字符串，值是任意类型
    """根据文件类型解析文档，返回全文和元数据"""
    path = Path(file_path)
    suffix = path.suffix.lower()#获取文件扩展名,并转换为小写.例如:.pdf,.docx,.txt,.md

    if suffix not in ALLOWED_EXTENSIONS:
        raise ValueError(f"不支持的文件类型: {suffix}，支持的类型: {ALLOWED_EXTENSIONS}")

    if suffix == ".pdf":
        pages = parse_pdf(file_path)#列表,每个元素是一个一页的文本字符串
    elif suffix == ".docx":
        pages = parse_docx(file_path)#列表,整个文档拼接成 单元素列表
    elif suffix == ".txt":
        text = read_text_file_with_fallback(file_path)#一整个字符串,文件内容
        pages = [text]#把 text 塞进一个列表里
    elif suffix == ".md":
        text = read_text_file_with_fallback(file_path)
        pages = [text]
    else:
        pages = []#理论上不会被执行到(因为前面已经做了白名单校验),但保留它作为防御性编程

    full_text = "\n".join(pages)#把 pages 列表中的所有元素用 \n 连接起来,得到一个字符串,作为全文

    #记录文件级别的元信息（文件名、类型、页数、字符数
    metadata = {
        "filename": path.name,
        "file_type": suffix[1:],#字符串切片,去掉扩展名前面的点号
        "total_pages": len(pages),#计算总页数
        "total_chars": len(full_text),#计算总字符数
    }

    return {
        "metadata": metadata,#元信息
        "documents": [{
            "page_content": page, 
            "metadata": {"source": file_path, "page": i}}
            for i, page in enumerate(pages)],#把列表中每个元素包装成一个(索引,值)的元组,每次循环，enumerate 产出一个元组,i, page 自动把元组拆开
        "full_text": full_text,
    }
