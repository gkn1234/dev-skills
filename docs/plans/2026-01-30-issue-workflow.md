# Issue Workflow Skill 实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 创建一个基于 GitHub Issue 的研发流程管理 skill，实现 Milestone → User Story → Design → Task → Test Cases 的完整工作流。

**Architecture:** 使用 Claude Code skill 格式，主入口 skill.md 提供流程概览，5 个子 skill 分别处理各类型的创建。通过 `gh` CLI 与 GitHub API 交互，支持中英双语模板。

**Tech Stack:** Claude Code Skill, GitHub CLI (`gh`), Markdown

**Design Doc:** [docs/plans/2026-01-30-issue-workflow-design.md](./2026-01-30-issue-workflow-design.md)

---

## Task 1: 创建项目基础文件

**Files:**
- Create: `README.md`
- Create: `LICENSE`

### Step 1: 创建 README.md

```markdown
# Dev Skills

A collection of Claude Code skills for development workflows.

## Skills

### issue-workflow

GitHub Issue-based development workflow management.

**Features:**
- Milestone → User Story → Design → Task → Test Cases workflow
- Auto-create labels and bidirectional linking
- Bilingual templates (zh/en, auto-detected)
- Integration with `superpowers:brainstorming` and `superpowers:writing-plans`

**Usage:**

```bash
# Add to your Claude Code skills directory
git clone https://github.com/<your-username>/dev-skills.git ~/.claude/skills/dev-skills
```

**Sub-commands:**
- `/dev-skills:issue-workflow` - Workflow overview
- `/dev-skills:issue-workflow:create-milestone` - Create milestone
- `/dev-skills:issue-workflow:create-user-story` - Create user story
- `/dev-skills:issue-workflow:create-design` - Create design issue
- `/dev-skills:issue-workflow:create-task` - Create task issue
- `/dev-skills:issue-workflow:create-test-cases` - Create test cases issue

## License

MIT
```

### Step 2: 创建 LICENSE

```
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### Step 3: 提交

```bash
git add README.md LICENSE
git commit -m "chore: add README and MIT license"
```

---

## Task 2: 创建模板文件

**Files:**
- Create: `issue-workflow/references/templates-zh.md`
- Create: `issue-workflow/references/templates-en.md`

### Step 1: 创建中文模板文件

```markdown
# Issue 模板 - 中文

## User Story 模板

```markdown
## 用户故事
作为一个【角色】，我想要【功能】，以便【价值】。

## Design
📄 （待创建）

## 验收标准
（待创建）
```

## Design 模板

```markdown
## 概述
【设计文档内容摘要】

## 设计文档
📄 [【文档路径】](【文档链接】)

## User Story
📄 #【编号】

## Tasks
（待创建）
```

## Task 模板

```markdown
## 任务描述
【任务目标简述】

## 实现计划
📄 [【计划路径】](【计划链接】)

## User Story
📄 #【编号】

## Design
📄 #【编号】

## Test Cases
📄 （待创建）
```

## Test Cases 模板

```markdown
## 测试用例
- [ ] 【用例描述】

## User Story
📄 #【编号】

## Task
📄 #【编号】
```

## 标签

| 类型 | 标签名 | 颜色 |
|------|--------|------|
| User Story | `user-story` | `0052CC` (蓝色) |
| Design | `design` | `0E8A16` (绿色) |
| Task | `task` | `FBCA04` (黄色) |
| Test Cases | `test-cases` | `D93F0B` (橙色) |
```

### Step 2: 创建英文模板文件

```markdown
# Issue Templates - English

## User Story Template

```markdown
## User Story
As a 【role】, I want to 【action】, so that 【value】.

## Design
📄 (To be created)

## Acceptance Criteria
(To be created)
```

## Design Template

```markdown
## Overview
【Design document summary】

## Design Document
📄 [【Document path】](【Document link】)

## User Story
📄 #【number】

## Tasks
(To be created)
```

## Task Template

```markdown
## Description
【Task objective】

## Implementation Plan
📄 [【Plan path】](【Plan link】)

## User Story
📄 #【number】

## Design
📄 #【number】

## Test Cases
📄 (To be created)
```

## Test Cases Template

```markdown
## Test Cases
- [ ] 【Test case description】

## User Story
📄 #【number】

## Task
📄 #【number】
```

## Labels

