---
name: issue-workflow
description: 当用户提到"研发流程"/"开发流程"/"workflow"、或需要了解整体工作流时使用。自动检测当前阶段并引导下一步操作。
---

# Issue Workflow - PRD 驱动研发流程

## Overview

基于 PRD 文档驱动的研发流程管理。自动检测当前阶段，引导下一步操作。

## 流程概览

```
一无所有
    │
    ▼
issue-prd-review ─→ 主 Issue + 评估 Comment + 子 Issue(s)
    │
    ▼ (对每个子 Issue)
issue-design ─→ Design Comment
    │
    ▼
issue-tasks ─→ Task Comment(s)
    │
    ▼
issue-test-cases ─→ Test Cases Comment(s)
    │
    ▼ (对每个 Task)
issue-implement ─→ 代码实现
    │
    ▼
issue-pr ─→ Pull Request
    │
    ▼
手动合并 ─→ 手动关闭 Issue
```

## 技能列表

| 技能 | 触发条件 | 用途 |
|------|----------|------|
| `issue-prd-review` | "评审 PRD"/"需求评估"/"review" | PRD 评估与 Issue 创建 |
| `issue-design` | "添加设计"/"design" | 添加 Design Comment |
| `issue-tasks` | "添加任务"/"tasks" | 添加 Task Comment |
| `issue-test-cases` | "添加用例"/"test cases" | 添加 Test Cases Comment |
| `issue-implement` | "实现"/"implement"/"开发" | 在 worktree 中执行实现 |
| `issue-pr` | "创建 PR"/"pull request" | 创建 Pull Request |

## 状态检测

### 第一层：主 Issue 检测

| 状态 | 判断条件 | 下一步 |
|------|----------|--------|
| 一无所有 | 无 PRD Issue | → issue-prd-review |
| 待评估 | 有主 Issue，无评估 Comment | → issue-prd-review（继续评估） |
| 待拆分 | 有评估 Comment，无子 Issue | → issue-prd-review（创建子 Issues） |
| 已拆分 | 有子 Issues | → 进入子 Issue 流程 |

### 第二层：子 Issue 检测

| 已有 Comment | 当前阶段 | 下一步 |
|--------------|----------|--------|
| 无 | 待设计 | → issue-design |
| design | 待拆分任务 | → issue-tasks |
| design, task | 待添加用例 | → issue-test-cases |
| design, task, test-cases | 待实现 | → issue-implement |
| 已有 PR | 待合并 | 手动合并 → 手动关闭 Issue |

### 状态检测命令

```bash
# 检测子 Issue 的 Comment 类型
gh api repos/{owner}/{repo}/issues/{issue号}/comments \
  --jq '[.[] | .body | capture("<!-- type: (?<type>[^,>]+)") | .type] | unique'
```

## 数据模型

| 关系 | 说明 |
|------|------|
| 主 Issue : 子 Issue | 1 : N（Sub-Issue 关联） |
| 子 Issue : Design | 1 : 1 |
| 子 Issue : Task | 1 : N |
| Task : Test Cases | 1 : 1 |
| Task : PR | 1 : 1 |

## 标签规则

| Issue 类型 | 标签 |
|------------|------|
| 主 Issue（PRD） | 无标签 |
| 子 Issue | `feat` / `fix` / `refactor` |
