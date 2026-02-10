---
name: issue-pr
description: 当用户提到"创建 PR"/"提交 PR"/"pull request"/"合并代码"、实现完成后、或 issue-implement 完成后使用。为 Task 创建 PR 关联子 Issue（Task : PR = 1:1）。
---

# Issue PR - 创建 Pull Request

## 职责

为 Task 创建 Pull Request，关联子 Issue（Task : PR = 1:1）。

## 前置：仓库检测

调用 `issue-repo` 技能确定目标仓库。

## 工作流程

```
1. 确认目标子 Issue 和 Task
   │
2. 读取 Task Comment（按需过滤）
   │
3. 确认分支已推送到远程
   │
4. 创建 PR，使用 Related to #子issue号
   │
   ▼
→ 后续：手动合并后关闭 Issue
```

## 操作命令

```bash
# 读取特定 Task Comment
gh api repos/{owner}/{repo}/issues/{子issue号}/comments \
  --jq '.[] | select(.body | contains("<!-- type: task, id: task-1 -->")) | .body'

# 推送分支到远程
git push -u origin feat/101-task-1-add-login

# 创建 PR
gh pr create \
  --repo {owner}/{repo} \
  --title "{Task 名称} (#{子issue号})" \
  --body-file /tmp/pr-body.md \
  --base main

# 获取 PR URL
gh pr view --repo {owner}/{repo} --json url --jq '.url'
```

## 关联规则

| 关联方式 | 说明 |
|----------|------|
| `Related to #子issue号` | 关联但不自动关闭 Issue |
| `Closes #子issue号` | **不使用**，Issue 手动关闭 |

**原因**：一个子 Issue 可能有多个 Task，每个 Task 对应一个 PR。所有 PR 合并后再手动关闭 Issue。

## PR 标题格式

```
{Task 名称} (#{子issue号})
```

示例：
- `添加登录表单组件 (#101)`
- `修复认证错误处理 (#102)`

## 使用示例

```
用户: 给 task-1 创建 PR

助手: [调用 issue-repo] 仓库: owner/repo

      [读取 Task Comment: task-1]
      任务：创建登录表单组件

      [检查分支状态]
      分支 feat/101-task-1-add-login 已推送

      [创建 PR]
      gh pr create \
        --title "添加登录表单组件 (#101)" \
        --body-file /tmp/pr-body.md

      PR 创建成功！
      https://github.com/owner/repo/pull/105

      → 后续：Code Review 后手动合并
      → 所有 Task PR 合并后，手动关闭 Issue #101
```

## 模板

| 模板 | 路径 | 用途 |
|------|------|------|
| PR Body | `shared/templates/pr.md` | PR 描述模板 |

## 关联流程

| 方向 | 技能 | 说明 |
|------|------|------|
| **上游** | `issue-implement` | 实现 Task |

## 注意事项

- **不使用 Closes**：使用 `Related to` 避免自动关闭
- **Issue 手动关闭**：所有 Task PR 合并后手动关闭
- **PR 标题含 Issue 号**：便于追踪
- **Code Review**：PR 创建后等待 Review