| Type | Label | Color |
|------|-------|-------|
| User Story | `user-story` | `0052CC` (Blue) |
| Design | `design` | `0E8A16` (Green) |
| Task | `task` | `FBCA04` (Yellow) |
| Test Cases | `test-cases` | `D93F0B` (Orange) |
```

### Step 3: 提交

```bash
git add issue-workflow/references/
git commit -m "feat(issue-workflow): add bilingual issue templates"
```

---

## Task 3: 创建主入口 skill.md

**Files:**
- Create: `issue-workflow/skill.md`

### Step 1: 创建 skill.md

```markdown
---
name: issue-workflow
description: 基于 GitHub Issue 的研发流程管理。用于：(1) 创建里程碑管理大需求，(2) 拆分用户故事，(3) 创建 Design/Task/Test Cases Issue 并自动关联。触发词：create issue, milestone, user story, task breakdown, 研发流程, 里程碑, 用户故事, 任务拆分。
---

# Issue Workflow - 研发流程管理

## 流程概览

```
Milestone → User Story → Design → Task → Test Cases
    │           │           │        │         │
    │           │           │        │         └── 验收用例 (与 Task 1:1)
    │           │           │        └── 实现任务 (与 Design N:1)
    │           │           └── 设计文档 (与 User Story 1:1)
    │           └── 用户故事 (与 Milestone N:1)
    └── GitHub 原生里程碑功能
```

## 子命令

| 命令 | 用途 |
|------|------|
| `create-milestone` | 创建 GitHub 里程碑 |
| `create-user-story` | 创建用户故事 Issue |
| `create-design` | 创建设计文档 Issue（配合 `superpowers:brainstorming`）|
| `create-task` | 创建任务 Issue（配合 `superpowers:writing-plans`）|
| `create-test-cases` | 创建测试用例 Issue |

## 工作流集成

1. **设计阶段**：先使用 `/superpowers:brainstorming` 完成设计，再使用 `create-design`
2. **任务阶段**：先使用 `/superpowers:writing-plans` 编写计划，再使用 `create-task`

## 自动行为

- **标签**：自动检查并创建缺失的标签（`user-story`, `design`, `task`, `test-cases`）
- **关联**：自动在相关 Issue 间建立双向链接
- **语言**：根据用户对话语言自动选择模板（中/英文）
- **仓库**：优先从 `git remote` 自动检测，失败时询问用户

## 优先级规则

对于所有输入（milestone, user-story, design, task）：
1. 优先使用当前对话上下文中的信息
2. 其次使用命令参数（如 `--milestone 1`）
3. 最后查询 GitHub API 并展示选项列表供选择
```

### Step 2: 提交

```bash
git add issue-workflow/skill.md
git commit -m "feat(issue-workflow): add main skill entry point"
```

---

## Task 4: 创建 create-milestone 子命令

**Files:**
- Create: `issue-workflow/create-milestone.md`

### Step 1: 创建 create-milestone.md

```markdown
---
name: create-milestone
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
```

### Step 2: 提交

```bash
git add issue-workflow/create-milestone.md
git commit -m "feat(issue-workflow): add create-milestone sub-skill"
```

---

## Task 5: 创建 create-user-story 子命令

**Files:**
- Create: `issue-workflow/create-user-story.md`

### Step 1: 创建 create-user-story.md

```markdown
---
name: create-user-story
description: 在里程碑下创建用户故事 Issue。用于将需求拆分为面向用户的功能。Create a user story issue under a milestone.
---

# 创建用户故事

创建标准格式的用户故事 Issue。

## 流程

1. **检测仓库**（同 create-milestone）

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
```

### Step 2: 提交

```bash
git add issue-workflow/create-user-story.md
git commit -m "feat(issue-workflow): add create-user-story sub-skill"
```

---

## Task 6: 创建 create-design 子命令

**Files:**
- Create: `issue-workflow/create-design.md`

### Step 1: 创建 create-design.md

```markdown
---
name: create-design
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
```

### Step 2: 提交

```bash
git add issue-workflow/create-design.md
git commit -m "feat(issue-workflow): add create-design sub-skill"
```

---

## Task 7: 创建 create-task 子命令

**Files:**
- Create: `issue-workflow/create-task.md`

### Step 1: 创建 create-task.md

```markdown
---
name: create-task
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
```

### Step 2: 提交

```bash
git add issue-workflow/create-task.md
git commit -m "feat(issue-workflow): add create-task sub-skill"
```

---

## Task 8: 创建 create-test-cases 子命令

**Files:**
- Create: `issue-workflow/create-test-cases.md`

### Step 1: 创建 create-test-cases.md

```markdown
---
name: create-test-cases
description: 创建与任务关联的测试用例 Issue。用自然语言生成验收测试用例。Create a test cases issue linked to a task.
---

