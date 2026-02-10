---
name: issue-test-cases
description: 当用户提到"添加用例"/"test cases"、或从 Task 继续流程时使用。为每个 Task 添加 Test Cases Comment（Task:Test Cases = 1:1）。
---

# Issue Test Cases - 添加测试用例

## Overview

为每个 Task 添加对应的 Test Cases Comment（1:1 关系）。测试用例采用 Web 回归测试 todo-list 形式。

## 工作流程

1. 确认目标子 Issue
2. 读取 Task Comment(s)
3. 为每个 Task 生成 Test Cases Comment
4. 添加到 Issue

## 按需读取 Comment

```bash
# 只读取 Task Comments
gh api repos/{owner}/{repo}/issues/{issue号}/comments \
  --jq '.[] | select(.body | contains("<!-- type: task,")) | .body'
```

## 操作命令

```bash
# 为每个 Task 添加 Test Cases Comment
gh issue comment {子issue号} --body "$(cat <<'EOF'
{Test Cases Comment，参考模板}
EOF
)"
```

## 模板

- Test Cases Comment: `../shared/templates/test-cases-comment.md`

## Comment 标识

每个 Test Cases Comment 必须包含标识：

```markdown
<!-- type: test-cases, task-id: task-{n} -->
```

## 双向链接

Task 和 Test Cases 之间建立双向跳转：

- Task Comment: `> 🧪 Test Cases: [跳转](#test-cases-task-{n})`
- Test Cases Comment: `> 📋 Task: [跳转](#task-{n})`
