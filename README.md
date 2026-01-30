# Dev Skills

A collection of Claude Code skills for development workflows.

[中文文档](./README.zh-CN.md)

## Introduction

Dev Skills is a collection of Claude Code skills for enhancing development workflows. Currently includes the `issue-workflow` skill for GitHub Issue-based development workflow management.

## Skills

### issue-workflow

GitHub Issue-based development workflow management.

**Features:**
- Complete workflow: Milestone → User Story → Design → Task → Test Cases
- Auto-create labels and bidirectional linking
- Bilingual templates (zh/en, auto-detected)
- Deep integration with [superpowers](https://github.com/anthropics/claude-code-superpowers) skills

**Workflow Overview:**

```
Milestone → User Story → Design → Task → Test Cases
    │           │           │        │         │
    │           │           │        │         └── Acceptance tests (1:1 with Task)
    │           │           │        └── Implementation units (N:1 with Design)
    │           │           └── Design doc (1:1 with User Story)
    │           └── User stories (N:1 with Milestone)
    └── GitHub native milestone feature
```

## Installation

```bash
# Add marketplace
claude plugin marketplace add gkn1234/dev-skills

# Install plugin
claude plugin install dev-skills@dev-skills
```

## Update

```bash
# Update marketplace and reinstall
claude plugin marketplace update dev-skills
claude plugin update dev-skills@dev-skills
```

## Dependencies

This skill integrates with [superpowers](https://github.com/obra/superpowers). Recommended to install

**Related skills:**
- `superpowers:brainstorming` - For design phase brainstorming
- `superpowers:writing-plans` - For writing detailed implementation plans

## Usage

**Skills:**

| Skill | Purpose |
|-------|---------|
| `/dev-skills:issue-workflow` | Workflow overview |
| `/dev-skills:issue-workflow-milestone` | Create GitHub milestone |
| `/dev-skills:issue-workflow-user-story` | Create user story issue |
| `/dev-skills:issue-workflow-design` | Create design issue |
| `/dev-skills:issue-workflow-task` | Create task issue |
| `/dev-skills:issue-workflow-test-cases` | Create test cases issue |

**Typical Workflow:**

1. **Create milestone**: Create a milestone for new requirements
   ```
   /dev-skills:issue-workflow-milestone
   ```

2. **Create user story**: Break down requirements into user stories
   ```
   /dev-skills:issue-workflow-user-story
   ```

3. **Design phase**: Complete design with brainstorming, then create Design Issue
   ```
   /superpowers:brainstorming
   /dev-skills:issue-workflow-design
   ```

4. **Task breakdown**: Write plan with writing-plans, then create Task Issue
   ```
   /superpowers:writing-plans
   /dev-skills:issue-workflow-task
   ```

5. **Create test cases**: Create acceptance test cases for the task
   ```
   /dev-skills:issue-workflow-test-cases
   ```

## License

MIT
