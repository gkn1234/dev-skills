---
name: issue-workflow-user-story
description: 当用户想要添加新功能（"我想加个..."、"需要一个..."）、拆分里程碑为具体功能、或明确提到"用户故事"/"user story"时使用
---

# 创建用户故事

## Overview

提供用户故事编写的逐步引导，遵循业界最佳实践，生成高质量、可追踪的 GitHub Issue。

## 好的用户故事标准（INVEST）

| 原则 | 含义 | 检查点 |
|------|------|--------|
| **I**ndependent | 独立 | 不依赖其他故事即可开发 |
| **N**egotiable | 可协商 | 描述目标而非具体实现 |
| **V**aluable | 有价值 | 对用户有明确好处 |
| **E**stimable | 可估算 | 范围清晰到能评估工作量 |
| **S**mall | 足够小 | 1-3 天内可完成 |
| **T**estable | 可测试 | 能定义明确的验收条件 |

## 流程

### 1. 检测仓库
- 自动检测 `git remote`
- 失败则询问用户

### 2. 确定里程碑
- 对话上下文中有：直接使用
- 参数指定：`--milestone N`
- 否则：列出里程碑供选择

### 3. 引导内容生成

**默认模式（快速确认）：**
- 根据用户描述，推测完整用户故事
- 一次性呈现，让用户确认或修改

**深入模式（用户需要时）：**
- 一次只问一个问题
- 角色："谁会使用这个功能？"（提供 2-3 选项）
- 行为："想要完成什么？"
- 价值："完成后有什么好处？"（重点追问）

### 4. 质量检查

创建前自动检查 INVEST 原则：
- 故事是否独立？
- 范围是否足够小（1-3 天）？
- 价值是否明确？

有问题则提示用户调整。

### 5. 创建 Issue

确保 `user-story` 标签存在，创建并关联 Milestone。

### 6. 引导下一步

"用户故事已创建 (#N)。接下来可以使用 `issue-workflow-design` 创建设计文档。"

## Issue 模板

根据用户对话语言自动选择：

**中文模板：**
```markdown
## 用户故事
【定稿】

## Design
📄 （待填充，使用 `issue-workflow-design` 添加设计）

## Tasks
- [ ] （待创建，由 issue-workflow-task 关联，格式：#issue_number）

## 验收标准
- [ ] （待创建，由 issue-workflow-test-cases 关联，格式：[Test Cases #N](#N)）
```

**英文模板：**
```markdown
## User Story
【定稿】

## Design
📄 (To be filled, use `issue-workflow-design` to add design)

## Tasks
- [ ] (To be created, linked by issue-workflow-task, format: #issue_number)

## Acceptance Criteria
- [ ] (To be created, linked by issue-workflow-test-cases, format: [Test Cases #N](#N))
```

> **【定稿】**：流程第 3-4 步中讨论并通过质量检查的用户故事内容。

## Common Mistakes

| 错误 | 示例 | 正确做法 |
|------|------|----------|
| 角色太泛 | "用户" | 具体化："已注册用户"、"管理员" |
| 行为是实现 | "点击按钮提交表单" | 描述目标："提交反馈" |
| 价值缺失 | "以便使用该功能" | 量化好处："节省手动操作时间" |
| 故事太大 | 包含 5+ 个功能点 | 拆分为多个独立故事 |
| 技术语言 | "调用 API 获取数据" | 用户视角："查看我的订单" |

## 示例

用户："我想加个导出功能"

**快速确认模式：**
```
根据你的描述，我理解的用户故事是：

作为一个数据分析师，我想要将报表导出为 Excel 格式，以便在本地进行进一步分析和分享给团队。

这样描述准确吗？需要调整吗？
```

用户确认后 → 质量检查 → 创建 Issue

**深入模式（用户说"不太确定"）：**
```
谁会使用这个导出功能？
A. 普通用户 - 导出自己的数据
B. 数据分析师 - 导出报表做分析
C. 管理员 - 导出系统数据做备份
D. 其他（请描述）
```

逐步引导 → 形成定稿 → 质量检查 → 创建 Issue

## 上下游关系

| 方向 | 技能 | 说明 |
|------|------|------|
| 上游 | `issue-workflow-milestone` | 通常先创建里程碑 |
| 下游 | `issue-workflow-design` | 添加设计内容 |
| 下游 | `issue-workflow-task` | 创建实现任务 |
| 下游 | `issue-workflow-test-cases` | 创建验收测试 |
