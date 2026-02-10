---
name: issue-design
description: 当用户提到"添加设计"/"design"/"技术方案"/"架构设计"/"创建子 Issue"、从主 Issue 继续流程、或 issue-prd-review 完成后使用。选取一个功能点，创建子 Issue 并添加 Design Comment。
---

# Issue Design - 创建子 Issue 与设计方案

## 职责

1. 读取主 Issue 的技术评估 Comment，获取功能点列表
2. 用户选取一个功能点（或自定义）
3. 创建子 Issue
4. 为该子 Issue 添加 Design Comment

## 前置：仓库检测

调用 `issue-repo` 技能确定目标仓库。

## 工作流程

```
1. 确认目标主 Issue
   │
2. 读取技术评估 Comment，提取功能点列表
   │
3. 用户选取一个功能点（或自定义新功能点）
   │
4. 创建子 Issue
   │
5. 调用 brainstorming 完成设计
   │
6. 添加 Design Comment 到子 Issue
   │
   ▼
→ 下一步：issue-tasks（为该子 Issue 创建 Task Comments）
→ 或继续：为其他功能点重复 issue-design
```

## 操作命令

```bash
# 读取主 Issue 信息
gh issue view {主issue号} --repo {owner}/{repo} --json body,title

# 读取技术评估 Comment（含功能点建议）
gh api repos/{owner}/{repo}/issues/{主issue号}/comments \
  --jq '.[] | select(.body | contains("<!-- type: review -->")) | .body'

# 创建子 Issue（带标签）
gh issue create \
  --repo {owner}/{repo} \
  --title "[Story] {功能点名称}" \
  --body-file /tmp/sub-issue.md \
  --label feat

# 获取子 Issue 号
SUB_ISSUE=$(gh issue list --repo {owner}/{repo} --limit 1 --json number --jq '.[0].number')

# 将子 Issue 设为主 Issue 的 Sub-Issue
gh issue develop $SUB_ISSUE --repo {owner}/{repo} --issue $MAIN_ISSUE

# 添加 Design Comment
gh issue comment $SUB_ISSUE \
  --repo {owner}/{repo} \
  --body-file /tmp/design-comment.md
```

## 使用示例

```
用户: 给 Issue #100 添加子 Issue

助手: [调用 issue-repo] 仓库: owner/repo

      [读取主 Issue #100]
      [读取技术评估 Comment]

      技术评估建议的功能点：
      1. 用户登录表单
      2. JWT 认证服务
      3. OAuth 集成

      请选择要创建的功能点（输入序号或自定义）

用户: 1

助手: 好的，为"用户登录表单"创建子 Issue。

      [创建子 Issue #101]
      [关联到主 Issue #100]

      现在为 #101 添加设计？

用户: 好

助手: [调用 superpowers:brainstorming]

      ## 设计讨论 - 用户登录表单

      Q: 表单字段有哪些？
      A: 用户名、密码、记住我

      Q: 需要验证码吗？
      A: 暂不需要

      ...

      设计完成，是否添加到 Issue #101？

用户: 是

助手: [添加 Design Comment 到 #101]

      完成！子 Issue #101 已创建并添加设计。

      任务拆分结果：
      - task-1: 创建 LoginForm 组件
      - task-2: 添加表单验证
      - task-3: 集成登录 API

      → 下一步：使用 issue-tasks 为 #101 创建 Task Comments
      → 或继续：使用 issue-design 为其他功能点创建子 Issue
```

**自定义功能点**：

```
用户: 我想先做"密码重置功能"

助手: 好的，为"密码重置功能"创建子 Issue 并添加设计。
      （后续同上）
```

## 与 brainstorming 集成

| brainstorming 默认 | issue-design 调整 |
|-------------------|-------------------|
| 写入本地设计文档 | **跳过**，不创建文件 |
| 提交到 git | **跳过** |
| 输出设计内容 | **格式化为 Design Comment** |

**重点**：Design Comment 必须包含**任务拆分**，输出 Task 列表供 `issue-tasks` 使用。

## 模板

| 模板 | 路径 | 用途 |
|------|------|------|
| 子 Issue | `shared/templates/sub-issue.md` | 子 Issue Body |
| Design Comment | `shared/templates/design-comment.md` | 设计方案 Comment |

## 关联流程

| 方向 | 技能 | 说明 |
|------|------|------|
| **上游** | `issue-prd-review` | 创建主 Issue + 技术评估 Comment（含功能点建议） |
| **下游** | `issue-tasks` | 为子 Issue 创建 Task Comments |
| **循环** | `issue-design` | 为其他功能点创建子 Issue |

## 注意事项

- **单个功能点**：每次调用只处理一个功能点
- **可自定义**：用户可以选择建议的功能点，也可以自定义
- **子 Issue 关联**：使用 GitHub Sub-Issue 功能关联主 Issue
- **标签规则**：子 Issue 使用 `feat`/`fix`/`refactor`
- **任务拆分必须完成**：Design Comment 必须包含 Task 列表
- **Task ID 格式**：使用 `task-1`, `task-2`, `task-3` 等
