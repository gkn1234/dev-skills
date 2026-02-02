---
name: issue-workflow-problem
description: 当用户发现 bug、提出改进建议、需要代码重构、或明确提到"问题"/"problem"/"bug"/"改进"/"重构"时使用
---

# 提交 Problem

## Overview

提交问题报告并创建 GitHub Issue，支持 BUG、功能改进、代码重构三种类型。Problem 与 User Story 平行，后续走 Design → Task → Test Cases → PR 流程。

## 问题类型

| 类型 | 标签 | 说明 |
|------|------|------|
| **BUG** | `bug` | 程序错误、崩溃、异常 |
| **功能改进** | `improvement` | 功能不符合预期、优化点 |
| **代码重构** | `refactor` | 代码质量、技术债务、架构改进 |

## 标签体系

| 维度 | 标签 | 必选 |
|------|------|------|
| **类型标识** | `problem` | ✅ 是 |
| **问题类型** | `bug` / `improvement` / `refactor` | ✅ 是 |
| **严重程度** | `severity:critical` / `severity:high` / `severity:medium` / `severity:low` | ✅ 是 |
| **优先级** | `priority:p0` / `priority:p1` / `priority:p2` / `priority:p3` | ✅ 是 |

## 流程

### 1. 检测仓库
- 自动检测 `git remote`
- 失败则询问用户

### 2. 引导内容生成

**默认模式（快速确认）：**
- 根据用户描述，推测完整问题报告
- 一次性呈现，让用户确认或修改

**深入模式（用户需要时）：**
- 一次只问一个问题
- 问题是什么？
- 复现步骤？（BUG 类型）
- 期望 vs 实际行为？

### 3. 选择标签

依次确认：
- 问题类型：bug / improvement / refactor
- 严重程度：critical / high / medium / low
- 优先级：p0 / p1 / p2 / p3

提供默认推荐，用户确认或修改。

### 4. 记录来源（可选）

Problem 可能来源于：
- User Story 开发过程中发现：`--from-user-story N`
- Test Cases 验收时发现：`--from-test-cases N`
- 独立发现：无需关联

这是单向弱关联，仅在 Problem 中记录来源，不反向更新来源 Issue。

### 5. 质量检查

创建前检查：
- 问题描述是否清晰？
- 复现步骤是否完整？（BUG 类型）
- 期望行为是否明确？

有问题则提示用户补充。

### 6. 创建 Issue

确保所有必需标签存在（`problem`、问题类型、严重程度、优先级），创建 Issue。
如有 Milestone，通过 `--milestone` 参数关联。

### 7. 引导下一步

"Problem 已创建 (#N)。接下来可以使用 `issue-workflow-design` 添加修复方案。"

## Issue 模板

根据用户对话语言自动选择：

**中文模板：**
```markdown
## 问题描述
【定稿：问题现象】

## 复现步骤
1. 【定稿：复现步骤，BUG 类型必填】

## 期望行为
【定稿：应该是什么样】

## 实际行为
【定稿：目前是什么样】

## 环境信息
- 版本：
- 浏览器/系统：

## Design
📄 （待填充，使用 `issue-workflow-design` 添加修复方案）

## Tasks
- [ ] （待创建，由 issue-workflow-task 关联，格式：#issue_number）

## 验收标准
- [ ] （待创建，由 issue-workflow-test-cases 关联，格式：[Test Cases #N](#N)）

## 来源（可选）
- 来自 User Story: #N
- 来自 Test Cases: #N
```

**英文模板：**
```markdown
## Problem Description
【定稿：Problem description】

## Steps to Reproduce
1. 【定稿：Reproduction steps, required for BUG type】

## Expected Behavior
【定稿：What should happen】

## Actual Behavior
【定稿：What currently happens】

## Environment
- Version:
- Browser/OS:

## Design
📄 (To be filled, use `issue-workflow-design` to add fix design)

## Tasks
- [ ] (To be created, linked by issue-workflow-task, format: #issue_number)

## Acceptance Criteria
- [ ] (To be created, linked by issue-workflow-test-cases, format: [Test Cases #N](#N))

## Source (optional)
- From User Story: #N
- From Test Cases: #N
```

> **【定稿】**：流程第 2-5 步中确认的问题报告内容。

> **关闭条件**：Problem 在关联的 PR 合入且 Test Cases 验证通过后关闭。Task 由 PR 合并自动关闭。

## Common Mistakes

| 错误 | 示例 | 正确做法 |
|------|------|----------|
| 描述模糊 | "页面有问题" | 具体化："点击提交按钮后页面白屏" |
| 缺少复现步骤 | 只写"登录失败" | 补充：1. 打开登录页 2. 输入XX 3. 点击登录 |
| 期望/实际不分 | 混在一起写 | 分开描述：期望跳转首页，实际停留登录页 |
| 严重程度夸大 | 小 UI 问题标 critical | 按影响范围评估：阻塞=critical，影响体验=medium |
| 跳过标签 | 不设置优先级 | 所有标签维度都必须填写 |

## 示例

用户："登录页面输入密码后点击登录没反应"

**快速确认模式：**
```
根据你的描述，我理解的问题报告是：

问题描述：登录页面点击登录按钮无响应
复现步骤：1. 打开登录页面 2. 输入用户名和密码 3. 点击登录按钮
期望行为：跳转到首页或显示错误提示
实际行为：页面无任何响应

建议标签：
- 类型：bug
- 严重程度：high（核心功能不可用）
- 优先级：p1

这样描述准确吗？需要调整吗？
```

用户确认后 → 质量检查 → 创建 Issue

## 上下游关系

| 方向 | 技能 | 说明 |
|------|------|------|
| 上游 | `issue-workflow-milestone` | 可选关联里程碑 |
| 下游 | `issue-workflow-design` | 添加修复方案 |
| 下游 | `issue-workflow-task` | 创建修复任务 |
| 下游 | `issue-workflow-test-cases` | 创建验收测试 |
| 来源 | `issue-workflow-user-story` | 可能来自用户故事（单向弱关联） |
| 来源 | `issue-workflow-test-cases` | 可能来自验收测试发现（单向弱关联） |
