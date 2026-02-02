---
name: issue-workflow
description: 当用户提到"研发流程"/"issue 管理"/"项目管理"、或需要了解整体工作流时使用
---

# Issue Workflow - 研发流程管理

## Overview

基于 GitHub Issue 的完整研发流程管理。从里程碑规划到 PR 提交，建立清晰的需求追踪链路。

## 流程概览

```
正向开发流程：
Milestone → User Story → Design → Task → Test Cases → Pull Request
    │           │          │        │         │            │
    │           │          │        │         │            └── 合并后自动关闭 Task
    │           │          │        │         └── 验收用例 (与 Task/User Story 关联)
    │           │          │        └── 实现任务 (与 User Story N:1)
    │           │          └── 设计内容 (嵌入 User Story)
    │           └── 用户故事 (与 Milestone N:1)
    └── GitHub 原生里程碑功能

问题修复流程：
Milestone → Problem → Design → Task → Test Cases → Pull Request
    │          │         │        │         │            │
    │          │         │        │         │            └── 合并后自动关闭 Task
    │          │         │        │         └── 验证通过后关闭 Problem
    │          │         │        └── 修复任务 (与 Problem N:1)
    │          │         └── 修复方案 (嵌入 Problem)
    │          └── 问题报告 (bug/improvement/refactor)
    └── 可用于专门的修复里程碑
```

## 技能列表

| 技能 | 触发条件 | 用途 |
|------|----------|------|
| `issue-workflow-milestone` | "里程碑"/"milestone"/"新阶段" | 创建 GitHub 里程碑 |
| `issue-workflow-problem` | "问题"/"problem"/"bug"/"改进"/"重构" | 提交 Problem Issue |
| `issue-workflow-user-story` | "用户故事"/"user story"/"我想要..." | 创建用户故事 Issue |
| `issue-workflow-design` | 完成 brainstorming 后、"设计文档"/"design" | 为 User Story 添加设计内容 |
| `issue-workflow-task` | 完成 writing-plans 后、"创建任务"/"task" | 创建任务 Issue |
| `issue-workflow-test-cases` | 从任务继续、"测试用例"/"test cases" | 创建测试用例 Issue |
| `issue-workflow-pull-request` | "创建 PR"/"提交 PR"/"pull request" | 创建关联 Task 的 PR |

## 工作流集成

| 阶段 | 推荐流程 |
|------|----------|
| **规划** | 创建 Milestone → 拆分 User Story |
| **设计** | `superpowers:brainstorming` → `issue-workflow-design`（更新 User Story） |
| **计划** | `superpowers:writing-plans` → `issue-workflow-task` |
| **测试** | `issue-workflow-test-cases` |
| **提交** | 实现代码 → `issue-workflow-pull-request` |
| **问题提交** | `issue-workflow-problem` |
| **问题修复** | `issue-workflow-design` → `issue-workflow-task` → `issue-workflow-test-cases` → `issue-workflow-pull-request` |

## 自动行为

- **标签管理**：自动检查并创建缺失的标签（`user-story`, `task`, `test-cases`, `problem`, `bug`, `improvement`, `refactor`, `severity:*`, `priority:*`）
- **双向关联**：自动在相关 Issue 间建立双向链接
- **语言适配**：根据用户对话语言自动选择模板（中/英文）
- **仓库检测**：优先从 `git remote` 自动检测，失败时询问用户
- **永久链接**：设计文档和实现计划使用 commit SHA 生成永久链接

## 优先级规则

对于所有输入（milestone, user-story, design, task）：
1. 优先使用当前对话上下文中的信息
2. 其次使用命令参数（如 `--milestone 1`、`--task 1,2,3`）
3. 最后查询 GitHub API 并展示选项列表供选择

## 质量标准

每个技能都内置质量检查，确保：
- **Milestone**：目标明确、范围合理
- **User Story**：符合 INVEST 原则
- **Problem**：描述清晰、标签完整、复现步骤明确（BUG 类型）
- **Design**：有明确目标、技术方案、可拆分任务
- **Task**：目标明确、1-3 天可完成、有完成标准
- **Test Cases**：场景明确、预期清晰、可验证
- **Pull Request**：关联 Task、描述清晰、使用 Closes 关键字
