---
name: issue-test-cases
description: 当用户提到"添加用例"/"test cases"/"测试用例"/"验收标准"/"QA"/"回归测试"、从 Task 继续流程、或 issue-tasks 完成后使用。选取一个 Task，为其添加 Test Cases Comment。
---

# Issue Test Cases - 添加测试用例

## 职责

1. 读取 Task Comments，获取 Task 列表
2. 用户选取一个 Task
3. 为该 Task 生成 Test Cases Comment
4. 添加到 Issue（含双向链接）

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
4. 生成 Test Cases Comment
   │
5. 添加到 Issue
   │
   ▼
→ 下一步：issue-implement（实现 Task）
→ 或继续：为其他 Task 重复 issue-test-cases
```

## 操作命令

```bash
# 获取 Task 列表（仅 ID）
gh api repos/{owner}/{repo}/issues/{子issue号}/comments \
  --jq '[.[] | select(.body | contains("<!-- type: task,")) |
    .body | capture("<!-- type: task, id: (?<id>[^>]+) -->") | .id]'

# 检查已存在的 Test Cases（避免重复）
gh api repos/{owner}/{repo}/issues/{子issue号}/comments \
  --jq '[.[] | select(.body | contains("<!-- type: test-cases")) |
    .body | capture("<!-- type: test-cases, task-id: (?<id>[^>]+) -->") | .id]'

# 选择后读取特定 Task Comment
gh api repos/{owner}/{repo}/issues/{子issue号}/comments \
  --jq '.[] | select(.body | contains("<!-- type: task, id: task-1 -->")) | .body'

# 添加 Test Cases Comment
gh issue comment {子issue号} \
  --repo {owner}/{repo} \
  --body-file /tmp/test-cases-task-{n}.md
```

## 测试用例格式

参考模板 `shared/templates/test-cases-comment.md`，要点：
- **分类**：正常流程、边界场景、异常场景
- **结构**：分步骤 + 验证点 + `- [ ] 通过`

## 使用示例

```
用户: 给 Issue #101 添加测试用例

助手: [调用 issue-repo] 仓库: owner/repo

      [读取 Task Comments]
      可添加用例的 Task：
      1. task-1: 创建登录表单组件
      2. task-2: 实现 JWT 认证服务
      3. task-3: 添加 OAuth 集成

      请选择要添加用例的 Task（输入序号）

用户: 1

助手: 好的，为 task-1 生成测试用例。

      [生成 Test Cases]
      - 正常流程：3 个用例
      - 边界场景：2 个用例
      - 异常场景：1 个用例

      是否添加 Test Cases Comment？

用户: 是

助手: [添加 Test Cases: task-1]

      完成！已添加 task-1 的测试用例到 Issue #101

      → 下一步：使用 issue-implement 实现 task-1
      → 或继续：使用 issue-test-cases 为其他 Task 添加用例
```

## 模板

| 模板 | 路径 | 用途 |
|------|------|------|
| Test Cases Comment | `shared/templates/test-cases-comment.md` | 测试用例 Comment |

## 关联流程

| 方向 | 技能 | 说明 |
|------|------|------|
| **上游** | `issue-tasks` | 创建 Task Comments |
| **下游** | `issue-implement` | 实现 Task |
| **循环** | `issue-test-cases` | 为其他 Task 添加用例 |

## 注意事项

- **单个 Task**：每次调用只处理一个 Task
- **todo-list 格式**：使用 `- [ ]` 便于 QA 勾选
- **分类明确**：正常流程、边界场景、异常场景
- **双向链接**：确保 Task 和 Test Cases 可互相跳转
