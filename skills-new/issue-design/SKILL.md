---
name: issue-design
description: 当用户提到"添加设计"/"design"、或从子 Issue 继续流程时使用。调用 brainstorming 完成设计，为子 Issue 添加 Design Comment（含任务拆分）。
---

# Issue Design - 添加设计方案

## Overview

为子 Issue 添加 Design Comment（1:1 关系）。使用 brainstorming 完成设计，包含技术方案和任务拆分。

## 工作流程

1. 确认目标子 Issue
2. 读取子 Issue 的 body 获取功能描述
3. 调用 `superpowers:brainstorming`（**不创建本地文档**）
4. 设计完成后，格式化为 Design Comment
5. 添加 Comment 到 Issue

## 前置检查

1. 确认目标是子 Issue（通过父 Issue 关联判断）
2. 检查是否已存在 Design Comment（避免重复）

```bash
# 检查是否已有 Design Comment
gh api repos/{owner}/{repo}/issues/{issue号}/comments \
  --jq '.[] | select(.body | contains("<!-- type: design -->"))' | head -1
```

## 与 brainstorming 集成

| brainstorming 默认行为 | issue-design 调整 |
|------------------------|-------------------|
| 写入 `docs/plans/YYYY-MM-DD-<topic>-design.md` | 跳过，不创建本地文件 |
| 提交设计文档到 git | 跳过 |
| 输出设计内容 | 格式化后添加为 Issue Comment |

## 操作命令

```bash
# 添加 Design Comment
gh issue comment {子issue号} --body "$(cat <<'EOF'
{Design Comment，参考模板}
EOF
)"
```

## 模板

- Design Comment: `../shared/templates/design-comment.md`

## 注意

Design 阶段必须完成**任务拆分**，输出任务列表供后续 issue-tasks 使用。
