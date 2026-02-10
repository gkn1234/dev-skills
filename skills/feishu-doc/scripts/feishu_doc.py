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
from urllib.parse import urlparse

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

        # 保存原始 blocks JSON
        output_file = output_dir / "document.json"
        doc_data = {
            "title": title,
            "doc_token": doc_token,
            "blocks": blocks
        }
        output_file.write_text(json.dumps(doc_data, ensure_ascii=False, indent=2), encoding="utf-8")

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
