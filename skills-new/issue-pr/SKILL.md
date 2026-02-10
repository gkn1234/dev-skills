---
name: issue-pr
description: 当用户提到"创建 PR"/"提交 PR"/"pull request"、或实现完成后使用。为 Task 创建 PR 关联子 Issue（Task:PR = 1:1）。
---

# Issue PR - 创建 Pull Request

## Overview

为 Task 创建 Pull Request，关联子 Issue。

## 工作流程

1. 确认目标子 Issue 和 Task
2. 读取 Task Comment（按需过滤）
3. 推送分支到远程
4. 创建 PR，使用 `Related to #子issue号`

## 按需读取 Comment

```bash
# 只读取特定 Task Comment
gh api repos/{owner}/{repo}/issues/{issue号}/comments \
  --jq '.[] | select(.body | contains("<!-- type: task, id: task-1 -->")) | .body'
```

## 操作命令

```bash
# 推送分支
git push -u origin feat/123-task-1-add-login

# 创建 PR
gh pr create \
  --title "{Task 名称} (#{子issue号})" \
  --body "$(cat <<'EOF'
{PR 内容，参考模板}
EOF
)" \
  --base main
```

## 关联规则

- 所有 PR 统一使用 `Related to #子issue号`（不自动关闭）
- Issue 手动关闭（所有 Task PR 合并后）

## 模板

- PR: `../shared/templates/pr.md`
