---
name: issue-implement
description: 当用户提到"实现"/"implement"/"开发"/"coding"/"写代码"、从 Task 或 Test Cases 继续流程、或 issue-tasks/issue-test-cases 完成后使用。选取一个 Task，在 git worktree 中执行实现。
---

# Issue Implement - 执行实现

## 职责

1. 读取 Task Comments，获取 Task 列表
2. 用户选取一个 Task
3. 创建 git worktree
4. 执行代码实现
5. 本地验证（测试、构建）

## 前置：仓库检测

调用 `issue-repo` 技能确定目标仓库。

## 工作流程

```
1. 确认目标子 Issue
   │
2. 读取 Task Comments，提取 Task 列表
   │
3. 用户选取一个 Task
   │
4. 创建 git worktree（.worktrees/<分支名>）
   │
5. 调用 superpowers 执行实现
   │
6. 本地验证（测试、构建）
   │
   ▼
→ 下一步：issue-pr（创建 Pull Request）
→ 或继续：为其他 Task 重复 issue-implement
```

## 操作命令

```bash
# 获取 Task 列表（仅 ID）
gh api repos/{owner}/{repo}/issues/{子issue号}/comments \
  --jq '[.[] | select(.body | contains("<!-- type: task,")) |
    .body | capture("<!-- type: task, id: (?<id>[^>]+) -->") | .id]'

# 选择后读取特定 Task Comment
gh api repos/{owner}/{repo}/issues/{子issue号}/comments \
  --jq '.[] | select(.body | contains("<!-- type: task, id: task-1 -->")) | .body'

# 创建 worktree
git worktree add .worktrees/feat-101-task-1-add-login -b feat/101-task-1-add-login

# 完成后清理 worktree（可选）
git worktree remove .worktrees/feat-101-task-1-add-login
```

## 分支命名规范

```
feat/<issue号>-<task-id>-<简述>
fix/<issue号>-<task-id>-<简述>
refactor/<issue号>-<task-id>-<简述>
```

## 使用示例

```
用户: 实现 Issue #101

助手: [调用 issue-repo] 仓库: owner/repo

      [读取 Task Comments]
      可实现的 Task：
      1. task-1: 创建登录表单组件
      2. task-2: 实现 JWT 认证服务
      3. task-3: 添加 OAuth 集成

      请选择要实现的 Task（输入序号）

用户: 1

助手: 好的，实现 task-1: 创建登录表单组件

      [创建 worktree]
      git worktree add .worktrees/feat-101-task-1-add-login -b feat/101-task-1-add-login

      [调用 superpowers 技能实现]
      执行实现步骤...

      [本地验证]

      实现完成！

      → 下一步：调用 issue-pr 创建 Pull Request
      → 或继续：使用 issue-implement 实现其他 Task
```

## 与 superpowers 集成

| 场景 | 使用技能 |
|------|----------|
| 多个独立步骤可并行 | `superpowers:subagent-driven-development` |
| 顺序执行的实现计划 | `superpowers:executing-plans` |
| TDD 流程 | `superpowers:test-driven-development` |

## 完成标准

- [ ] 代码符合 Task Comment 中的完成标准
- [ ] 本地测试通过
- [ ] 构建无错误

## 关联流程

| 方向 | 技能 | 说明 |
|------|------|------|
| **上游** | `issue-tasks` | 创建 Task Comment |
| **上游** | `issue-test-cases` | 创建 Test Cases Comment |
| **下游** | `issue-pr` | 创建 Pull Request |
| **循环** | `issue-implement` | 实现其他 Task |

## 注意事项

- **单个 Task**：每次调用只实现一个 Task
- **Worktree 位置**：统一放在 `.worktrees/` 目录下
- **跳过 Test Cases**：实现阶段不读取测试用例 Comment，节省上下文
