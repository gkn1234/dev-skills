---
name: feishu-doc
description: 读取飞书文档链接并输出原始 JSON。当用户提供飞书文档链接、需要读取飞书文档内容、或提到"飞书"/"Feishu"/"lark"时使用。
---

# 飞书文档读取

## 概述

独立技能，读取飞书文档链接并输出原始 blocks JSON，支持图片下载和文档链接提取。

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
│   ├── document.json    # 原始 blocks 数据
│   └── assets/
│       ├── img1.png
│       └── img2.jpg
└── DocB_yyy/
    ├── document.json
    └── assets/
```

## 脚本输出格式

```json
{
  "success": true,
  "output_path": "~/.cache/feishu-docs/Abc123/document.json",
  "title": "文档标题",
  "images": ["img1.png", "img2.jpg"],
  "referenced_docs": [
    {"title": "接口规范", "url": "https://xxx.feishu.cn/docx/Def456"}
  ]
}
```

## document.json 结构

```json
{
  "title": "文档标题",
  "doc_token": "Abc123",
  "blocks": [
    {
      "block_id": "xxx",
      "block_type": 2,
      "text": { "elements": [...] }
    }
  ]
}
```

图片 block 会添加 `local_path` 字段指向已下载的本地文件。

## 处理引用文档

当脚本输出 `referenced_docs` 时，询问用户是否读取，确认后对每个文档再次调用脚本。

## 注意事项

- 图片临时链接有效期 24h
- 需要应用有「云文档」读取权限
- 大文档自动处理 API 分页
