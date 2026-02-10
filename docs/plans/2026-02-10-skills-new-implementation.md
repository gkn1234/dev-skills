# Skills-New Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 创建 PRD 驱动的研发流程技能套件（7 个技能 + 7 个模板）

**Architecture:** 技能放在 skills-new/ 目录，共享模板放在 shared/templates/，各技能 SKILL.md 引用模板

**Tech Stack:** Markdown (SKILL.md), GitHub CLI (gh), jq

**Design Doc:** `docs/plans/2026-02-10-skills-new-design.md`

---

## Task 1: 创建目录结构

**Files:**
- Create: `skills-new/shared/templates/.gitkeep`
- Create: `skills-new/issue-workflow/.gitkeep`
- Create: `skills-new/issue-prd-review/.gitkeep`
- Create: `skills-new/issue-design/.gitkeep`
- Create: `skills-new/issue-tasks/.gitkeep`
- Create: `skills-new/issue-test-cases/.gitkeep`
- Create: `skills-new/issue-implement/.gitkeep`
- Create: `skills-new/issue-pr/.gitkeep`

**Step 1: 创建目录结构**

```bash
mkdir -p skills-new/shared/templates
mkdir -p skills-new/issue-workflow
mkdir -p skills-new/issue-prd-review
mkdir -p skills-new/issue-design
mkdir -p skills-new/issue-tasks
mkdir -p skills-new/issue-test-cases
mkdir -p skills-new/issue-implement
mkdir -p skills-new/issue-pr
```

**Step 2: 验证目录创建成功**

```bash
ls -la skills-new/
```

Expected: 显示 shared 和 7 个 issue-* 目录

**Step 3: Commit**

```bash
git add skills-new/
git commit -m "chore: 创建 skills-new 目录结构"
```

---

## Task 2: 创建主 Issue 模板

**Files:**
- Create: `skills-new/shared/templates/prd-issue.md`

**Step 1: 创建模板文件**

```markdown
## 📋 PRD 信息

- **来源**: {prd_source}
- **评审时间**: {review_date}

## 🔗 Sub Issues

```[tasklist]
### 功能拆分
{sub_issues_list}
```
```

**Step 2: 验证文件创建**

```bash
cat skills-new/shared/templates/prd-issue.md
```

**Step 3: Commit**

```bash
git add skills-new/shared/templates/prd-issue.md
git commit -m "feat: 添加主 Issue 模板"
```

---

## Task 3: 创建子 Issue 模板

**Files:**
- Create: `skills-new/shared/templates/sub-issue.md`

**Step 1: 创建模板文件**

```markdown
## 🎯 用户故事

作为 {role}，我希望 {feature}，以便 {value}

## 📋 功能描述

{description}

## 🔧 技术要点

- **涉及模块**: {modules}
- **预估改动**: {scope}

## ✅ 验收标准

{acceptance_criteria}

## 🔗 关联

- 父 PRD: #{parent_issue}
```

**Step 2: 验证文件创建**

```bash
cat skills-new/shared/templates/sub-issue.md
```

**Step 3: Commit**

```bash
git add skills-new/shared/templates/sub-issue.md
git commit -m "feat: 添加子 Issue 模板"
```

---

## Task 4: 创建技术评估报告模板

**Files:**
- Create: `skills-new/shared/templates/review-comment.md`

**Step 1: 创建模板文件**

```markdown
<!-- type: review -->
## 🎯 技术评估报告

### 📋 需求摘要

{requirement_summary}

**关键功能点：**

{feature_points}

### 🔧 推荐方案

**方案名称**: {approach_name}

**技术架构**:

{architecture}

**实现要点**:

{implementation_points}

**优势**: {pros}

**劣势**: {cons}

### 📊 实现规模

| 维度 | 评估 |
|------|------|
| **工作量级别** | {scope_level} |
| **预估改动文件数** | {file_count} |
| **爆炸半径** | {blast_radius} |

**需修改的模块：**

{modules_to_modify}

**需新增的模块：**

{modules_to_add}

### ⚠️ 风险评估

{risks}

### 📝 实现步骤

{implementation_steps}

### 🧪 测试建议

{test_suggestions}

### ❓ 待澄清问题

{clarification_needed}

---

### 📌 评估结论

**状态**: {status}
```

