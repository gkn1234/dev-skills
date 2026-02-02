---
name: issue-workflow-task
description: 当用户完成 writing-plans 计划、从用户故事继续流程、或明确提到"创建任务"/"task issue"时使用
---

# 创建任务

## Overview

将实现计划记录为 GitHub Issue，并建立与用户故事的追踪关联。支持引用已有计划文档或直接描述任务。

## 好的任务标准

| 原则 | 含义 | 检查点 |
|------|------|--------|
| **目标明确** | 做什么 | 任务目标清晰具体 |
| **范围合理** | 多大 | 1-3 天内可完成 |
| **可验证** | 怎么算完成 | 有明确的完成标准 |
| **有依赖说明** | 前置条件 | 依赖关系已识别 |

## 流程

### 1. 检测仓库
- 自动检测 `git remote`
- 失败则询问用户

### 2. 确定用户故事
- 对话上下文中有：直接使用
- 参数指定：`--user-story N`
- 否则：列出用户故事供选择

### 3. 检查实现计划

**有现成计划：**
- 询问计划路径（如 `docs/plans/2026-01-30-xxx.md`）
- 自动提取任务描述

**没有计划：**
- 提示："建议先使用 `superpowers:writing-plans` 完成计划"
- 用户坚持继续 → 询问任务描述

### 4. 质量检查

创建前检查任务标准：
- 目标是否明确？
- 范围是否合理（1-3 天）？
- 完成标准是否清晰？

有问题则提示用户调整，修改后再继续。

### 5. 确保文档已提交

质量检查通过后，检查实现计划是否已提交到 git：
```bash
git ls-files --error-unmatch {doc_path} 2>/dev/null
```

**未提交：**
- 提示："实现计划需要先提交到 git，以便生成永久链接"
- 引导提交：`git add {doc_path} && git commit -m "docs: 添加实现计划"`
- 获取 commit SHA：`git rev-parse HEAD`

**已提交：**
- 直接获取包含该文件的 commit SHA

### 6. 创建 Issue

确保 `task` 标签存在，创建并关联 Milestone。

### 7. 双向更新

更新用户故事的 Tasks 列表：添加 `- [ ] #task_number`

### 8. 引导下一步

"任务已创建 (#N) 并关联到用户故事 (#M)。接下来可以使用 `issue-workflow-test-cases` 创建测试用例。"

## Issue 模板

根据用户对话语言自动选择：

**中文模板：**
```markdown
## 任务描述
【定稿：任务目标和范围】

## 实现计划
📄 [docs/plans/YYYY-MM-DD-xxx.md](https://github.com/{owner}/{repo}/blob/{commit_sha}/docs/plans/YYYY-MM-DD-xxx.md)

## User Story
📄 #user_story_number

## Test Cases
📄 （待创建，由 issue-workflow-test-cases 关联，格式：#issue_number）
```

**英文模板：**
```markdown
## Task Description
【定稿：Task goal and scope】

## Implementation Plan
📄 [docs/plans/YYYY-MM-DD-xxx.md](https://github.com/{owner}/{repo}/blob/{commit_sha}/docs/plans/YYYY-MM-DD-xxx.md)

## User Story
📄 #user_story_number

## Test Cases
📄 (To be created, linked by issue-workflow-test-cases, format: #issue_number)
```

> **永久链接**：使用 `{commit_sha}` 指向特定提交，确保分支删除后链接仍可访问。通过 `git rev-parse HEAD` 获取当前 commit SHA。

> **【定稿】**：流程第 3-4 步中确定的任务描述内容。

## Common Mistakes

| 错误 | 示例 | 正确做法 |
|------|------|----------|
| 任务太大 | "实现整个登录系统" | 拆分："实现登录 API"、"实现登录页面" |
| 描述模糊 | "优化性能" | 具体化："将列表加载时间从 3s 降到 1s" |
| 没有完成标准 | 只写"做XX" | 添加"完成时应该能XX" |
| 忘记关联用户故事 | 孤立的任务 | 必须关联用户故事 |
| 跳过计划 | 边做边想 | 先完成实现计划 |

## 示例

用户完成 writing-plans 后："帮我创建任务 Issue"

**有实现计划：**
```
检测到你刚完成了登录 API 的实现计划，文档路径是 docs/plans/2026-01-30-login-api.md。

任务描述：实现 POST /api/auth/login 端点，支持 JWT token 生成和验证。

关联到用户故事 #42，确认创建任务 Issue 吗？
```

用户确认后 → 质量检查 → 创建 Issue → 更新用户故事

**没有实现计划：**
```
还没有实现计划。建议先使用 `superpowers:writing-plans` 完成计划。

如果任务比较简单，也可以直接描述：
- 任务目标是什么？
- 预计多久完成？
```

## 上下游关系

| 方向 | 技能 | 说明 |
|------|------|------|
| 上游 | `issue-workflow-user-story` | 先有用户故事 |
| 上游 | `superpowers:writing-plans` | 建议先完成计划 |
| 下游 | `issue-workflow-test-cases` | 创建后添加测试用例 |
