import requests
import re
import os

def get_cct_and_contentkey(url):
    # 1. 配置请求参数（替换为目标网页的URL）
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36 Edg/148.0.0.0'
    }

    # 2. 获取网页源码
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # 抛出HTTP请求异常
        response.encoding = response.apparent_encoding  # 自动识别编码
        html = response.text
    except Exception as e:
        print(f"获取网页失败：{e}")
        exit()

    # 3. 正则匹配 cct 和 contentKey 的值
    # 正则模式：匹配 var 变量名 = '值'; （允许空格、换行等）
    pattern_cct = re.compile(r"var\s+cct\s+=\s+'(.*?)';", re.S)
    pattern_contentKey = re.compile(r"var\s+contentKey\s+=\s+'(.*?)';", re.S)

    # 提取值
    cct_value = pattern_cct.search(html).group(1) if pattern_cct.search(html) else None
    contentKey_value = pattern_contentKey.search(html).group(1) if pattern_contentKey.search(html) else None

    comic_title = "未知漫画"
    chapter_name = "未知章节"
    pattern_header = re.compile(r'<h4 class="header">\s*(.+?)\s*</h4>', re.S)
    header_match = pattern_header.search(html)
    
    if header_match:
        full_name = header_match.group(1).strip()
        # 拆分漫画名和章节名（按 / 分割）
        if "/" in full_name:
            comic_title, chapter_name = full_name.split("/", 1)  # 只分割一次
        else:
            comic_title = full_name

    # 清理非法字符（Windows文件夹禁止字符）
    illegal_chars = r'[\\/:*?"<>|]'
    comic_title = re.sub(illegal_chars, '_', comic_title.strip())
    chapter_name = re.sub(illegal_chars, '_', chapter_name.strip())

    return cct_value, contentKey_value, comic_title, chapter_name