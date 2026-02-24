---
name: feishu-doc
description: 读取飞书文档链接并输出 Markdown。当用户提供飞书文档链接、需要读取飞书文档内容、或提到"飞书"/"Feishu"/"lark"时使用。
---

# 飞书文档读取

## 概述

独立技能，读取飞书文档链接并转换为 Markdown 输出，支持图片下载、嵌入表格转换和文档链接提取。

## 使用方式

```bash
# 安装依赖（首次使用）
pip install -r skills/feishu-doc/requirements.txt

# 读取文档
python skills/feishu-doc/scripts/feishu_doc.py <飞书文档链接>
```

## 环境变量

需要配置飞书应用凭证：

```bash
export FEISHU_APP_ID=cli_xxx
export FEISHU_APP_SECRET=xxx
```

如未配置，脚本会输出配置指引。

## 输出目录

```
~/.cache/feishu-docs/
├── DocA_xxx/
│   ├── document.md     # Markdown 内容
│   └── assets/
│       ├── img1.png
│       └── img2.jpg
└── DocB_yyy/
    ├── document.md
    └── assets/
```

## 脚本输出格式

```json
{
  "success": true,
  "output_path": "~/.cache/feishu-docs/Abc123/document.md",
  "title": "文档标题",
  "images": ["img1.png", "img2.jpg"],
  "referenced_docs": [
    {"title": "接口规范", "url": "https://xxx.feishu.cn/docx/Def456"}
  ]
}
```

## 读取文档内容

脚本执行后，直接用 Read 工具读取 `output_path` 指向的 Markdown 文件即可。

## 处理引用文档

当脚本输出 `referenced_docs` 时，询问用户是否读取，确认后对每个文档再次调用脚本。

## 注意事项

- 图片临时链接有效期 24h
- 需要应用有「云文档」和「电子表格」读取权限
- 大文档自动处理 API 分页
- 嵌入表格自动转为 Markdown 表格
