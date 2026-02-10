---
name: issue-implement
description: 当用户提到"实现"/"implement"/"开发"、或从 Test Cases 继续流程时使用。在 git worktree 中执行 Task 实现（Task:实现 = 1:1）。
---

# Issue Implement - 执行实现

## Overview

根据 Task 详情在 git worktree 中执行代码实现。

## 工作流程

1. 确认目标子 Issue 和 Task
2. 按需读取 Comment（Design + Task，**跳过 Test Cases**）
3. 创建 git worktree（`.worktrees/<分支名>`）
4. 调用 superpowers 执行实现
5. 本地验证（测试、构建）

## 按需读取 Comment

```bash
# 只读取 Design Comment
gh api repos/{owner}/{repo}/issues/{issue号}/comments \
  --jq '.[] | select(.body | contains("<!-- type: design -->")) | .body'

# 只读取特定 Task Comment
gh api repos/{owner}/{repo}/issues/{issue号}/comments \
  --jq '.[] | select(.body | contains("<!-- type: task, id: task-1 -->")) | .body'
```

**注意**：实现时**跳过 Test Cases Comment**，节省上下文。

## 分支命名

```
feat/<issue号>-<task-id>-<简述>
fix/<issue号>-<task-id>-<简述>
refactor/<issue号>-<task-id>-<简述>
```

## Worktree 管理

```bash
# 创建 worktree
git worktree add .worktrees/feat-123-task-1-add-login -b feat/123-task-1-add-login

# 切换到 worktree
cd .worktrees/feat-123-task-1-add-login
```

## 与 superpowers 集成

| 场景 | 使用技能 |
|------|----------|
| 多个独立步骤可并行 | `superpowers:subagent-driven-development` |
| 顺序执行的实现计划 | `superpowers:executing-plans` |

## 完成标准

- [ ] 代码符合 Task Comment 中的完成标准
- [ ] 本地测试通过
- [ ] 构建无错误
