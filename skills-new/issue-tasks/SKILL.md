---
name: issue-tasks
description: 当用户提到"添加任务"/"tasks"、或从 Design 继续流程时使用。读取 Design 中的任务拆分，为子 Issue 添加 Task Comment（1:N 关系）。
---

# Issue Tasks - 添加任务

## Overview

读取 Design Comment 中的任务拆分，为每个 Task 生成详细 Comment。

## 工作流程

1. 确认目标子 Issue
2. 读取 Design Comment，解析任务拆分表
3. 为每个 Task 生成详细 Comment
4. 依次添加到 Issue

## 按需读取 Comment

```bash
# 只读取 Design Comment（节省上下文）
gh api repos/{owner}/{repo}/issues/{issue号}/comments \
  --jq '.[] | select(.body | contains("<!-- type: design -->")) | .body'
```

## 操作命令

```bash
# 为每个 Task 添加 Comment
gh issue comment {子issue号} --body "$(cat <<'EOF'
{Task Comment，参考模板}
EOF
)"
```

## 模板

- Task Comment: `../shared/templates/task-comment.md`

## Comment 标识

每个 Task Comment 必须包含标识，用于后续过滤：

```markdown
<!-- type: task, id: task-{n} -->
```