**Step 2: 验证文件创建**

```bash
cat skills-new/shared/templates/review-comment.md
```

**Step 3: Commit**

```bash
git add skills-new/shared/templates/review-comment.md
git commit -m "feat: 添加技术评估报告模板"
```

---

## Task 5: 创建 Design Comment 模板

**Files:**
- Create: `skills-new/shared/templates/design-comment.md`

**Step 1: 创建模板文件**

```markdown
<!-- type: design -->
## 🎨 Design

### 📋 设计概述

{design_summary}

### 🏗️ 技术方案

**架构设计**:

{architecture}

**核心流程**:

{core_flow}

**数据结构**:

{data_structures}

### 📁 文件改动

| 文件 | 改动类型 | 说明 |
|------|----------|------|
{file_changes}

### 📋 任务拆分

| Task ID | 任务名称 | 说明 | 预估 |
|---------|----------|------|------|
{task_breakdown}

### 🔗 相关资源

{related_resources}
```

**Step 2: 验证文件创建**

```bash
cat skills-new/shared/templates/design-comment.md
```

**Step 3: Commit**

```bash
git add skills-new/shared/templates/design-comment.md
git commit -m "feat: 添加 Design Comment 模板"
```

---

## Task 6: 创建 Task Comment 模板

**Files:**
- Create: `skills-new/shared/templates/task-comment.md`

**Step 1: 创建模板文件**

```markdown
<!-- type: task, id: {task_id} -->
<a id="{task_id}"></a>

## 📋 Task {task_number}: {task_name}

> 🧪 Test Cases: [跳转](#test-cases-{task_id})

### 🎯 目标

{task_goal}

### 📝 实现步骤

{implementation_steps}

### 📁 涉及文件

{files_involved}

### ✅ 完成标准

{completion_criteria}
```

**Step 2: 验证文件创建**

```bash
cat skills-new/shared/templates/task-comment.md
```

**Step 3: Commit**

```bash
git add skills-new/shared/templates/task-comment.md
git commit -m "feat: 添加 Task Comment 模板"
```

---

## Task 7: 创建 Test Cases Comment 模板

**Files:**
- Create: `skills-new/shared/templates/test-cases-comment.md`

**Step 1: 创建模板文件**

```markdown
<!-- type: test-cases, task-id: {task_id} -->
<a id="test-cases-{task_id}"></a>

## 🧪 Test Cases for Task {task_number}

> 📋 Task: [跳转](#{task_id})

### 📋 测试范围

{test_scope}

### ✅ 回归测试用例

#### 正常流程

{normal_cases}

#### 边界场景

{boundary_cases}

#### 异常场景

{error_cases}

### 🔗 关联

- Task: {task_id}
```

**Step 2: 验证文件创建**

```bash
cat skills-new/shared/templates/test-cases-comment.md
```

**Step 3: Commit**

```bash
git add skills-new/shared/templates/test-cases-comment.md
git commit -m "feat: 添加 Test Cases Comment 模板"
```

---

## Task 8: 创建 PR 模板

**Files:**
- Create: `skills-new/shared/templates/pr.md`

**Step 1: 创建模板文件**

```markdown
## 📋 Summary

{summary}

## 🔗 关联

- Issue: #{issue_number}
- Task: {task_id}

Related to #{issue_number}

## 📝 改动说明

{changes}

## ✅ Checklist

- [ ] 代码自测通过
- [ ] 符合 Task 完成标准
```

**Step 2: 验证文件创建**

```bash
cat skills-new/shared/templates/pr.md
```

**Step 3: Commit**

```bash
git add skills-new/shared/templates/pr.md
git commit -m "feat: 添加 PR 模板"
```

---

## Task 9: 创建 issue-workflow SKILL.md

**Files:**
- Create: `skills-new/issue-workflow/SKILL.md`

**Step 1: 创建 SKILL.md**

```markdown
---
name: issue-workflow
description: 当用户提到"研发流程"/"开发流程"/"workflow"、或需要了解整体工作流时使用。自动检测当前阶段并引导下一步操作。
---

# Issue Workflow - PRD 驱动研发流程

## Overview

基于 PRD 文档驱动的研发流程管理。自动检测当前阶段，引导下一步操作。

## 流程概览

```
一无所有
    │
    ▼
