# issue-workflow-design 优化设计

## 背景

对比 obra/superpowers 技能库，优化 `issue-workflow-design` 技能，使其更符合最佳实践。

## 设计目标

- 将设计决策记录为 GitHub Issue
- 建立与用户故事、任务的追踪关联
- 支持有文档和无文档两种场景
- 与上下游技能无缝衔接

---

## 完整 SKILL.md

```markdown
---
name: issue-workflow-design
description: 当用户完成 brainstorming 设计、从用户故事继续流程、或明确提到"设计文档"/"design issue"时使用
---

# 创建设计文档

## Overview

将设计决策记录为 GitHub Issue，并建立与用户故事、任务的追踪关联。支持引用已有设计文档或提示先完成设计。

## 好的设计文档标准

| 原则 | 含义 | 检查点 |
|------|------|--------|
| **有明确目标** | 解决什么问题 | 设计目标清晰 |
| **有技术方案** | 如何实现 | 架构/数据流/接口已定义 |
| **有取舍说明** | 为什么这样选 | 备选方案和取舍已记录 |
| **可拆分任务** | 能分解实现 | 可识别出独立的实现任务 |

## 流程

### 1. 检测仓库
- 自动检测 `git remote`
- 失败则询问用户

### 2. 确定用户故事
- 对话上下文中有：直接使用
- 参数指定：`--user-story N`
- 否则：列出用户故事供选择

### 3. 检查设计文档

**有现成文档：**
- 询问文档路径（如 `docs/plans/2026-01-30-xxx-design.md`）
- 自动提取概述（读取文档前 200 字或 Overview 部分）

**没有文档：**
- 提示："建议先使用 `superpowers:brainstorming` 完成设计"
- 用户坚持继续 → 询问简要概述

### 4. 质量检查

创建前检查设计文档标准：
- 有明确目标？
- 有技术方案？
- 可拆分任务？

有问题则提示用户补充。

### 5. 创建 Issue

确保 `design` 标签存在，创建并关联 Milestone。

### 6. 双向更新

更新用户故事的 Design 字段：`📄 #design_number`

### 7. 引导下一步

"设计文档已创建 (#N) 并关联到用户故事 (#M)。接下来：
- 使用 `issue-workflow-task` 创建实现任务
- 或使用 `superpowers:writing-plans` 编写详细实现计划"

## Issue 模板

根据用户对话语言自动选择：

**中文模板：**
```markdown
## 概述
【定稿：设计目标和方案概述】

## 设计文档
📄 [docs/plans/YYYY-MM-DD-xxx-design.md](./docs/plans/YYYY-MM-DD-xxx-design.md)

## User Story
📄 #user_story_number

## Tasks
- [ ] （待创建，由 issue-workflow-task 关联，格式：#issue_number）
```

**英文模板：**
```markdown
## Overview
【定稿：Design goals and solution overview】

## Design Document
📄 [docs/plans/YYYY-MM-DD-xxx-design.md](./docs/plans/YYYY-MM-DD-xxx-design.md)

## User Story
📄 #user_story_number

## Tasks
- [ ] (To be created, linked by issue-workflow-task, format: #issue_number)
```

> **【定稿】**：流程第 3-4 步中确定的设计概述内容。

## Common Mistakes

| 错误 | 示例 | 正确做法 |
|------|------|----------|
| 概述太长 | 复制整个设计文档 | 2-3 句话概括核心方案 |
| 没有文档链接 | 只写概述不链接 | 必须链接到完整设计文档 |
| 忘记关联用户故事 | 孤立的设计 Issue | 双向链接确保可追溯 |
| 跳过 brainstorming | 边做边设计 | 先完成设计再创建 Issue |
| 设计太大 | 一个设计包含多个功能 | 一个用户故事对应一个设计 |

## 示例

用户完成 brainstorming 后："帮我创建设计文档 Issue"

**有设计文档：**
```
检测到你刚完成了登录系统的设计，文档路径是 docs/plans/2026-01-30-login-design.md。

概述：基于 JWT 的认证系统，支持 refresh token 轮换，包含登录、登出、token 刷新三个接口。

关联到用户故事 #42，确认创建设计 Issue 吗？
```

用户确认后 → 质量检查 → 创建 Issue → 更新用户故事

**没有设计文档：**
```
还没有设计文档。建议先使用 `superpowers:brainstorming` 完成设计。

如果你已经有设计思路，也可以直接提供：
- 设计目标是什么？
- 技术方案概述？
```

## 上下游关系

| 方向 | 技能 | 说明 |
|------|------|------|
| 上游 | `issue-workflow-user-story` | 先有用户故事 |
| 上游 | `superpowers:brainstorming` | 建议先完成设计 |
| 下游 | `issue-workflow-task` | 创建后拆分任务 |
| 下游 | `superpowers:writing-plans` | 或编写实现计划 |
```
