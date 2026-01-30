---
name: issue-workflow-pull-request
description: 当用户明确提到"创建 PR"/"提交 PR"/"pull request"、或从任务实现流程继续时使用
---

# 创建 Pull Request

## Overview

`issue-workflow-pull-request` 是 issue-workflow 流程的最后一环。在完成任务实现后，自动从 task issue 和 commits 生成 PR 内容，用户确认后创建 PR，并建立与 task issue 的双向关联。

**核心价值：**
- 自动生成结构化的 PR 描述
- 确保 PR 与 task issue 正确关联
- 合并后自动关闭相关 issue

## 流程

### 1. 检测仓库
- 自动检测 `git remote`
- 失败则询问用户

### 2. 确定 Task Issue
- 对话上下文中有：直接使用
- 参数指定：`--task 1,2,3` 或 `--task 1 --task 2`（支持多个）
- 检查当前分支名是否包含 issue 编号（如 `feature/123-login`）
- 都没有：列出 task issue 供选择（支持多选）

### 3. 收集 PR 信息
- 读取 task issue 内容（任务描述、关联的 user story、design、test cases）
- 获取当前分支相对于 base 分支的 commits
- 确定 base 分支（默认 main/master）

### 4. 自动生成 PR 内容

根据 task issue 和 commits 生成：
- PR 标题（从 task issue 标题派生）
- PR 描述（Summary、Changes、Related Issues）

呈现给用户确认/修改。

### 5. 创建 PR

```bash
gh pr create --title "标题" --body "描述" --base main
```

### 6. 双向更新
- 更新每个 task issue：添加 `## PR` 字段记录 PR 链接
- PR 描述中已包含 `Closes #task_number`，合并后自动关闭

### 7. 报告结果

"PR 已创建 (#N) 并关联到任务 (#M, #K)。合并后任务将自动关闭。"

## PR 模板

根据用户对话语言自动选择：

**中文模板：**
```markdown
## Summary
【自动生成：综合多个 task 的描述】

## Changes
【自动生成：从 commits 分析的主要改动】

## Related Issues
### Tasks
- Closes #task_1
- Closes #task_2

### Context
- User Story: #user_story_number
- Design: #design_number
- Test Cases: #test_cases_1, #test_cases_2
```

**英文模板：**
```markdown
## Summary
【Auto-generated: Combined description from tasks】

## Changes
【Auto-generated: Main changes analyzed from commits】

## Related Issues
### Tasks
- Closes #task_1
- Closes #task_2

### Context
- User Story: #user_story_number
- Design: #design_number
- Test Cases: #test_cases_1, #test_cases_2
```

## Common Mistakes

| 错误 | 示例 | 正确做法 |
|------|------|----------|
| 没有关联 task | 孤立的 PR | 必须关联至少一个 task issue |
| 标题太长 | 超过 70 字符 | 简洁概括，详情放描述里 |
| 描述太简略 | 只写"修复 bug" | 说明改了什么、为什么改 |
| 忘记 Closes 关键字 | 只写 `#123` | 用 `Closes #123` 实现自动关闭 |
| 混合多个不相关任务 | 一个 PR 改多个功能 | 相关任务才放一个 PR |

## 示例

用户完成任务实现后："帮我创建 PR"

**自动生成：**
```
检测到当前分支 feature/45-login-api，关联任务 #45。

PR 标题：feat: 实现登录 API 端点

PR 描述：
## Summary
实现 POST /api/auth/login 端点，支持 JWT token 生成和验证。

## Changes
- 添加 /api/auth/login 路由
- 实现 JWT token 生成逻辑
- 添加密码验证中间件

## Related Issues
### Tasks
- Closes #45

### Context
- User Story: #42
- Design: #43
- Test Cases: #46

确认创建 PR 吗？或者需要修改？
```

用户确认后 → 创建 PR → 更新 task issue

## 上下游关系

| 方向 | 技能 | 说明 |
|------|------|------|
| 上游 | `issue-workflow-task` | 先有任务 |
| 上游 | `issue-workflow-test-cases` | 建议先有测试用例 |