# 创建测试用例

创建与任务关联的测试用例 Issue。

## 流程

1. **检测仓库**

2. **确定任务**
   - 如果上下文中有：直接使用
   - 如果提供了参数：使用 `--task N`
   - 否则：列出任务供选择
   ```bash
   gh issue list --label task --json number,title --jq '.[] | "#\(.number): \(.title)"'
   ```

3. **确保标签存在**
   ```bash
   gh label create test-cases --color D93F0B --description "测试用例" 2>/dev/null || true
   ```

4. **读取任务详情**
   ```bash
   gh issue view {task_number} --json body,title --jq '{title: .title, body: .body}'
   ```

5. **从任务内容中提取用户故事编号**

6. **生成测试用例建议**

   根据任务内容，用自然语言建议验收测试用例。
   请用户确认/修改。

7. **从任务获取里程碑**
   ```bash
   gh issue view {task_number} --json milestone --jq '.milestone.number'
   ```

8. **创建测试用例 Issue**

   ```bash
   gh issue create \
     --title "Test Cases: {任务名称}" \
     --body "内容" \
     --label test-cases \
     --milestone N
   ```

9. **更新任务**（添加 Test Cases 链接）

   将 `📄 （待创建）` 替换为 `📄 #{test_cases_number}`

   ```bash
   gh issue edit {task_number} --body "新内容"
   ```

10. **更新用户故事**（添加到验收标准）

    读取用户故事内容，追加到验收标准：
    - 添加 `- [ ] [Test Cases #{number}](#{number})`

    ```bash
    gh issue edit {user_story_number} --body "新内容"
    ```

11. **报告结果**
    - 显示测试用例 Issue 编号和 URL
    - 确认任务和用户故事已更新

## 示例

针对任务 "实现登录 API 端点"：

建议的测试用例：
1. 用户可以使用有效的邮箱和密码登录
2. 使用无效密码登录失败（返回 401）
3. 使用不存在的邮箱登录失败（返回 401）
4. 登录成功返回有效的 JWT token
5. 登录限流生效（每分钟最多 5 次尝试）

```bash
gh issue create \
  --title "Test Cases: 登录 API 端点" \
  --body "## 测试用例
- [ ] 用户可以使用有效的邮箱和密码登录
- [ ] 使用无效密码登录失败（返回 401）
- [ ] 使用不存在的邮箱登录失败（返回 401）
- [ ] 登录成功返回有效的 JWT token
- [ ] 登录限流生效（每分钟最多 5 次尝试）

## User Story
📄 #42

## Task
📄 #44" \
  --label test-cases \
  --milestone 3
```
```

### Step 2: 提交

```bash
git add issue-workflow/create-test-cases.md
git commit -m "feat(issue-workflow): add create-test-cases sub-skill"
```

---

## Task 9: 最终验证与发布准备

### Step 1: 验证目录结构

```bash
tree /Users/macbookair/Desktop/projects/dev-skills
```

Expected:
```
dev-skills/
├── README.md
├── LICENSE
├── docs/
│   └── plans/
│       ├── 2026-01-30-issue-workflow-design.md
│       └── 2026-01-30-issue-workflow.md
└── issue-workflow/
    ├── skill.md
    ├── create-milestone.md
    ├── create-user-story.md
    ├── create-design.md
    ├── create-task.md
    ├── create-test-cases.md
    └── references/
        ├── templates-zh.md
        └── templates-en.md
```

### Step 2: 创建 .gitignore

```bash
echo ".DS_Store" > .gitignore
git add .gitignore
git commit -m "chore: add gitignore"
```

### Step 3: 查看所有提交

```bash
git log --oneline
```

### Step 4: 完成

Skill 开发完成，可以：
1. 创建 GitHub 仓库并推送
2. 将 `issue-workflow/` 复制到 Claude Code skills 目录测试

---

## 文件清单

| 文件 | 用途 |
|------|------|
| `README.md` | 项目介绍和使用说明 |
| `LICENSE` | MIT 开源协议 |
| `issue-workflow/skill.md` | 主入口，流程概览 |
| `issue-workflow/create-milestone.md` | 创建里程碑 |
| `issue-workflow/create-user-story.md` | 创建用户故事 |
| `issue-workflow/create-design.md` | 创建设计文档 Issue |
| `issue-workflow/create-task.md` | 创建任务 Issue |
| `issue-workflow/create-test-cases.md` | 创建测试用例 Issue |
| `issue-workflow/references/templates-zh.md` | 中文模板 |
| `issue-workflow/references/templates-en.md` | 英文模板 |
