# Skills-New 设计文档

PRD 驱动的研发流程技能套件设计。

## 概述

基于 PRD 文档驱动的简化研发流程，通过 GitHub Issue + Comment 管理完整开发周期。

### 流程图

```
PRD 文档 ─→ issue-prd-review ─┬─→ 通过 → 主 Issue + 子 Issue(s)
                              └─→ 不通过 → 打回产品

子 Issue 流程：
issue-design → issue-tasks → issue-test-cases → issue-implement → issue-pr
                                                                      │
                                                                      └─→ 手动关闭 Issue
```

### 数据模型

| 关系 | 说明 |
|------|------|
| 主 Issue : 子 Issue | 1 : N（Sub-Issue 关联） |
| 子 Issue : Design | 1 : 1 |
| 子 Issue : Task | 1 : N |
| Task : Test Cases | 1 : 1 |
| Task : PR | 1 : 1 |

### 标签规则

| Issue 类型 | 标签 |
|------------|------|
| 主 Issue（PRD） | 无标签 |
| 子 Issue | `feat` / `fix` / `refactor`（根据实际功能判断） |

---

## 目录结构

```
skills-new/
├── shared/
│   └── templates/
│       ├── prd-issue.md           # 主 Issue Body
│       ├── sub-issue.md           # 子 Issue Body
│       ├── review-comment.md      # 技术评估报告 Comment
│       ├── design-comment.md      # Design Comment
│       ├── task-comment.md        # Task Comment
│       ├── test-cases-comment.md  # Test Cases Comment
│       └── pr.md                  # PR 模板
├── issue-prd-review/
│   └── SKILL.md
├── issue-design/
│   └── SKILL.md
├── issue-tasks/
│   └── SKILL.md
├── issue-test-cases/
│   └── SKILL.md
├── issue-implement/
│   └── SKILL.md
└── issue-pr/
    └── SKILL.md
```

---

## 技能设计

### 1. issue-prd-review

**职责**：读取 PRD 文档 → 技术评估 → 通过创建 Issues / 不通过打回

```yaml
name: issue-prd-review
description: 当用户提供 PRD 文档（飞书链接或文本）、提到"评审 PRD"/"需求评估"/"review"时使用。读取 PRD 进行技术评估，通过则创建主 Issue + 子 Issue(s)，不通过则打回给产品。
```

**输入来源**：

| 输入类型 | 处理方式 |
|----------|----------|
| 飞书文档链接 | WebFetch 读取 |
| 文本内容 | 直接使用对话中的 PRD 文本 |
| 本地文件 | Read 工具读取 |

**评估流程**：

1. 需求理解：总结核心目标、关键功能点、边界条件
2. 代码影响分析：搜索相关模块，评估改动范围
3. 工作量评估：small/medium/large/extra-large
4. 爆炸半径评估：isolated/contained/moderate/wide
5. 功能点拆分：识别可独立交付的功能点

**输出**：

| 结果 | 动作 |
|------|------|
| 通过 | 创建主 Issue（Body） + 技术评估 Comment + N 个子 Issue |
| 不通过 | 输出问题清单和修改建议，打回给产品 |

**模板引用**：
- 主 Issue Body: `shared/templates/prd-issue.md`
- 子 Issue Body: `shared/templates/sub-issue.md`
- 技术评估 Comment: `shared/templates/review-comment.md`

---

### 2. issue-design

**职责**：为子 Issue 添加 Design Comment（1:1 关系），包含技术方案和任务拆分

```yaml
name: issue-design
description: 当用户提到"添加设计"/"design"、或从子 Issue 继续流程时使用。调用 brainstorming 完成设计，为子 Issue 添加 Design Comment。
```

**工作流程**：

1. 确认目标子 Issue
2. 读取子 Issue 的 body 获取功能描述
3. 调用 `superpowers:brainstorming`（不创建本地文档）
4. 设计完成后，格式化为 Design Comment
5. `gh issue comment <子issue号> --body "..."`

**注意**：Design 阶段完成任务拆分，输出任务列表供后续 issue-tasks 使用

**模板引用**：`shared/templates/design-comment.md`

---

### 3. issue-tasks

**职责**：读取 Design 中的任务拆分，为每个 Task 生成详细 Comment

