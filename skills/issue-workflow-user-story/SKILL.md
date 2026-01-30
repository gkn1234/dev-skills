---
name: issue-workflow-user-story
description: 在里程碑下创建用户故事 Issue。用于将需求拆分为面向用户的功能。Create a user story issue under a milestone.
---

# 创建用户故事

创建标准格式的用户故事 Issue。

## 流程

1. **检测仓库**（同 issue-workflow-milestone）

2. **确定里程碑**
   - 如果上下文中有：直接使用
   - 如果提供了参数：使用 `--milestone N`
   - 否则：列出里程碑供选择
   ```bash
   gh api repos/{owner}/{repo}/milestones --jq '.[] | "\(.number): \(.title)"'
   ```

3. **确保标签存在**
   ```bash
   gh label create user-story --color 0052CC --description "用户故事" 2>/dev/null || true
   ```

4. **收集故事详情**
   - 角色：用户是谁？
   - 行为：想要做什么？
   - 价值：为什么要这样做？

5. **创建 Issue**

   根据用户对话语言自动选择模板：

   **中文模板：**
   ```markdown
   ## 用户故事
   作为一个【角色】，我想要【行为】，以便【价值】。

   ## Design
   📄 （待创建）

   ## 验收标准
   （待创建）
   ```

   **英文模板：**
   ```markdown
   ## User Story
   As a 【role】, I want to 【action】, so that 【value】.

   ## Design
   📄 (To be created)

   ## Acceptance Criteria
   (To be created)
   ```

   ```bash
   gh issue create --title "标题" --body "内容" --label user-story --milestone N
   ```

6. **报告结果**
   - 显示 Issue 编号和 URL
   - 存入上下文

## 示例

用户："为登录功能创建一个用户故事"

询问：
- 角色？→ "已注册用户"
- 行为？→ "使用邮箱和密码登录"
- 价值？→ "访问我的个人仪表盘"

```bash
gh issue create \
  --title "用户使用邮箱/密码登录" \
  --body "## 用户故事
作为一个已注册用户，我想要使用邮箱和密码登录，以便访问我的个人仪表盘。

## Design
📄 （待创建）

## 验收标准
（待创建）" \
  --label user-story \
  --milestone 3
```
