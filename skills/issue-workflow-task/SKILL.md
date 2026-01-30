---
name: issue-workflow-task
description: 创建与设计文档关联的任务 Issue。在使用 superpowers:writing-plans 完成实现计划后使用。Create a task issue linked to a design.
---

# 创建任务

创建任务 Issue 并关联到设计文档。

## 流程

1. **提醒用户**
   > 在创建 Task Issue 之前，请确保已使用 `/superpowers:writing-plans` 完成实现计划并保存了计划文档。

2. **检测仓库**

3. **确定设计文档**
   - 如果上下文中有：直接使用
   - 如果提供了参数：使用 `--design N`
   - 否则：列出设计文档供选择
   ```bash
   gh issue list --label design --json number,title --jq '.[] | "#\(.number): \(.title)"'
   ```

4. **确保标签存在**
   ```bash
   gh label create task --color FBCA04 --description "实现任务" 2>/dev/null || true
   ```

5. **收集任务详情**
   - 任务标题/描述
   - 实现计划路径

6. **从设计文档获取用户故事**
   ```bash
   gh issue view {design_number} --json body --jq '.body'
   ```
   解析 `## User Story` 部分获取用户故事编号。

7. **从设计文档获取里程碑**
   ```bash
   gh issue view {design_number} --json milestone --jq '.milestone.number'
   ```

8. **创建任务 Issue**

   ```bash
   gh issue create \
     --title "Task: {任务名称}" \
     --body "内容" \
     --label task \
     --milestone N
   ```

9. **更新设计文档**（添加到 Tasks 列表）

   读取当前内容，追加到 Tasks 部分：
   - 将 `（待创建）` 替换为 `- [ ] #{task_number}`
   - 或追加 `- [ ] #{task_number}` 到已有列表

   ```bash
   gh issue edit {design_number} --body "新内容"
   ```

10. **报告结果**
    - 显示任务 Issue 编号和 URL
    - 确认设计文档已更新
    - 存入上下文

## 示例

使用 writing-plans 完成计划并保存到 `docs/plans/2026-01-30-login-api.md` 后：

```bash
gh issue create \
  --title "Task: 实现登录 API 端点" \
  --body "## 任务描述
实现 POST /api/auth/login 端点，支持 JWT token 生成。

## 实现计划
📄 [docs/plans/2026-01-30-login-api.md](./docs/plans/2026-01-30-login-api.md)

## User Story
📄 #42

## Design
📄 #43

## Test Cases
📄 （待创建）" \
  --label task \
  --milestone 3
```