issue-prd-review ─→ 主 Issue + 评估 Comment + 子 Issue(s)
    │
    ▼ (对每个子 Issue)
issue-design ─→ Design Comment
    │
    ▼
issue-tasks ─→ Task Comment(s)
    │
    ▼
issue-test-cases ─→ Test Cases Comment(s)
    │
    ▼ (对每个 Task)
issue-implement ─→ 代码实现
    │
    ▼
issue-pr ─→ Pull Request
    │
    ▼
手动合并 ─→ 手动关闭 Issue
```

## 技能列表

| 技能 | 触发条件 | 用途 |
|------|----------|------|
| `issue-prd-review` | "评审 PRD"/"需求评估"/"review" | PRD 评估与 Issue 创建 |
| `issue-design` | "添加设计"/"design" | 添加 Design Comment |
| `issue-tasks` | "添加任务"/"tasks" | 添加 Task Comment |
| `issue-test-cases` | "添加用例"/"test cases" | 添加 Test Cases Comment |
| `issue-implement` | "实现"/"implement"/"开发" | 在 worktree 中执行实现 |
| `issue-pr` | "创建 PR"/"pull request" | 创建 Pull Request |

## 状态检测

### 第一层：主 Issue 检测

| 状态 | 判断条件 | 下一步 |
|------|----------|--------|
| 一无所有 | 无 PRD Issue | → issue-prd-review |
| 待评估 | 有主 Issue，无评估 Comment | → issue-prd-review（继续评估） |
| 待拆分 | 有评估 Comment，无子 Issue | → issue-prd-review（创建子 Issues） |
| 已拆分 | 有子 Issues | → 进入子 Issue 流程 |

### 第二层：子 Issue 检测

| 已有 Comment | 当前阶段 | 下一步 |
|--------------|----------|--------|
| 无 | 待设计 | → issue-design |
| design | 待拆分任务 | → issue-tasks |
| design, task | 待添加用例 | → issue-test-cases |
| design, task, test-cases | 待实现 | → issue-implement |
| 已有 PR | 待合并 | 手动合并 → 手动关闭 Issue |

### 状态检测命令

```bash
# 检测子 Issue 的 Comment 类型
gh api repos/{owner}/{repo}/issues/{issue号}/comments \
  --jq '[.[] | .body | capture("<!-- type: (?<type>[^,>]+)") | .type] | unique'
```

## 数据模型

| 关系 | 说明 |
|------|------|
| 主 Issue : 子 Issue | 1 : N（Sub-Issue 关联） |
| 子 Issue : Design | 1 : 1 |
| 子 Issue : Task | 1 : N |
| Task : Test Cases | 1 : 1 |
| Task : PR | 1 : 1 |

## 标签规则

| Issue 类型 | 标签 |
|------------|------|
| 主 Issue（PRD） | 无标签 |
| 子 Issue | `feat` / `fix` / `refactor` |
```

**Step 2: 验证文件创建**

```bash
cat skills-new/issue-workflow/SKILL.md
```

**Step 3: Commit**

```bash
git add skills-new/issue-workflow/SKILL.md
git commit -m "feat: 添加 issue-workflow 技能"
```

---

## Task 10: 创建 issue-prd-review SKILL.md

**Files:**
- Create: `skills-new/issue-prd-review/SKILL.md`

**Step 1: 创建 SKILL.md**

