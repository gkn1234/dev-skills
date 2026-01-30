# Dev Skills

A collection of Claude Code skills for development workflows.

[中文文档](#中文文档) | [English](#english)

---

## 中文文档

### 简介

Dev Skills 是一个 Claude Code 技能集合，用于增强开发工作流程。目前包含 `issue-workflow` 技能，帮助团队基于 GitHub Issue 进行规范化的研发流程管理。

### Skills

#### issue-workflow

基于 GitHub Issue 的研发流程管理技能。

**功能特性：**
- 完整的研发流程：Milestone → User Story → Design → Task → Test Cases
- 自动创建标签并建立双向链接
- 双语模板支持（中/英文，自动检测）
- 与 [superpowers](https://github.com/anthropics/claude-code-superpowers) 技能深度集成

**流程概览：**

```
Milestone → User Story → Design → Task → Test Cases
    │           │           │        │         │
    │           │           │        │         └── 验收用例 (与 Task 1:1)
    │           │           │        └── 实现任务 (与 Design N:1)
    │           │           └── 设计文档 (与 User Story 1:1)
    │           └── 用户故事 (与 Milestone N:1)
    └── GitHub 原生里程碑功能
```

### 安装

```bash
# 克隆到 Claude Code skills 目录
git clone https://github.com/gvtroutmain/dev-skills.git ~/.claude/skills/dev-skills
```

### 更新

```bash
# 进入 skills 目录并拉取最新代码
cd ~/.claude/skills/dev-skills && git pull
```

### 依赖

本技能与 [superpowers](https://github.com/anthropics/claude-code-superpowers) 技能集成，建议同时安装：

```bash
# 安装 superpowers（如果尚未安装）
git clone https://github.com/anthropics/claude-code-superpowers.git ~/.claude/skills/superpowers
```

**相关技能：**
- `superpowers:brainstorming` - 用于设计阶段的头脑风暴
- `superpowers:writing-plans` - 用于编写详细的实现计划

### 使用方法

**子命令列表：**

| 命令 | 用途 |
|------|------|
| `/dev-skills:issue-workflow` | 查看流程概览 |
| `/dev-skills:issue-workflow:create-milestone` | 创建 GitHub 里程碑 |
| `/dev-skills:issue-workflow:create-user-story` | 创建用户故事 Issue |
| `/dev-skills:issue-workflow:create-design` | 创建设计文档 Issue |
| `/dev-skills:issue-workflow:create-task` | 创建任务 Issue |
| `/dev-skills:issue-workflow:create-test-cases` | 创建测试用例 Issue |

**典型工作流：**

1. **创建里程碑**：为新需求创建里程碑
   ```
   /dev-skills:issue-workflow:create-milestone
   ```

2. **创建用户故事**：将需求拆分为用户故事
   ```
   /dev-skills:issue-workflow:create-user-story
   ```

3. **设计阶段**：使用 brainstorming 完成设计，然后创建 Design Issue
   ```
   /superpowers:brainstorming
   /dev-skills:issue-workflow:create-design
   ```

4. **任务拆分**：使用 writing-plans 编写计划，然后创建 Task Issue
   ```
   /superpowers:writing-plans
   /dev-skills:issue-workflow:create-task
   ```

5. **创建测试用例**：为任务创建验收测试用例
   ```
   /dev-skills:issue-workflow:create-test-cases
   ```

### 自动行为

- **标签管理**：自动检查并创建缺失的标签（`user-story`, `design`, `task`, `test-cases`）
- **双向链接**：自动在相关 Issue 间建立双向链接
- **语言检测**：根据用户对话语言自动选择中/英文模板
- **仓库检测**：优先从 `git remote` 自动检测仓库，失败时询问用户

### 优先级规则

对于所有输入（milestone, user-story, design, task）：
1. 优先使用当前对话上下文中的信息
2. 其次使用命令参数（如 `--milestone 1`）
3. 最后查询 GitHub API 并展示选项列表供选择

---

## English

### Introduction

Dev Skills is a collection of Claude Code skills for enhancing development workflows. Currently includes the `issue-workflow` skill for GitHub Issue-based development workflow management.

### Skills

#### issue-workflow

GitHub Issue-based development workflow management.

**Features:**
- Complete workflow: Milestone → User Story → Design → Task → Test Cases
- Auto-create labels and bidirectional linking
- Bilingual templates (zh/en, auto-detected)
- Deep integration with [superpowers](https://github.com/anthropics/claude-code-superpowers) skills

### Installation

```bash
# Clone to Claude Code skills directory
git clone https://github.com/gvtroutmain/dev-skills.git ~/.claude/skills/dev-skills
```

### Update

```bash
# Navigate to skills directory and pull latest
cd ~/.claude/skills/dev-skills && git pull
```

### Dependencies

This skill integrates with [superpowers](https://github.com/anthropics/claude-code-superpowers). Recommended to install:

```bash
# Install superpowers (if not already installed)
git clone https://github.com/anthropics/claude-code-superpowers.git ~/.claude/skills/superpowers
```

**Related skills:**
- `superpowers:brainstorming` - For design phase brainstorming
- `superpowers:writing-plans` - For writing detailed implementation plans

### Usage

**Sub-commands:**

| Command | Purpose |
|---------|---------|
| `/dev-skills:issue-workflow` | Workflow overview |
| `/dev-skills:issue-workflow:create-milestone` | Create GitHub milestone |
| `/dev-skills:issue-workflow:create-user-story` | Create user story issue |
| `/dev-skills:issue-workflow:create-design` | Create design issue |
| `/dev-skills:issue-workflow:create-task` | Create task issue |
| `/dev-skills:issue-workflow:create-test-cases` | Create test cases issue |

## License

MIT
