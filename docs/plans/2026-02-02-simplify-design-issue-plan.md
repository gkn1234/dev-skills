# 简化 Design Issue 流程实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 将 Design Issue 内容合并到 User Story，减少 Issue 数量和追踪复杂度。

**Architecture:** 修改 6 个 skill 文件，移除 Design Issue 创建逻辑，改为更新 User Story 的 Design 区块。Task/Test Cases/PR 的关联从 Design Issue 改为 User Story。

**Tech Stack:** Markdown skill 文件

---

### Task 1: 修改 issue-workflow-user-story 模板

**Files:**
- Modify: `skills/issue-workflow-user-story/SKILL.md:63-91`

**Step 1: 更新 Issue 模板的 Design 区块**

将中文模板的 `## Design` 从占位符改为可直接放内容的格式：

```markdown
## Design
📄 （待填充，使用 `issue-workflow-design` 添加设计）
```

**Step 2: 更新英文模板的 Design 区块**

```markdown
## Design
📄 (To be filled, use `issue-workflow-design` to add design)
```

**Step 3: 更新下游关系说明**

在"上下游关系"表格中，将 `issue-workflow-design` 的说明从"创建后引导做设计"改为"添加设计内容到 User Story"。

**Step 4: Commit**

```bash
git add skills/issue-workflow-user-story/SKILL.md
git commit -m "refactor: 更新 User Story 模板支持直接放置设计内容"
```

---

### Task 2: 重写 issue-workflow-design 流程

**Files:**
- Modify: `skills/issue-workflow-design/SKILL.md` (完全重写)

**Step 1: 更新 description**

```yaml
description: 当用户完成 brainstorming 设计、从用户故事继续流程、或明确提到"添加设计"/"design"时使用
```

**Step 2: 更新 Overview**

```markdown
## Overview

为 User Story 添加设计内容，支持两种模式：简单功能直接写概述，复杂功能链接设计文档。不创建单独的 Design Issue。
```

**Step 3: 重写流程部分**

新流程：
1. 检测仓库
2. 确定 User Story（对话上下文/参数/列表选择）
3. 判断复杂度（Claude 推断，用户确认）
4. 检查设计文档（有则提取概述+链接，无则询问概述）
5. 质量检查
6. 确保文档已提交（如有文档）
7. 更新 User Story（用 `gh issue edit` 更新 body）
8. 引导下一步

**Step 4: 删除 Issue 模板部分**

删除整个 "Issue 模板" 部分（中英文模板），替换为 "Design 内容格式"：