```markdown
---
name: issue-prd-review
description: 当用户提供 PRD 文档（飞书链接或文本）、提到"评审 PRD"/"需求评估"/"review"时使用。读取 PRD 进行技术评估，通过则创建主 Issue + 子 Issue(s)，不通过则打回给产品。
---

# Issue PRD Review - PRD 评估与 Issue 创建

## Overview

读取 PRD 文档，进行技术评估。通过则创建主 Issue + 子 Issue(s)，不通过则打回给产品。

## 输入来源

| 输入类型 | 处理方式 |
|----------|----------|
| 飞书文档链接 | WebFetch 读取 |
| 文本内容 | 直接使用对话中的 PRD 文本 |
| 本地文件 | Read 工具读取 |

## 评估流程

1. **需求理解**：总结核心目标、关键功能点、边界条件
2. **代码影响分析**：搜索相关模块，评估改动范围
3. **工作量评估**：small/medium/large/extra-large
4. **爆炸半径评估**：isolated/contained/moderate/wide
5. **功能点拆分**：识别可独立交付的功能点

## 评估结果

| 结果 | 动作 |
|------|------|
| 通过 | 创建主 Issue + 技术评估 Comment + 子 Issue(s) |
| 不通过 | 输出问题清单和修改建议，打回给产品 |

## 操作命令

```bash
# 创建主 Issue
gh issue create --title "[PRD] {需求名称}" --body "$(cat <<'EOF'
{主 Issue Body，参考模板}
EOF
)"

# 添加技术评估 Comment
gh issue comment {主issue号} --body "$(cat <<'EOF'
{技术评估报告，参考模板}
EOF
)"

# 创建子 Issue 并关联父 Issue
gh issue create --title "[Story] {功能点}" --body "..." --label feat --parent {主issue号}
```

## 模板

- 主 Issue Body: `../shared/templates/prd-issue.md`
- 子 Issue Body: `../shared/templates/sub-issue.md`
- 技术评估 Comment: `../shared/templates/review-comment.md`
```

**Step 2: 验证文件创建**

```bash
cat skills-new/issue-prd-review/SKILL.md
```

**Step 3: Commit**

```bash
git add skills-new/issue-prd-review/SKILL.md
git commit -m "feat: 添加 issue-prd-review 技能"
```

---

## Task 11: 创建 issue-design SKILL.md

**Files:**
- Create: `skills-new/issue-design/SKILL.md`

**Step 1: 创建 SKILL.md**

```markdown
---
name: issue-design
description: 当用户提到"添加设计"/"design"、或从子 Issue 继续流程时使用。调用 brainstorming 完成设计，为子 Issue 添加 Design Comment（含任务拆分）。
---

# Issue Design - 添加设计方案

## Overview

为子 Issue 添加 Design Comment（1:1 关系）。使用 brainstorming 完成设计，包含技术方案和任务拆分。

## 工作流程

1. 确认目标子 Issue
2. 读取子 Issue 的 body 获取功能描述
3. 调用 `superpowers:brainstorming`（**不创建本地文档**）
4. 设计完成后，格式化为 Design Comment
5. 添加 Comment 到 Issue

## 前置检查

1. 确认目标是子 Issue（通过父 Issue 关联判断）
2. 检查是否已存在 Design Comment（避免重复）

```bash
# 检查是否已有 Design Comment
gh api repos/{owner}/{repo}/issues/{issue号}/comments \
  --jq '.[] | select(.body | contains("<!-- type: design -->"))' | head -1
```

## 与 brainstorming 集成

| brainstorming 默认行为 | issue-design 调整 |
|------------------------|-------------------|
| 写入 `docs/plans/YYYY-MM-DD-<topic>-design.md` | 跳过，不创建本地文件 |
| 提交设计文档到 git | 跳过 |
| 输出设计内容 | 格式化后添加为 Issue Comment |

## 操作命令

```bash
# 添加 Design Comment
gh issue comment {子issue号} --body "$(cat <<'EOF'
{Design Comment，参考模板}
EOF
)"
```

## 模板

- Design Comment: `../shared/templates/design-comment.md`

## 注意

Design 阶段必须完成**任务拆分**，输出任务列表供后续 issue-tasks 使用。
```

**Step 2: 验证文件创建**

```bash
cat skills-new/issue-design/SKILL.md
```

**Step 3: Commit**

```bash
git add skills-new/issue-design/SKILL.md
git commit -m "feat: 添加 issue-design 技能"
```

---

## Task 12: 创建 issue-tasks SKILL.md

**Files:**
- Create: `skills-new/issue-tasks/SKILL.md`

**Step 1: 创建 SKILL.md**

