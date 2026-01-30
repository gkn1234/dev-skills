---
name: issue-workflow
description: 基于 GitHub Issue 的研发流程管理。用于：(1) 创建里程碑管理大需求，(2) 拆分用户故事，(3) 创建 Design/Task/Test Cases Issue 并自动关联。触发词：create issue, milestone, user story, task breakdown, 研发流程, 里程碑, 用户故事, 任务拆分。
---

# Issue Workflow - 研发流程管理

## 流程概览

```
Milestone → User Story → Design → Task → Test Cases
    │           │           │        │         │
    │           │           │        │         └── 验收用例 (与 Task 1:1)
    │           │           │        └── 实现任务 (与 Design N:1)
    │           │           └── 设计文档 (与 User Story 1:1)
    │           └── 用户故事 (与 Milestone N:1)
    └── GitHub 原生里程碑功能
```

## 相关技能

| 技能 | 用途 |
|------|------|
| `issue-workflow-milestone` | 创建 GitHub 里程碑 |
| `issue-workflow-user-story` | 创建用户故事 Issue |
| `issue-workflow-design` | 创建设计文档 Issue（配合 `superpowers:brainstorming`）|
| `issue-workflow-task` | 创建任务 Issue（配合 `superpowers:writing-plans`）|
| `issue-workflow-test-cases` | 创建测试用例 Issue |

## 工作流集成

1. **设计阶段**：先使用 `/superpowers:brainstorming` 完成设计，再使用 `issue-workflow-design`
2. **任务阶段**：先使用 `/superpowers:writing-plans` 编写计划，再使用 `issue-workflow-task`

## 自动行为

- **标签**：自动检查并创建缺失的标签（`user-story`, `design`, `task`, `test-cases`）
- **关联**：自动在相关 Issue 间建立双向链接
- **语言**：根据用户对话语言自动选择模板（中/英文）
- **仓库**：优先从 `git remote` 自动检测，失败时询问用户

## 优先级规则

对于所有输入（milestone, user-story, design, task）：
1. 优先使用当前对话上下文中的信息
2. 其次使用命令参数（如 `--milestone 1`）
3. 最后查询 GitHub API 并展示选项列表供选择
