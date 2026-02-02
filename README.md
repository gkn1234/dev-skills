# Dev Skills

A collection of Claude Code skills for development workflows.

[中文文档](./README.zh-CN.md)

## Introduction

Dev Skills is a collection of Claude Code skills for enhancing development workflows. Currently includes the `issue-workflow` skill for GitHub Issue-based development workflow management.

## Skills

### issue-workflow

GitHub Issue-based development workflow management.

**Features:**
- Complete workflow: Milestone → User Story → Task → Test Cases → Pull Request
- Auto-create labels and bidirectional linking
- Bilingual templates (zh/en, auto-detected)
- Deep integration with [superpowers](https://github.com/anthropics/claude-code-superpowers) skills
- Permanent links using commit SHA for design docs and implementation plans
- Built-in quality checks for each workflow step

**Workflow Overview:**

```
Milestone → User Story → Task → Test Cases → Pull Request
    │           │          │         │            │
    │           │          │         │            └── Auto-close Task on merge
    │           │          │         └── Acceptance tests (linked to Task/User Story)
    │           │          └── Implementation units (N:1 with User Story)
    │           └── User stories (N:1 with Milestone, contains design)
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

| Skill | Trigger | Purpose |
|-------|---------|---------|
| `/issue-workflow` | "workflow"/"issue management" | Workflow overview |
| `/issue-workflow-milestone` | "milestone"/"new phase" | Create GitHub milestone |
| `/issue-workflow-user-story` | "user story"/"I want to..." | Create user story issue |
| `/issue-workflow-design` | After brainstorming/"design doc" | Add design to User Story |
| `/issue-workflow-task` | After writing-plans/"create task" | Create task issue |
| `/issue-workflow-test-cases` | After task/"test cases" | Create test cases issue |
| `/issue-workflow-pull-request` | "create PR"/"pull request" | Create PR linked to tasks |

**Typical Workflow:**

1. **Create milestone**: Create a milestone for new requirements
   ```
   /issue-workflow-milestone
   ```

2. **Create user story**: Break down requirements into user stories
   ```
   /issue-workflow-user-story
   ```

3. **Design phase**: Complete design with brainstorming, then add to User Story
   ```
   /superpowers:brainstorming
   /issue-workflow-design
   ```

4. **Task breakdown**: Write plan with writing-plans, then create Task Issue
   ```
   /superpowers:writing-plans
   /issue-workflow-task
   ```

5. **Create test cases**: Create acceptance test cases for the task
   ```
   /issue-workflow-test-cases
   ```

6. **Create pull request**: After implementation, create PR linked to tasks
   ```
   /issue-workflow-pull-request
   ```

## License

MIT