```markdown
---
name: issue-tasks
description: 当用户提到"添加任务"/"tasks"、或从 Design 继续流程时使用。读取 Design 中的任务拆分，为子 Issue 添加 Task Comment（1:N 关系）。
---

# Issue Tasks - 添加任务

## Overview

读取 Design Comment 中的任务拆分，为每个 Task 生成详细 Comment。

## 工作流程

1. 确认目标子 Issue
2. 读取 Design Comment，解析任务拆分表
3. 为每个 Task 生成详细 Comment
4. 依次添加到 Issue

## 按需读取 Comment

```bash
# 只读取 Design Comment（节省上下文）
gh api repos/{owner}/{repo}/issues/{issue号}/comments \
  --jq '.[] | select(.body | contains("<!-- type: design -->")) | .body'
```

## 操作命令

```bash
# 为每个 Task 添加 Comment
gh issue comment {子issue号} --body "$(cat <<'EOF'
{Task Comment，参考模板}
EOF
)"
```

## 模板

- Task Comment: `../shared/templates/task-comment.md`

## Comment 标识

每个 Task Comment 必须包含标识，用于后续过滤：

```markdown
<!-- type: task, id: task-{n} -->
```
```

**Step 2: 验证文件创建**

```bash
cat skills-new/issue-tasks/SKILL.md
```

**Step 3: Commit**

```bash
git add skills-new/issue-tasks/SKILL.md
git commit -m "feat: 添加 issue-tasks 技能"
```

---

## Task 13: 创建 issue-test-cases SKILL.md

**Files:**
- Create: `skills-new/issue-test-cases/SKILL.md`

**Step 1: 创建 SKILL.md**

```markdown
---
name: issue-test-cases
description: 当用户提到"添加用例"/"test cases"、或从 Task 继续流程时使用。为每个 Task 添加 Test Cases Comment（Task:Test Cases = 1:1）。
---

# Issue Test Cases - 添加测试用例

## Overview

为每个 Task 添加对应的 Test Cases Comment（1:1 关系）。测试用例采用 Web 回归测试 todo-list 形式。

## 工作流程

1. 确认目标子 Issue
2. 读取 Task Comment(s)
3. 为每个 Task 生成 Test Cases Comment
4. 添加到 Issue

## 按需读取 Comment

```bash
# 只读取 Task Comments
gh api repos/{owner}/{repo}/issues/{issue号}/comments \
  --jq '.[] | select(.body | contains("<!-- type: task,")) | .body'
