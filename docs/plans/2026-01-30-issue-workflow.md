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
description: GitHub Issue-based development workflow management. Use for: (1) Creating milestones for large requirements, (2) Breaking down User Stories, (3) Creating Design/Task/Test Cases issues with auto-linking. Triggers on: "create issue", "milestone", "user story", "task breakdown", "研发流程", "里程碑", "用户故事", "任务拆分".
---

# Issue Workflow

## Process Overview

```
Milestone → User Story → Design → Task → Test Cases
    │           │           │        │         │
    │           │           │        │         └── Acceptance tests (1:1 with Task)
    │           │           │        └── Implementation units (N:1 with Design)
    │           │           └── Architecture doc (1:1 with User Story)
    │           └── Business requirements (N:1 with Milestone)
    └── GitHub native milestone feature
```

## Sub-commands

| Command | Purpose |
|---------|---------|
| `create-milestone` | Create GitHub milestone |
| `create-user-story` | Create user story issue |
| `create-design` | Create design issue (use with `superpowers:brainstorming`) |
| `create-task` | Create task issue (use with `superpowers:writing-plans`) |
| `create-test-cases` | Create test cases issue |

## Workflow Integration

1. **Design Phase**: Use `/superpowers:brainstorming` first, then `create-design`
2. **Task Phase**: Use `/superpowers:writing-plans` first, then `create-task`

## Auto Behaviors

- **Labels**: Auto-create if missing (`user-story`, `design`, `task`, `test-cases`)
- **Linking**: Bidirectional links between related issues
- **Language**: Auto-detect from conversation (zh/en templates)
- **Repository**: Auto-detect from `git remote`, prompt if not found

## Priority Rules

For all inputs (milestone, user-story, design, task):
1. Context from current conversation
2. Command parameters (e.g., `--milestone 1`)
3. Query GitHub API and present selection list
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
description: Create a GitHub milestone for managing a large requirement. Use when starting a new project phase or feature set.
---

# Create Milestone

Create a GitHub milestone to track a large requirement.

## Process

1. **Detect repository**
   ```bash
   gh repo view --json nameWithOwner -q '.nameWithOwner'
   ```
   If fails, ask user for `owner/repo`.

2. **Gather information**
   - Ask for milestone title
   - Ask for description (optional)
   - Ask for due date (optional, format: YYYY-MM-DD)

3. **Create milestone**
   ```bash
   gh api repos/{owner}/{repo}/milestones -f title="TITLE" -f description="DESC" -f due_on="DATE"
   ```

   Without due date:
   ```bash
   gh api repos/{owner}/{repo}/milestones -f title="TITLE" -f description="DESC"
   ```

4. **Report result**
   - Show milestone number and URL
   - Store in context for subsequent commands

## Example

User: "Create a milestone for user authentication feature"

```bash
gh api repos/myorg/myrepo/milestones \
  -f title="User Authentication" \
  -f description="Implement complete user authentication system including login, registration, and password reset."
```

Output:
```
Created Milestone #3: User Authentication
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
description: Create a user story issue under a milestone. Use when breaking down requirements into user-facing features.
---

# Create User Story

Create a user story issue with standard format.

## Process

1. **Detect repository** (same as create-milestone)

2. **Determine milestone**
   - If in context: use it
   - If parameter provided: use `--milestone N`
   - Otherwise: list milestones and ask
   ```bash
   gh api repos/{owner}/{repo}/milestones --jq '.[] | "\(.number): \(.title)"'
   ```

3. **Ensure label exists**
   ```bash
   gh label create user-story --color 0052CC --description "User Story" 2>/dev/null || true
   ```

4. **Gather story details**
   - Role: Who is the user?
   - Action: What do they want to do?
   - Value: Why do they want it?

5. **Create issue**

   Template (auto-detect language from conversation):

   **Chinese:**
   ```markdown
   ## 用户故事
   作为一个【role】，我想要【action】，以便【value】。

   ## Design
   📄 （待创建）

   ## 验收标准
   （待创建）
   ```

   **English:**
   ```markdown
   ## User Story
   As a 【role】, I want to 【action】, so that 【value】.

   ## Design
   📄 (To be created)

   ## Acceptance Criteria
   (To be created)
   ```

   ```bash
   gh issue create --title "TITLE" --body "BODY" --label user-story --milestone N
   ```

6. **Report result**
   - Show issue number and URL
   - Store in context

## Example

User: "Create a user story for login feature"

Response:
- Role? → "registered user"
- Action? → "log in with email and password"
- Value? → "access my personal dashboard"

```bash
gh issue create \
  --title "User login with email/password" \
  --body "## User Story
As a registered user, I want to log in with email and password, so that I can access my personal dashboard.

## Design
📄 (To be created)

## Acceptance Criteria
(To be created)" \
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
description: Create a design issue linked to a user story. Use after completing design with superpowers:brainstorming.
---

# Create Design

Create a design issue and link it to a user story.

## Process

1. **Remind user**
   > Before creating a Design issue, ensure you have completed the design using `/superpowers:brainstorming` and saved the design document.

2. **Detect repository**

3. **Determine user story**
   - If in context: use it
   - If parameter: use `--user-story N`
   - Otherwise: list user stories and ask
   ```bash
   gh issue list --label user-story --json number,title --jq '.[] | "#\(.number): \(.title)"'
   ```

4. **Ensure label exists**
   ```bash
   gh label create design --color 0E8A16 --description "Design Document" 2>/dev/null || true
   ```

