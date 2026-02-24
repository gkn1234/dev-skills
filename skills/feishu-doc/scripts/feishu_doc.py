#!/usr/bin/env python3
"""
飞书文档读取工具
将飞书文档转换为 Markdown 并下载图片
"""

import os
import re
import sys
import json
import requests
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse, unquote

CACHE_DIR = Path.home() / ".cache" / "feishu-docs"


def get_env_config() -> tuple[Optional[str], Optional[str]]:
    """获取环境变量配置"""
    app_id = os.environ.get("FEISHU_APP_ID")
    app_secret = os.environ.get("FEISHU_APP_SECRET")
    return app_id, app_secret


def get_token(app_id: str, app_secret: str) -> str:
    """获取 tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    resp = requests.post(url, json={
        "app_id": app_id,
        "app_secret": app_secret
    })
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 0:
        raise Exception(f"获取 token 失败: {data.get('msg')}")
    return data["tenant_access_token"]


def parse_url(url: str) -> tuple[str, str]:
    """
    解析飞书链接，提取 doc_token 和文档类型
    支持格式:
    - https://xxx.feishu.cn/docx/Abc123
    - https://xxx.feishu.cn/docs/Abc123
    - https://xxx.feishu.cn/wiki/Abc123
    """
    parsed = urlparse(url)
    path_parts = parsed.path.strip("/").split("/")

    if len(path_parts) >= 2:
        doc_type = path_parts[0]  # docx, docs, wiki
        doc_token = path_parts[1].split("?")[0]  # 移除查询参数
        return doc_token, doc_type

    raise ValueError(f"无法解析飞书链接: {url}")


def fetch_blocks(doc_token: str, token: str, page_token: str = None) -> tuple[list, Optional[str]]:
    """获取文档所有 blocks，支持分页"""
    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"page_size": 500}
    if page_token:
        params["page_token"] = page_token

    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()

    if data.get("code") != 0:
        raise Exception(f"获取文档失败: {data.get('msg')}")

    blocks = data.get("data", {}).get("items", [])
    next_page = data.get("data", {}).get("page_token")
    return blocks, next_page


def fetch_all_blocks(doc_token: str, token: str) -> list:
    """获取文档所有 blocks（处理分页）"""
    all_blocks = []
    page_token = None

    while True:
        blocks, next_page = fetch_blocks(doc_token, token, page_token)
        all_blocks.extend(blocks)
        if not next_page:
            break
        page_token = next_page

    return all_blocks


def get_document_info(doc_token: str, token: str) -> dict:
    """获取文档基本信息"""
    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}"
    headers = {"Authorization": f"Bearer {token}"}

    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    if data.get("code") != 0:
        raise Exception(f"获取文档信息失败: {data.get('msg')}")

    return data.get("data", {}).get("document", {})


def download_image(file_token: str, token: str, output_dir: Path) -> str:
    """下载图片，返回本地文件名"""
    # 先获取临时下载链接
    url = "https://open.feishu.cn/open-apis/drive/v1/medias/batch_get_tmp_download_url"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"file_tokens": file_token}

    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()

    if data.get("code") != 0:
        raise Exception(f"获取图片链接失败: {data.get('msg')}")

    tmp_urls = data.get("data", {}).get("tmp_download_urls", [])
    if not tmp_urls:
        raise Exception(f"未找到图片: {file_token}")

    download_url = tmp_urls[0].get("tmp_download_url")

    # 下载图片
    img_resp = requests.get(download_url)
    img_resp.raise_for_status()

    # 从 Content-Type 确定扩展名
    content_type = img_resp.headers.get("Content-Type", "image/png")
    ext_map = {
        "image/png": ".png",
        "image/jpeg": ".jpg",
        "image/gif": ".gif",
        "image/webp": ".webp",
    }
    ext = ext_map.get(content_type, ".png")

    # 保存文件
    filename = f"{file_token}{ext}"
    filepath = output_dir / filename
    filepath.write_bytes(img_resp.content)

    return filename


def process_blocks(blocks: list, output_dir: Path, token: str) -> tuple[list, list]:
    """
    处理 blocks：下载图片，提取文档链接
    返回: (downloaded_images, referenced_docs)
    """
    images = []
    doc_links = []
    assets_dir = output_dir / "assets"

    for block in blocks:
        block_type = block.get("block_type")

        # 下载图片
        if block_type == 27:  # image
            image_data = block.get("image", {})
            file_token = image_data.get("token", "")
            if file_token:
                try:
                    assets_dir.mkdir(parents=True, exist_ok=True)
                    filename = download_image(file_token, token, assets_dir)
                    images.append(filename)
                    # 在 block 中添加本地路径
                    block["image"]["local_path"] = f"./assets/{filename}"
                except Exception as e:
                    block["image"]["download_error"] = str(e)

        # 提取文档链接
        type_key_map = {
            2: "text", 3: "heading1", 4: "heading2", 5: "heading3",
            6: "heading4", 7: "heading5", 8: "heading6", 9: "heading7",
            10: "heading8", 11: "heading9", 12: "bullet", 13: "ordered",
            15: "quote", 17: "todo"
        }

        if block_type in type_key_map:
            text_data = block.get(type_key_map[block_type], {})
            elements = text_data.get("elements", [])
            for elem in elements:
                if "mention_doc" in elem:
                    mention = elem["mention_doc"]
                    title = mention.get("title", "文档链接")
                    url = mention.get("url", "")
                    if url and url not in [d["url"] for d in doc_links]:
                        doc_links.append({"title": title, "url": url})

    return images, doc_links


# 飞书代码块语言枚举 -> Markdown 语言标识
LANG_MAP = {
    1: "", 2: "abap", 3: "ada", 4: "apache", 5: "apex",
    6: "asm", 7: "bash", 8: "csharp", 9: "cpp", 10: "c",
    11: "cobol", 12: "css", 13: "coffeescript", 14: "d", 15: "dart",
    16: "delphi", 17: "django", 18: "dockerfile", 19: "erlang", 20: "fortran",
    21: "foxpro", 22: "go", 23: "groovy", 24: "html", 25: "handlebars",
    26: "http", 27: "haskell", 28: "json", 29: "java", 30: "javascript",
    31: "julia", 32: "kotlin", 33: "latex", 34: "lisp", 35: "logo",
    36: "lua", 37: "matlab", 38: "makefile", 39: "markdown", 40: "nginx",
    41: "objectivec", 42: "openedgeabl", 43: "php", 44: "perl",
    45: "postscript", 46: "powershell", 47: "prolog", 48: "protobuf",
    49: "python", 50: "r", 51: "rpg", 52: "ruby", 53: "rust",
    54: "sas", 55: "scss", 56: "sql", 57: "scala", 58: "scheme",
    59: "scratch", 60: "shell", 61: "swift", 62: "thrift",
    63: "typescript", 64: "vbscript", 65: "vb", 66: "xml", 67: "yaml",
}

# block_type -> block 数据的 key 名
TYPE_KEY_MAP = {
    2: "text", 3: "heading1", 4: "heading2", 5: "heading3",
    6: "heading4", 7: "heading5", 8: "heading6", 9: "heading7",
    10: "heading8", 11: "heading9", 12: "bullet", 13: "ordered",
    14: "code", 15: "quote", 17: "todo",
}


def render_elements(elements: list) -> str:
    """将 block 内的 elements 数组渲染为 Markdown 文本"""
    parts = []
    for elem in elements:
        if "text_run" in elem:
            tr = elem["text_run"]
            text = tr.get("content", "")
            style = tr.get("text_element_style", {})

            # 应用行内样式
            if style.get("inline_code"):
                text = f"`{text}`"
            else:
                if style.get("bold"):
                    text = f"**{text}**"
                if style.get("italic"):
                    text = f"*{text}*"
                if style.get("strikethrough"):
                    text = f"~~{text}~~"
                if style.get("underline"):
                    text = f"<u>{text}</u>"

            # 链接
            link = style.get("link", {})
            url = link.get("url", "") if link else ""
            if url:
                url = unquote(url)
                text = f"[{tr.get('content', '')}]({url})"

            parts.append(text)

        elif "mention_doc" in elem:
            mention = elem["mention_doc"]
            title = mention.get("title", "文档链接")
            url = mention.get("url", "")
            if url:
                parts.append(f"[{title}]({url})")
            else:
                parts.append(title)

        elif "equation" in elem:
            content = elem["equation"].get("content", "")
            parts.append(f"${content}$")

    return "".join(parts)


def fetch_sheet_data(sheet_token: str, token: str) -> str:
    """获取嵌入表格数据并转为 Markdown 表格"""
    # sheet_token 格式: {spreadsheetToken}_{sheetId}
    parts = sheet_token.rsplit("_", 1)
    if len(parts) != 2:
        return f"[嵌入表格: token 格式异常 - {sheet_token}]"

    spreadsheet_token, sheet_id = parts
    headers = {"Authorization": f"Bearer {token}"}

    # 获取表格数据
    url = f"https://open.feishu.cn/open-apis/sheets/v2/spreadsheets/{spreadsheet_token}/values/{sheet_id}"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    if data.get("code") != 0:
        return f"[嵌入表格: 获取失败 - {data.get('msg')}]"

    values = data.get("data", {}).get("valueRange", {}).get("values", [])
    if not values:
        return "[嵌入表格: 空表格]"

    # 转为 Markdown 表格
    lines = []
    # 表头
    header = values[0]
    header_cells = [str(c) if c is not None else "" for c in header]
    lines.append("| " + " | ".join(header_cells) + " |")
    lines.append("| " + " | ".join(["---"] * len(header_cells)) + " |")
    # 数据行
    for row in values[1:]:
        cells = [str(c) if c is not None else "" for c in row]
        # 补齐列数
        while len(cells) < len(header_cells):
            cells.append("")
        lines.append("| " + " | ".join(cells) + " |")

    return "\n".join(lines)


def blocks_to_markdown(blocks: list, token: str) -> str:
    """将飞书 blocks 转换为 Markdown"""
    # 构建 block_id -> block 映射
    block_map = {b["block_id"]: b for b in blocks if "block_id" in b}

    # 找到根节点 id，只渲染 parent_id == root_id 的 block
    root_id = blocks[0]["block_id"] if blocks else ""

    lines = []
    for block in blocks:
        if block.get("block_type") == 1:
            continue
        if block.get("parent_id") != root_id:
            continue
        _render_block(block, block_map, token, lines)

    return "\n".join(lines)


def _render_block(block: dict, block_map: dict, token: str, lines: list):
    """渲染单个 block 到 lines 列表"""
    bt = block.get("block_type")

    # 跳过根节点和表格单元格（由表格处理）
    if bt in (1, 32):
        return

    # 标题
    if 3 <= bt <= 11:
        level = min(bt - 2, 6)
        key = TYPE_KEY_MAP.get(bt, "")
        if key:
            text = render_elements(block.get(key, {}).get("elements", []))
            lines.append(f"{'#' * level} {text}")
            lines.append("")
        return

    # 普通文本
    if bt == 2:
        text = render_elements(block.get("text", {}).get("elements", []))
        lines.append(text)
        lines.append("")
        return

    # 无序列表
    if bt == 12:
        text = render_elements(block.get("bullet", {}).get("elements", []))
        lines.append(f"- {text}")
        return

    # 有序列表
    if bt == 13:
        text = render_elements(block.get("ordered", {}).get("elements", []))
        lines.append(f"1. {text}")
        return

    # 代码块
    if bt == 14:
        code_data = block.get("code", {})
        lang_id = code_data.get("style", {}).get("language", 1)
        lang = LANG_MAP.get(lang_id, "")
        content = render_elements(code_data.get("elements", []))
        lines.append(f"```{lang}")
        lines.append(content)
        lines.append("```")
        lines.append("")
        return

    # 引用（单行）
    if bt == 15:
        text = render_elements(block.get("quote", {}).get("elements", []))
        lines.append(f"> {text}")
        lines.append("")
        return

    # Todo
    if bt == 17:
        todo_data = block.get("todo", {})
        text = render_elements(todo_data.get("elements", []))
        done = todo_data.get("style", {}).get("done", False)
        checkbox = "[x]" if done else "[ ]"
        lines.append(f"- {checkbox} {text}")
        return

    # 分割线
    if bt == 22:
        lines.append("---")
        lines.append("")
        return

    # 图片
    if bt == 27:
        image_data = block.get("image", {})
        local_path = image_data.get("local_path", "")
        if local_path:
            lines.append(f"![image]({local_path})")
        elif image_data.get("download_error"):
            lines.append(f"[图片加载失败: {image_data['download_error']}]")
        else:
            lines.append("[图片]")
        lines.append("")
        return

    # 嵌入表格（sheet）
    if bt == 30:
        sheet_data = block.get("sheet", {})
        st = sheet_data.get("token", "")
        if st:
            try:
                lines.append(fetch_sheet_data(st, token))
            except Exception as e:
                lines.append(f"[嵌入表格: 获取失败 - {e}]")
        else:
            lines.append("[嵌入表格: 无 token]")
        lines.append("")
        return

    # 文档内表格
    if bt == 31:
        _render_table(block, block_map, token, lines)
        return

    # 引用容器（多行引用）
    if bt == 34:
        child_lines = []
        for cid in block.get("children", []):
            child = block_map.get(cid)
            if child:
                _render_block(child, block_map, token, child_lines)
        for cl in child_lines:
            lines.append(f"> {cl}" if cl else ">")
        lines.append("")
        return

    # 高亮块（callout）
    if bt == 19:
        emoji = block.get("callout", {}).get("emoji_id", "")
        prefix = f"> {emoji} " if emoji else "> "
        child_lines = []
        for cid in block.get("children", []):
            child = block_map.get(cid)
            if child:
                _render_block(child, block_map, token, child_lines)
        for i, cl in enumerate(child_lines):
            if i == 0 and emoji:
                lines.append(f"{prefix}{cl}")
            else:
                lines.append(f"> {cl}" if cl else ">")
        lines.append("")
        return

    # 容器 view（渲染子 block）
    if bt == 33:
        for cid in block.get("children", []):
            child = block_map.get(cid)
            if child:
                _render_block(child, block_map, token, lines)
        return

    # 群聊卡片
    if bt == 20:
        lines.append("[群聊卡片]")
        lines.append("")
        return

    # 文件
    if bt == 23:
        name = block.get("file", {}).get("name", "未知文件")
        lines.append(f"[文件: {name}]")
        lines.append("")
        return

    # 嵌入网页
    if bt == 26:
        url = block.get("iframe", {}).get("component", {}).get("url", "")
        if url:
            url = unquote(url)
        lines.append(f"[嵌入网页: {url}]" if url else "[嵌入网页]")
        lines.append("")
        return


def _render_table(block: dict, block_map: dict, token: str, lines: list):
    """渲染文档内表格为 Markdown 表格"""
    table_data = block.get("table", {})
    prop = table_data.get("property", {})
    col_size = prop.get("column_size", 1)
    cell_ids = table_data.get("cells", [])

    # 提取每个单元格的文本内容
    cell_texts = []
    for cid in cell_ids:
        cell_block = block_map.get(cid, {})
        # 递归渲染单元格内所有子 block
        cell_lines = []
        _render_cell_children(cell_block, block_map, token, cell_lines)
        # 合并为单行，管道符需要转义
        cell_text = " ".join(l for l in cell_lines if l).replace("|", "\\|")
        cell_texts.append(cell_text)

    # 按列数切分行
    rows = [cell_texts[i:i + col_size] for i in range(0, len(cell_texts), col_size)]
    if not rows:
        return

    # 表头
    header = rows[0]
    while len(header) < col_size:
        header.append("")
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join(["---"] * col_size) + " |")

    # 数据行
    for row in rows[1:]:
        while len(row) < col_size:
            row.append("")
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")


def _render_cell_children(block: dict, block_map: dict, token: str, lines: list):
    """递归渲染表格单元格内的所有内容"""
    for cid in block.get("children", []):
        child = block_map.get(cid)
        if not child:
            continue
        ct = child.get("block_type")
        key = TYPE_KEY_MAP.get(ct)

        # 有文本元素的 block
        if key and ct not in (14,):
            text = render_elements(child.get(key, {}).get("elements", []))
            if text:
                lines.append(text)
        elif ct == 14:
            content = render_elements(child.get("code", {}).get("elements", []))
            lines.append(f"`{content}`")
        elif ct == 27:
            local_path = child.get("image", {}).get("local_path", "")
            lines.append(f"![image]({local_path})" if local_path else "[图片]")

        # 递归处理子 block 的 children
        if child.get("children"):
            _render_cell_children(child, block_map, token, lines)


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "success": False,
            "error": "用法: feishu_doc.py <飞书文档链接>"
        }, ensure_ascii=False))
        sys.exit(1)

    url = sys.argv[1]

    # 检查环境变量
    app_id, app_secret = get_env_config()
    if not app_id or not app_secret:
        print(json.dumps({
            "success": False,
            "error": "未配置飞书应用凭证",
            "hint": "请设置环境变量:\nexport FEISHU_APP_ID=cli_xxx\nexport FEISHU_APP_SECRET=xxx\n\n获取方式:\n1. 访问 https://open.feishu.cn/app\n2. 创建企业自建应用\n3. 添加「云文档」权限\n4. 获取 App ID 和 App Secret"
        }, ensure_ascii=False))
        sys.exit(1)

    try:
        # 解析链接
        doc_token, doc_type = parse_url(url)

        # 获取 token
        token = get_token(app_id, app_secret)

        # 获取文档信息
        doc_info = get_document_info(doc_token, token)
        title = doc_info.get("title", doc_token)

        # 创建输出目录
        output_dir = CACHE_DIR / doc_token
        output_dir.mkdir(parents=True, exist_ok=True)

        # 获取所有 blocks
        blocks = fetch_all_blocks(doc_token, token)

        # 处理 blocks：下载图片，提取文档链接
        images, doc_links = process_blocks(blocks, output_dir, token)

        # 转换为 Markdown 并保存
        markdown = f"# {title}\n\n" + blocks_to_markdown(blocks, token)
        output_file = output_dir / "document.md"
        output_file.write_text(markdown, encoding="utf-8")

        # 输出结果
        result = {
            "success": True,
            "output_path": str(output_file),
            "title": title,
            "images": images,
            "referenced_docs": doc_links
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