```

## 操作命令

```bash
# 为每个 Task 添加 Test Cases Comment
gh issue comment {子issue号} --body "$(cat <<'EOF'
{Test Cases Comment，参考模板}
EOF
)"
```

## 模板

- Test Cases Comment: `../shared/templates/test-cases-comment.md`

## Comment 标识

每个 Test Cases Comment 必须包含标识：

```markdown
<!-- type: test-cases, task-id: task-{n} -->
```

## 双向链接

Task 和 Test Cases 之间建立双向跳转：

- Task Comment: `> 🧪 Test Cases: [跳转](#test-cases-task-{n})`
- Test Cases Comment: `> 📋 Task: [跳转](#task-{n})`
```

**Step 2: 验证文件创建**

```bash
cat skills-new/issue-test-cases/SKILL.md
```

**Step 3: Commit**

```bash
git add skills-new/issue-test-cases/SKILL.md
git commit -m "feat: 添加 issue-test-cases 技能"
```

---

## Task 14: 创建 issue-implement SKILL.md

**Files:**
- Create: `skills-new/issue-implement/SKILL.md`

**Step 1: 创建 SKILL.md**

```markdown
---
name: issue-implement
description: 当用户提到"实现"/"implement"/"开发"、或从 Test Cases 继续流程时使用。在 git worktree 中执行 Task 实现（Task:实现 = 1:1）。
---

# Issue Implement - 执行实现

## Overview

根据 Task 详情在 git worktree 中执行代码实现。

## 工作流程

1. 确认目标子 Issue 和 Task
2. 按需读取 Comment（Design + Task，**跳过 Test Cases**）
3. 创建 git worktree（`.worktrees/<分支名>`）
4. 调用 superpowers 执行实现
5. 本地验证（测试、构建）

## 按需读取 Comment

```bash
# 只读取 Design Comment
gh api repos/{owner}/{repo}/issues/{issue号}/comments \
  --jq '.[] | select(.body | contains("<!-- type: design -->")) | .body'

# 只读取特定 Task Comment
gh api repos/{owner}/{repo}/issues/{issue号}/comments \
  --jq '.[] | select(.body | contains("<!-- type: task, id: task-1 -->")) | .body'
```

**注意**：实现时**跳过 Test Cases Comment**，节省上下文。

## 分支命名

```
feat/<issue号>-<task-id>-<简述>
fix/<issue号>-<task-id>-<简述>
refactor/<issue号>-<task-id>-<简述>
```

## Worktree 管理

```bash
# 创建 worktree
git worktree add .worktrees/feat-123-task-1-add-login -b feat/123-task-1-add-login

# 切换到 worktree
cd .worktrees/feat-123-task-1-add-login
```

## 与 superpowers 集成

| 场景 | 使用技能 |
|------|----------|
| 多个独立步骤可并行 | `superpowers:subagent-driven-development` |
| 顺序执行的实现计划 | `superpowers:executing-plans` |

## 完成标准

- [ ] 代码符合 Task Comment 中的完成标准
- [ ] 本地测试通过
- [ ] 构建无错误
```

**Step 2: 验证文件创建**

```bash
cat skills-new/issue-implement/SKILL.md
```

**Step 3: Commit**

```bash
git add skills-new/issue-implement/SKILL.md
git commit -m "feat: 添加 issue-implement 技能"
```

---

## Task 15: 创建 issue-pr SKILL.md

**Files:**
- Create: `skills-new/issue-pr/SKILL.md`

**Step 1: 创建 SKILL.md**

```markdown
---
name: issue-pr
description: 当用户提到"创建 PR"/"提交 PR"/"pull request"、或实现完成后使用。为 Task 创建 PR 关联子 Issue（Task:PR = 1:1）。
---

# Issue PR - 创建 Pull Request

## Overview

为 Task 创建 Pull Request，关联子 Issue。

## 工作流程

1. 确认目标子 Issue 和 Task
2. 读取 Task Comment（按需过滤）
3. 推送分支到远程
4. 创建 PR，使用 `Related to #子issue号`

## 按需读取 Comment

```bash
# 只读取特定 Task Comment
gh api repos/{owner}/{repo}/issues/{issue号}/comments \
  --jq '.[] | select(.body | contains("<!-- type: task, id: task-1 -->")) | .body'
```

## 操作命令

```bash
# 推送分支
git push -u origin feat/123-task-1-add-login

# 创建 PR
gh pr create \
  --title "{Task 名称} (#{子issue号})" \
  --body "$(cat <<'EOF'
{PR 内容，参考模板}
EOF
)" \
  --base main
```

## 关联规则

- 所有 PR 统一使用 `Related to #子issue号`（不自动关闭）
- Issue 手动关闭（所有 Task PR 合并后）

## 模板

- PR: `../shared/templates/pr.md`
```

**Step 2: 验证文件创建**

```bash
cat skills-new/issue-pr/SKILL.md
```

**Step 3: Commit**

```bash
git add skills-new/issue-pr/SKILL.md
git commit -m "feat: 添加 issue-pr 技能"
```

---

## Task 16: 最终验证与汇总提交

**Step 1: 验证目录结构**

```bash
find skills-new -type f | sort
```

Expected:
```
skills-new/issue-design/SKILL.md
skills-new/issue-implement/SKILL.md
skills-new/issue-pr/SKILL.md
skills-new/issue-prd-review/SKILL.md
skills-new/issue-tasks/SKILL.md
skills-new/issue-test-cases/SKILL.md
skills-new/issue-workflow/SKILL.md
skills-new/shared/templates/design-comment.md
skills-new/shared/templates/pr.md
skills-new/shared/templates/prd-issue.md
skills-new/shared/templates/review-comment.md
skills-new/shared/templates/sub-issue.md
skills-new/shared/templates/task-comment.md
skills-new/shared/templates/test-cases-comment.md
```

**Step 2: 验证所有文件可读**

```bash
for f in $(find skills-new -name "*.md"); do
  echo "=== $f ==="
  head -5 "$f"
done
```

**Step 3: 查看 git log 确认所有提交**

```bash
git log --oneline -15
```