5. **Gather design details**
   - Design document path (e.g., `docs/plans/2026-01-30-login-design.md`)
   - Brief summary

6. **Get milestone from user story**
   ```bash
   gh issue view {user_story_number} --json milestone --jq '.milestone.number'
   ```

7. **Create design issue**

   ```bash
   gh issue create \
     --title "Design: {feature_name}" \
     --body "BODY" \
     --label design \
     --milestone N
   ```

8. **Update user story** (bidirectional link)

   Read current body:
   ```bash
   gh issue view {user_story_number} --json body --jq '.body'
   ```

   Replace `📄 （待创建）` or `📄 (To be created)` with `📄 #{design_number}`

   ```bash
   gh issue edit {user_story_number} --body "NEW_BODY"
   ```

9. **Report result**
   - Show design issue number and URL
   - Confirm user story was updated
   - Store in context

## Example

After brainstorming session saved `docs/plans/2026-01-30-login-design.md`:

```bash
gh issue create \
  --title "Design: User Login System" \
  --body "## Overview
JWT-based authentication with refresh token rotation.

## Design Document
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
description: Create a task issue linked to a design. Use after completing implementation plan with superpowers:writing-plans.
---

# Create Task

Create a task issue and link it to a design.

## Process

1. **Remind user**
   > Before creating a Task issue, ensure you have completed the implementation plan using `/superpowers:writing-plans` and saved the plan document.

2. **Detect repository**

3. **Determine design**
   - If in context: use it
   - If parameter: use `--design N`
   - Otherwise: list designs and ask
   ```bash
   gh issue list --label design --json number,title --jq '.[] | "#\(.number): \(.title)"'
   ```

4. **Ensure label exists**
   ```bash
   gh label create task --color FBCA04 --description "Implementation Task" 2>/dev/null || true
   ```

5. **Gather task details**
   - Task title/description
   - Implementation plan path

6. **Get user story from design**
   ```bash
   gh issue view {design_number} --json body --jq '.body'
   ```
   Parse `## User Story` section to get user story number.

7. **Get milestone from design**
   ```bash
   gh issue view {design_number} --json milestone --jq '.milestone.number'
   ```

8. **Create task issue**

   ```bash
   gh issue create \
     --title "Task: {task_name}" \
     --body "BODY" \
     --label task \
     --milestone N
   ```

9. **Update design** (add to Tasks list)

   Read current body, append to Tasks section:
   - Replace `（待创建）` with `- [ ] #{task_number}`
   - Or append `- [ ] #{task_number}` to existing list

   ```bash
   gh issue edit {design_number} --body "NEW_BODY"
   ```

10. **Report result**
    - Show task issue number and URL
    - Confirm design was updated
    - Store in context

## Example

After writing-plans session saved `docs/plans/2026-01-30-login-api.md`:

```bash
gh issue create \
  --title "Task: Implement Login API Endpoint" \
  --body "## Description
Implement POST /api/auth/login endpoint with JWT token generation.

## Implementation Plan
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
description: Create a test cases issue linked to a task. Generates acceptance test cases in natural language.
---

# Create Test Cases

Create a test cases issue linked to a task.

## Process

1. **Detect repository**

2. **Determine task**
   - If in context: use it
   - If parameter: use `--task N`
   - Otherwise: list tasks and ask
   ```bash
   gh issue list --label task --json number,title --jq '.[] | "#\(.number): \(.title)"'
   ```

3. **Ensure label exists**
   ```bash
   gh label create test-cases --color D93F0B --description "Test Cases" 2>/dev/null || true
   ```

4. **Read task details**
   ```bash
   gh issue view {task_number} --json body,title --jq '{title: .title, body: .body}'
   ```

5. **Extract user story number from task body**

6. **Generate test cases suggestions**

   Based on task content, suggest acceptance test cases in natural language.
   Ask user to confirm/modify.

7. **Get milestone from task**
   ```bash
   gh issue view {task_number} --json milestone --jq '.milestone.number'
   ```

8. **Create test cases issue**

   ```bash
   gh issue create \
     --title "Test Cases: {task_name}" \
     --body "BODY" \
     --label test-cases \
     --milestone N
   ```

9. **Update task** (add Test Cases link)

   Replace `📄 （待创建）` with `📄 #{test_cases_number}`

   ```bash
   gh issue edit {task_number} --body "NEW_BODY"
   ```

10. **Update user story** (add to acceptance criteria)

    Read user story body, append to acceptance criteria:
    - Add `- [ ] [Test Cases #{number}](#{number})`

    ```bash
    gh issue edit {user_story_number} --body "NEW_BODY"
    ```

11. **Report result**
    - Show test cases issue number and URL
    - Confirm task and user story were updated

## Example

For task "Implement Login API Endpoint":

Suggested test cases:
1. User can login with valid email and password
2. Login fails with invalid password (returns 401)
3. Login fails with non-existent email (returns 401)
4. Login returns valid JWT token
5. Login rate limiting works (max 5 attempts per minute)

```bash
gh issue create \
  --title "Test Cases: Login API Endpoint" \
  --body "## Test Cases
- [ ] User can login with valid email and password
- [ ] Login fails with invalid password (returns 401)
- [ ] Login fails with non-existent email (returns 401)
- [ ] Login returns valid JWT token
- [ ] Login rate limiting works (max 5 attempts per minute)

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
