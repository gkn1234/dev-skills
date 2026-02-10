---
name: issue-workflow
description: 当用户提到"研发流程"/"workflow"/"下一步"/"继续"/"进度"、需要了解整体工作流、或询问当前状态时使用。检测 Issue 状态并引导到对应技能。
---

# Issue Workflow - PRD 驱动研发流程

## 职责

检测 Issue 状态，引导用户到对应的下游技能。

## 流程概览

```
PRD 文档
    │
    ▼
issue-prd-review ─→ 主 Issue + 技术评估 Comment
    │
    ▼ (对每个功能点)
issue-design ─→ 子 Issue + Design Comment
    │
    ▼ (对每个 Task)
issue-tasks ─→ Task Comment
    │
    ▼ (可选)
issue-test-cases ─→ Test Cases Comment
    │
    ▼
issue-implement ─→ 代码实现
    │
    ▼
issue-pr ─→ Pull Request
    │
    ▼
手动合并 → 手动关闭 Issue
```

## 技能列表

| 技能 | 触发条件 | 产出 |
|------|----------|------|
| `issue-repo` | 所有技能前置 | 确定 owner/repo |
| `issue-prd-review` | PRD 文档、"评审"、"新需求" | 主 Issue + 技术评估 |
| `issue-design` | "设计"、"子 Issue"、从主 Issue 继续 | 子 Issue + Design Comment |
| `issue-tasks` | "任务"、"task"、从子 Issue 继续 | Task Comment |
| `issue-test-cases` | "测试用例"、"test cases" | Test Cases Comment |
| `issue-implement` | "实现"、"开发"、"coding" | 代码 + 本地验证 |
| `issue-pr` | "创建 PR"、"pull request" | Pull Request |

## 状态检测

```bash
# 检测 Issue 的 Comment 类型
gh api repos/{owner}/{repo}/issues/{issue号}/comments \
  --jq '[.[] | .body | capture("<!-- type: (?<type>[^,>]+)") | .type] | unique'
```

| 检测结果 | 当前阶段 | 下一步 |
|----------|----------|--------|
| 无 Issue | 起点 | `issue-prd-review` |
| 主 Issue 无 review | PRD 待评审 | `issue-prd-review` |
| 主 Issue 有 review，无子 Issue | 待拆分功能点 | `issue-design` |
| 子 Issue 无 design | 待设计 | `issue-design` |
| 子 Issue 有 design，无 task | 待拆分任务 | `issue-tasks` |
| 子 Issue 有 task | 待实现 | `issue-implement` |
| Task 已实现 | 待提 PR | `issue-pr` |

## 使用示例

```
用户: 我有一个 PRD 需要评审

助手: → 使用 issue-prd-review 评审 PRD 并创建主 Issue
```

```
用户: Issue #100 下一步是什么

助手: [检测 #100 状态]
      主 Issue #100 已有技术评估，建议的功能点：
      1. 用户登录表单
      2. JWT 认证服务
      3. OAuth 集成

      → 使用 issue-design 为功能点创建子 Issue
```

```
用户: #101 进度

助手: [检测 #101 状态]
      子 Issue #101 当前状态：
      - ✅ Design Comment
      - ✅ task-1, task-2 (Task Comments)
      - ⏳ task-1 待实现

      → 使用 issue-implement 实现 task-1
```