```markdown
## Design 内容格式

根据复杂度判断，生成以下格式之一：

**简单功能（无设计文档）：**
```markdown
## Design
> 简要设计概述，2-3 句话说明技术方案
```

**复杂功能（有设计文档）：**
```markdown
## Design
> **概述**：简要说明设计目标和方案
>
> 📄 [设计文档](https://github.com/{owner}/{repo}/blob/{commit_sha}/docs/plans/xxx-design.md)
```
```

**Step 5: 更新 Common Mistakes**

删除"忘记关联用户故事"（不再需要双向关联），更新其他错误描述。

**Step 6: 更新示例**

更新示例对话，展示更新 User Story 而非创建 Issue 的流程。

**Step 7: 更新上下游关系**

- 删除下游 `issue-workflow-task`（不再是创建 Design Issue）
- 更新说明为"更新 User Story 后引导创建任务"

**Step 8: Commit**

```bash
git add skills/issue-workflow-design/SKILL.md
git commit -m "refactor: 重写 issue-workflow-design 改为更新 User Story"
```

---

### Task 3: 修改 issue-workflow-task

**Files:**
- Modify: `skills/issue-workflow-task/SKILL.md`

**Step 1: 更新 description**

从"从设计文档继续流程"改为"从用户故事继续流程"：

```yaml
description: 当用户完成 writing-plans 计划、从用户故事继续流程、或明确提到"创建任务"/"task issue"时使用
```

**Step 2: 更新 Overview**

将"与设计文档、用户故事的追踪关联"改为"与用户故事的追踪关联"。

**Step 3: 更新流程第 2 步**

将"确定设计文档"改为"确定用户故事"：
- 对话上下文中有：直接使用
- 参数指定：`--user-story N`
- 否则：列出用户故事供选择

**Step 4: 更新流程第 7 步（双向更新）**

从"更新设计文档的 Tasks 列表"改为"更新用户故事的 Tasks 列表"。

**Step 5: 更新 Issue 模板**

删除 `## Design` 字段（`📄 #design_number`），只保留 `## User Story`。

**Step 6: 更新 Common Mistakes**

将"忘记关联设计"改为"忘记关联用户故事"。

**Step 7: 更新示例**

将"关联到设计文档 #43"改为"关联到用户故事 #42"。

**Step 8: 更新上下游关系**

将上游从 `issue-workflow-design` 改为 `issue-workflow-user-story`。

**Step 9: Commit**

```bash
git add skills/issue-workflow-task/SKILL.md
git commit -m "refactor: issue-workflow-task 改为关联 User Story"
```

---

### Task 4: 修改 issue-workflow-test-cases

**Files:**
- Modify: `skills/issue-workflow-test-cases/SKILL.md:33-38`

**Step 1: 更新流程第 3 步**

将"关联的设计文档（可选读取设计内容补充上下文）"改为"关联的用户故事（可选读取 Design 区块补充上下文）"。

**Step 2: Commit**

```bash
git add skills/issue-workflow-test-cases/SKILL.md
git commit -m "refactor: issue-workflow-test-cases 从 User Story 读取设计上下文"
```

---

### Task 5: 修改 issue-workflow-pull-request

**Files:**
- Modify: `skills/issue-workflow-pull-request/SKILL.md`

**Step 1: 更新流程第 3 步**

将"读取 task issue 内容（任务描述、关联的 user story、design、test cases）"改为"读取 task issue 内容（任务描述、关联的 user story、test cases）"。

**Step 2: 更新 PR 模板**

删除 `- Design: #design_number` 行（中英文模板都删除）。

**Step 3: 更新示例**

删除示例中的 `- Design: #43` 行。

**Step 4: Commit**

```bash
git add skills/issue-workflow-pull-request/SKILL.md
git commit -m "refactor: issue-workflow-pull-request 移除 Design Issue 引用"
```

---

### Task 6: 修改 issue-workflow 总览

**Files:**
- Modify: `skills/issue-workflow/SKILL.md`

**Step 1: 更新流程图**

将：
```
Milestone → User Story → Design → Task → Test Cases → Pull Request
```

改为：
```
Milestone → User Story → Task → Test Cases → Pull Request
```

删除 Design 节点，添加说明 Design 内容在 User Story 中。

**Step 2: 更新技能列表**

将 `issue-workflow-design` 的用途从"创建设计文档 Issue"改为"为 User Story 添加设计内容"。

**Step 3: 更新工作流集成表格**

将"设计"阶段的描述改为"`superpowers:brainstorming` → `issue-workflow-design`（更新 User Story）"。

**Step 4: 更新自动行为**

删除标签列表中的 `design`：
从 `user-story`, `design`, `task`, `test-cases`
改为 `user-story`, `task`, `test-cases`

**Step 5: Commit**

```bash
git add skills/issue-workflow/SKILL.md
git commit -m "refactor: 更新 issue-workflow 总览文档"
```

---

### Task 7: 验证和最终提交

**Step 1: 检查所有文件改动**

```bash
git diff HEAD~6 --stat
```

确认修改了 6 个文件。

**Step 2: 搜索遗留的 design_number 引用**

```bash
grep -r "design_number" skills/issue-workflow*/
grep -r "#design" skills/issue-workflow*/
```

应该没有匹配结果。

**Step 3: 完成**

所有改动已通过单独的 commit 提交，无需额外操作。
