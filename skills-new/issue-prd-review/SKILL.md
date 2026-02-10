---
name: issue-prd-review
description: 当用户提供 PRD 文档（飞书链接或文本）、提到"评审 PRD"/"需求评估"/"review"时使用。读取 PRD 进行技术评估，通过则创建主 Issue + 子 Issue(s)，不通过则打回给产品。
---

# Issue PRD Review - PRD 评估与 Issue 创建

## Overview

读取 PRD 文档，进行技术评估。通过则创建主 Issue + 子 Issue(s)，不通过则打回给产品。

## 输入来源

| 输入类型 | 处理方式 |
|----------|----------|
| 飞书文档链接 | WebFetch 读取 |
| 文本内容 | 直接使用对话中的 PRD 文本 |
| 本地文件 | Read 工具读取 |

## 评估流程

1. **需求理解**：总结核心目标、关键功能点、边界条件
2. **代码影响分析**：搜索相关模块，评估改动范围
3. **工作量评估**：small/medium/large/extra-large
4. **爆炸半径评估**：isolated/contained/moderate/wide
5. **功能点拆分**：识别可独立交付的功能点

## 评估结果

| 结果 | 动作 |
|------|------|
| 通过 | 创建主 Issue + 技术评估 Comment + 子 Issue(s) |
| 不通过 | 输出问题清单和修改建议，打回给产品 |

## 操作命令

```bash
# 创建主 Issue
gh issue create --title "[PRD] {需求名称}" --body "$(cat <<'EOF'
{主 Issue Body，参考模板}
EOF
)"

# 添加技术评估 Comment
gh issue comment {主issue号} --body "$(cat <<'EOF'
{技术评估报告，参考模板}
EOF
)"

# 创建子 Issue 并关联父 Issue
gh issue create --title "[Story] {功能点}" --body "..." --label feat --parent {主issue号}
```

## 模板

- 主 Issue Body: `../shared/templates/prd-issue.md`
- 子 Issue Body: `../shared/templates/sub-issue.md`
- 技术评估 Comment: `../shared/templates/review-comment.md`
