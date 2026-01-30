# Dev Skills

用于增强开发工作流程的 Claude Code 技能集合。

[English](./README.md)

## 简介

Dev Skills 是一个 Claude Code 技能集合，用于增强开发工作流程。目前包含 `issue-workflow` 技能，帮助团队基于 GitHub Issue 进行规范化的研发流程管理。

## Skills

### issue-workflow

基于 GitHub Issue 的研发流程管理技能。

**功能特性：**
- 完整的研发流程：Milestone → User Story → Design → Task → Test Cases → Pull Request
- 自动创建标签并建立双向链接
- 双语模板支持（中/英文，自动检测）
- 与 [superpowers](https://github.com/anthropics/claude-code-superpowers) 技能深度集成
- 使用 commit SHA 生成永久链接，避免分支删除后链接失效
- 每个流程步骤内置质量检查

**流程概览：**

```
Milestone → User Story → Design → Task → Test Cases → Pull Request
    │           │           │        │         │            │
    │           │           │        │         │            └── 合并后自动关闭 Task
    │           │           │        │         └── 验收用例 (与 Task/User Story 关联)
    │           │           │        └── 实现任务 (与 Design N:1)
    │           │           └── 设计文档 (与 User Story 1:1)
    │           └── 用户故事 (与 Milestone N:1)
    └── GitHub 原生里程碑功能
```

## 安装

```bash
# 添加 marketplace
claude plugin marketplace add gkn1234/dev-skills

# 安装插件
claude plugin install dev-skills@dev-skills
```

## 更新

```bash
# 更新 marketplace 并重新安装
claude plugin marketplace update dev-skills
claude plugin update dev-skills@dev-skills
```

## 依赖

本技能与 [superpowers](https://github.com/obra/superpowers) 技能集成，建议同时安装

**相关技能：**
- `superpowers:brainstorming` - 用于设计阶段的头脑风暴
- `superpowers:writing-plans` - 用于编写详细的实现计划

## 使用方法

**技能列表：**

| 技能 | 触发条件 | 用途 |
|------|----------|------|
| `/issue-workflow` | "研发流程"/"issue 管理" | 查看流程概览 |
| `/issue-workflow-milestone` | "里程碑"/"新阶段" | 创建 GitHub 里程碑 |
| `/issue-workflow-user-story` | "用户故事"/"我想要..." | 创建用户故事 Issue |
| `/issue-workflow-design` | 完成 brainstorming 后/"设计文档" | 创建设计文档 Issue |
| `/issue-workflow-task` | 完成 writing-plans 后/"创建任务" | 创建任务 Issue |
| `/issue-workflow-test-cases` | 从任务继续/"测试用例" | 创建测试用例 Issue |
| `/issue-workflow-pull-request` | "创建 PR"/"提交 PR" | 创建关联任务的 PR |

**典型工作流：**

1. **创建里程碑**：为新需求创建里程碑
   ```
   /issue-workflow-milestone
   ```

2. **创建用户故事**：将需求拆分为用户故事
   ```
   /issue-workflow-user-story
   ```

3. **设计阶段**：使用 brainstorming 完成设计，然后创建 Design Issue
   ```
   /superpowers:brainstorming
   /issue-workflow-design
   ```

4. **任务拆分**：使用 writing-plans 编写计划，然后创建 Task Issue
   ```
   /superpowers:writing-plans
   /issue-workflow-task
   ```

5. **创建测试用例**：为任务创建验收测试用例
   ```
   /issue-workflow-test-cases
   ```

6. **创建 Pull Request**：完成实现后，创建关联任务的 PR
   ```
   /issue-workflow-pull-request
   ```

## License

MIT
