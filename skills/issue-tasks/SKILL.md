---
name: issue-tasks
description: 当用户提到"添加任务"/"tasks"/"创建任务"/"task breakdown"/"实现计划"、从 Design 继续流程、或 issue-design 完成后使用。选取一个 Task，为其生成详细 Task Comment。
---

# Issue Tasks - 添加任务

## 职责

1. 读取 Design Comment 中的任务拆分，获取 Task 列表
2. 用户选取一个 Task（或自定义）
3. 为该 Task 生成详细 Comment

## 前置：仓库检测

调用 `issue-repo` 技能确定目标仓库。

## 工作流程

```
1. 确认目标子 Issue
   │
2. 读取 Design Comment，提取 Task 列表
   │
3. 用户选取一个 Task（或自定义新 Task）
   │
4. 调用 writing-plans 生成详细 Comment
   │
5. 添加到 Issue
   │
   ▼
→ 下一步：issue-test-cases（为该 Task 添加测试用例）
→ 或直接：issue-implement（实现该 Task）
→ 或继续：为其他 Task 重复 issue-tasks
```

## 操作命令

```bash
# 读取 Design Comment
gh api repos/{owner}/{repo}/issues/{子issue号}/comments \
  --jq '.[] | select(.body | contains("<!-- type: design -->")) | .body'

# 检查已存在的 Task Comments（避免重复）
gh api repos/{owner}/{repo}/issues/{子issue号}/comments \
  --jq '[.[] | select(.body | contains("<!-- type: task")) |
    .body | capture("<!-- type: task, id: (?<id>[^>]+) -->") | .id]'

# 添加 Task Comment
gh issue comment {子issue号} \
  --repo {owner}/{repo} \
  --body-file /tmp/task-{n}-comment.md
```

## 使用示例

```
用户: 给 Issue #101 添加任务

助手: [调用 issue-repo] 仓库: owner/repo

      [读取 Design Comment]
      Design 中的任务拆分：
      1. task-1: 创建登录表单组件
      2. task-2: 实现 JWT 认证服务
      3. task-3: 添加 OAuth 集成

      请选择要添加的 Task（输入序号或自定义）

用户: 1

助手: 好的，为"创建登录表单组件"生成详细 Task Comment。

      [调用 superpowers:writing-plans]
      生成详细实现步骤...

      是否添加 Task Comment？

用户: 是

助手: [添加 Task Comment: task-1]

      完成！已添加 task-1 到 Issue #101

      → 下一步：使用 issue-test-cases 为 task-1 添加测试用例
      → 或直接：使用 issue-implement 实现 task-1
      → 或继续：使用 issue-tasks 为其他 Task 添加 Comment
```

**自定义 Task**：

```
用户: 我想加一个"添加单元测试"

助手: 好的，为"添加单元测试"生成 Task Comment（task-4）。
      （后续同上）
```

## 与 writing-plans 集成

| writing-plans 默认 | issue-tasks 调整 |
|-------------------|------------------|
| 写入本地计划文件 | **跳过**，不创建文件 |
| 提交到 git | **跳过** |
| 输出计划内容 | **格式化为 Task Comment** |

## 模板

| 模板 | 路径 | 用途 |
|------|------|------|
| Task Comment | `shared/templates/task-comment.md` | Task 详细实现计划 |

## 关联流程

| 方向 | 技能 | 说明 |
|------|------|------|
| **上游** | `issue-design` | 创建子 Issue + Design Comment（含任务拆分） |
| **下游** | `issue-test-cases` | 为 Task 添加测试用例 |
| **下游** | `issue-implement` | 实现 Task |
| **循环** | `issue-tasks` | 为其他 Task 添加 Comment |

## 注意事项

- **单个 Task**：每次调用只处理一个 Task
- **可自定义**：用户可以选择建议的 Task，也可以自定义
- **Task ID 格式**：`task-1`, `task-2`, `task-3`（与 Design 中一致）
- **Test Cases 链接**：预留链接，待 issue-test-cases 添加后生效
