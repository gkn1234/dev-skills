# 简化 Design Issue 流程设计

## 概述

将 Design Issue 的内容合并到 User Story 中，减少 Issue 数量，简化追踪。

## 动机

- **减少 Issue 数量** - 一个功能对应太多 Issue 太碎片化
- **简化追踪** - 不想在多个 Issue 之间跳转查看信息

## 设计决策

### 1. Design 内容放置方式

User Story 中的 `## Design` 区块支持两种格式：

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

### 2. 复杂度判断

- 由 Claude 根据功能复杂度推断
- 用户确认或调整

### 3. 技能职责

- `issue-workflow-user-story` - 创建 User Story（Design 区块初始为空）
- `issue-workflow-design` - 为已有的 User Story 添加/更新设计内容（不创建单独 Issue）

### 4. 设计上下文读取

`issue-workflow-test-cases` 保持读取设计上下文的功能，来源从 Design Issue 改为 User Story 的 `## Design` 区块。

## 影响范围

### 需要修改的文件

| 文件 | 改动 |
|------|------|
| `issue-workflow-user-story/SKILL.md` | 模板 `## Design` 改为可直接放内容 |
| `issue-workflow-design/SKILL.md` | 改为更新 User Story；删除 Issue 模板；添加复杂度判断 |
| `issue-workflow-task/SKILL.md` | 上游改为 User Story；删除 `## Design` 字段；双向更新改为 User Story |
| `issue-workflow-test-cases/SKILL.md` | 设计上下文从 User Story 读取 |
| `issue-workflow-pull-request/SKILL.md` | 删除 `Design: #design_number`；设计信息从 User Story 获取 |
| `issue-workflow/SKILL.md` | 更新流程图；删除 `design` 标签；更新技能描述 |

### 删除的内容

- Design Issue 模板（中英文）
- `design` 标签相关逻辑
- 所有 `#design_number` 引用
- 双向关联逻辑（Design ↔ User Story）

### 流程变化

| 原流程 | 新流程 |
|--------|--------|
| 创建 Design Issue | 更新 User Story 的 `## Design` 区块 |
| Task 关联到 Design Issue | Task 关联到 User Story |
| Task 双向更新 Design Issue | Task 双向更新 User Story |
| PR 读取 Design Issue 编号 | PR 从 User Story 获取设计信息 |

## issue-workflow-design 新流程

1. 检测仓库
2. 确定 User Story（对话上下文/参数/列表选择）
3. **判断复杂度** - Claude 推断，用户确认
4. 检查设计文档（有则提取概述+链接，无则询问概述）
5. 质量检查（保持原有标准）
6. 确保文档已提交（如有文档）
7. **更新 User Story** - 用 `gh issue edit` 更新 body
8. 引导下一步 → `issue-workflow-task`

## 新流程图

```
Milestone → User Story → Task → Test Cases → Pull Request
    │           │          │         │            │
    │           │          │         │            └── 合并后自动关闭 Task
    │           │          │         └── 验收用例 (与 Task/User Story 关联)
    │           │          └── 实现任务 (与 User Story N:1)
    │           └── 用户故事 + 设计内容 (与 Milestone N:1)
    └── GitHub 原生里程碑功能

Design 内容通过 issue-workflow-design 添加到 User Story 中
```
