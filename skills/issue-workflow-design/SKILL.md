---
name: issue-workflow-design
description: 创建与用户故事关联的设计文档 Issue。在使用 superpowers:brainstorming 完成设计后使用。Create a design issue linked to a user story.
---

# 创建设计文档

创建设计文档 Issue 并关联到用户故事。

## 流程

1. **提醒用户**
   > 在创建 Design Issue 之前，请确保已使用 `/superpowers:brainstorming` 完成设计并保存了设计文档。

2. **检测仓库**

3. **确定用户故事**
   - 如果上下文中有：直接使用
   - 如果提供了参数：使用 `--user-story N`
   - 否则：列出用户故事供选择
   ```bash
   gh issue list --label user-story --json number,title --jq '.[] | "#\(.number): \(.title)"'
   ```

4. **确保标签存在**
   ```bash
   gh label create design --color 0E8A16 --description "设计文档" 2>/dev/null || true
   ```

5. **收集设计详情**
   - 设计文档路径（如 `docs/plans/2026-01-30-login-design.md`）
   - 简要概述

6. **从用户故事获取里程碑**
   ```bash
   gh issue view {user_story_number} --json milestone --jq '.milestone.number'
   ```

7. **创建设计 Issue**

   ```bash
   gh issue create \
     --title "Design: {功能名称}" \
     --body "内容" \
     --label design \
     --milestone N
   ```

8. **更新用户故事**（双向链接）

   读取当前内容：
   ```bash
   gh issue view {user_story_number} --json body --jq '.body'
   ```

   将 `📄 （待创建）` 或 `📄 (To be created)` 替换为 `📄 #{design_number}`

   ```bash
   gh issue edit {user_story_number} --body "新内容"
   ```

9. **报告结果**
   - 显示设计 Issue 编号和 URL
   - 确认用户故事已更新
   - 存入上下文

## 示例

使用 brainstorming 完成设计并保存到 `docs/plans/2026-01-30-login-design.md` 后：

```bash
gh issue create \
  --title "Design: 用户登录系统" \
  --body "## 概述
基于 JWT 的认证系统，支持 refresh token 轮换。

## 设计文档
📄 [docs/plans/2026-01-30-login-design.md](./docs/plans/2026-01-30-login-design.md)

## User Story
📄 #42

## Tasks
（待创建）" \
  --label design \
  --milestone 3
```
