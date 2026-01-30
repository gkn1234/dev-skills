---
name: issue-workflow-milestone
description: 创建 GitHub 里程碑，用于管理大需求。当开始新项目阶段或功能集时使用。Create a GitHub milestone for managing a large requirement.
---

# 创建里程碑

创建 GitHub 里程碑以追踪大需求。

## 流程

1. **检测仓库**
   ```bash
   gh repo view --json nameWithOwner -q '.nameWithOwner'
   ```
   如果失败，询问用户 `owner/repo`。

2. **收集信息**
   - 询问里程碑标题
   - 询问描述（可选）
   - 询问截止日期（可选，格式：YYYY-MM-DD）

3. **创建里程碑**
   ```bash
   gh api repos/{owner}/{repo}/milestones -f title="标题" -f description="描述" -f due_on="日期"
   ```

   不设截止日期时：
   ```bash
   gh api repos/{owner}/{repo}/milestones -f title="标题" -f description="描述"
   ```

4. **报告结果**
   - 显示里程碑编号和 URL
   - 存入上下文供后续命令使用

## 示例

用户："为用户认证功能创建一个里程碑"

```bash
gh api repos/myorg/myrepo/milestones \
  -f title="用户认证" \
  -f description="实现完整的用户认证系统，包括登录、注册和密码重置。"
```

输出：
```
已创建里程碑 #3: 用户认证
URL: https://github.com/myorg/myrepo/milestone/3
```