```yaml
name: issue-tasks
description: 当用户提到"添加任务"/"tasks"、或从 Design 继续流程时使用。为子 Issue 添加 Task Comment（1:N 关系）。
```

**工作流程**：

1. 确认目标子 Issue
2. 读取 Design Comment，解析任务拆分表
3. 为每个 Task 生成详细 Comment
4. 依次添加到 Issue

**按需读取 Comment**：
```bash
gh api repos/{owner}/{repo}/issues/{issue号}/comments \
  --jq '.[] | select(.body | contains("<!-- type: design -->"))'
```

**模板引用**：`shared/templates/task-comment.md`

---

### 4. issue-test-cases

**职责**：为每个 Task 添加对应的 Test Cases Comment（1:1 关系）

```yaml
name: issue-test-cases
description: 当用户提到"添加用例"/"test cases"、或从 Task 继续流程时使用。为每个 Task 添加 Test Cases Comment。
```

**工作流程**：

1. 确认目标子 Issue
2. 读取 Task Comment(s)
3. 为每个 Task 生成 Test Cases Comment（Web 回归测试 todo-list 形式）
4. 添加到 Issue

**模板引用**：`shared/templates/test-cases-comment.md`

---

### 5. issue-implement

**职责**：根据 Task 详情执行代码实现

```yaml
name: issue-implement
description: 当用户提到"实现"/"implement"/"开发"、或从 Test Cases 继续流程时使用。在 git worktree 中执行 Task 实现。
```

**工作流程**：

1. 确认目标子 Issue 和 Task
2. 按需读取 Comment（Design + Task，**跳过 Test Cases**）
3. 创建 git worktree（`.worktrees/<分支名>`）
4. 调用 `superpowers:subagent-driven-development` 或 `superpowers:executing-plans`
5. 本地验证（测试、构建）

**分支命名**：
```
feat/<issue号>-<task-id>-<简述>
fix/<issue号>-<task-id>-<简述>
refactor/<issue号>-<task-id>-<简述>
```

**Worktree 管理**：
```bash
git worktree add .worktrees/feat-123-task-1-add-login -b feat/123-task-1-add-login
```

---

### 6. issue-pr

**职责**：为 Task 创建 Pull Request（1:1 关系）

```yaml
name: issue-pr
description: 当用户提到"创建 PR"/"提交 PR"/"pull request"、或实现完成后使用。为 Task 创建 PR 关联子 Issue。
```

**工作流程**：

1. 确认目标子 Issue 和 Task
2. 读取 Task Comment（按需过滤）
3. 推送分支到远程
4. 创建 PR，使用 `Related to #子issue号`（不自动关闭）

**关联规则**：
- 所有 PR 统一使用 `Related to #子issue号`
- Issue 手动关闭（所有 Task PR 合并后）

**模板引用**：`shared/templates/pr.md`

---

## Comment 标识约定

用于 `gh api` + `jq` 精准过滤：

```markdown
<!-- type: design -->
<!-- type: task, id: task-1 -->
<!-- type: test-cases, task-id: task-1 -->
```

**过滤示例**：
```bash
# 只读取 Design
gh api repos/{owner}/{repo}/issues/{issue号}/comments \
  --jq '.[] | select(.body | contains("<!-- type: design -->"))'

# 只读取特定 Task
gh api repos/{owner}/{repo}/issues/{issue号}/comments \
  --jq '.[] | select(.body | contains("<!-- type: task, id: task-1 -->"))'
```

---

## Comment 双向链接

Task 和 Test Cases 之间建立双向跳转：

**Task Comment 开头**：
```markdown
<!-- type: task, id: task-{n} -->
<a id="task-{n}"></a>

## 📋 Task {n}: {任务名称}

> 🧪 Test Cases: [跳转](#test-cases-task-{n})
```

**Test Cases Comment 开头**：
```markdown
<!-- type: test-cases, task-id: task-{n} -->
<a id="test-cases-task-{n}"></a>

## 🧪 Test Cases for Task {n}

> 📋 Task: [跳转](#task-{n})
```

---

## 与 superpowers 集成

| 技能 | 集成的 superpowers | 调整 |
|------|-------------------|------|
| issue-design | `superpowers:brainstorming` | 不创建本地文档，输出到 Comment |
| issue-implement | `superpowers:subagent-driven-development` / `superpowers:executing-plans` | 在 worktree 中执行 |
