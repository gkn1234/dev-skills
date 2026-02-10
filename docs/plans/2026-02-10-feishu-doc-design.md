# feishu-doc 技能设计

## 概述

独立技能，读取飞书文档链接并转换为 Markdown。

## 设计决策

| 决策点 | 选择 |
|--------|------|
| 定位 | 独立技能，任何时候可调用 |
| 认证 | 环境变量 + 交互式引导 |
| 输出格式 | 原始 blocks JSON |
| 图片处理 | 下载到本地 |
| 文档链接 | 询问用户是否读取 |
| 输出目录 | `~/.cache/feishu-docs/` |
| 目录结构 | 扁平 + 本地链接替换 |
| 实现方式 | Python 脚本 |

## 环境变量

```bash
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=xxx
```

## 目录结构

```
skills/feishu-doc/
├── SKILL.md
└── scripts/
    └── feishu_doc.py
```

## 输出结构

```
~/.cache/feishu-docs/
├── DocA_xxx/
│   ├── document.md
│   └── assets/
│       ├── img1.png
│       └── img2.jpg
└── DocB_yyy/
    ├── document.md
    └── assets/
```

## API 调用流程

1. 解析飞书链接 → 提取 doc_token
2. 检查环境变量 → 无则引导配置
3. 获取 tenant_access_token
4. 调用 `/docx/v1/documents/{id}/blocks`
5. 遍历 blocks：
   - 文本/标题/列表 → 转 Markdown
   - 图片 → 下载到 `./assets/`
   - 文档链接 → 询问用户是否读取
6. 输出 Markdown 文件
7. 替换已下载文档的链接为本地路径

## Python 脚本结构

```python
#!/usr/bin/env python3
"""
飞书文档读取工具
"""

import os
import re
import json
import requests
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "feishu-docs"

def get_token() -> str:
    """获取 tenant_access_token"""

def parse_url(url: str) -> str:
    """解析飞书链接，提取 doc_token"""

def fetch_blocks(doc_token: str, token: str) -> list:
    """获取文档所有 blocks"""

def download_image(file_token: str, token: str, output_dir: Path) -> str:
    """下载图片，返回本地路径"""

def blocks_to_markdown(blocks: list, output_dir: Path) -> str:
    """将 blocks 转换为 Markdown"""

def extract_doc_links(blocks: list) -> list:
    """提取文档中引用的其他文档链接"""

def main():
    pass
```

## 脚本输出格式

```json
{
  "success": true,
  "output_path": "~/.cache/feishu-docs/Abc123/document.md",
  "images": ["img1.png", "img2.jpg"],
  "referenced_docs": [
    {"title": "接口规范", "url": "https://xxx.feishu.cn/docx/Def456"}
  ]
}
```

## 链接替换规则

| 场景 | 原始链接 | 替换后 |
|------|----------|--------|
| 已下载的文档 | `[文档B](https://xxx.feishu.cn/docx/DocB_yyy)` | `[文档B](../DocB_yyy/document.md)` |
| 未下载的文档 | 保留原始链接 | - |
| 图片 | 飞书内部链接 | `![alt](./assets/xxx.png)` |

## 使用示例

```
用户: 读取这个飞书文档 https://xxx.feishu.cn/docx/Abc123

助手: [调用 feishu_doc.py]
      文档标题：用户认证系统 PRD
      已下载 2 张图片

      发现 1 个引用文档：
      - 接口规范文档

      是否读取引用文档？

用户: 是

助手: [继续读取]
      完成！文档已保存：
      - ~/.cache/feishu-docs/Abc123/document.md
      - ~/.cache/feishu-docs/Def456/document.md
```

## 注意事项

- 图片临时链接有效期 24h
- 需要应用有「云文档」读取权限
- 大文档需处理 API 分页
