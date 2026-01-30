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
# Clone to Claude Code skills directory
git clone https://github.com/gkn1234/dev-skills.git ~/.claude/skills/dev-skills
```

## Update

```bash
# Navigate to skills directory and pull latest
cd ~/.claude/skills/dev-skills && git pull
```

## Dependencies

This skill integrates with [superpowers](https://github.com/obra/superpowers). Recommended to install:

```bash
# Install superpowers (if not already installed)
git clone https://github.com/obra/superpowers.git ~/.claude/skills/superpowers
```

**Related skills:**
- `superpowers:brainstorming` - For design phase brainstorming
- `superpowers:writing-plans` - For writing detailed implementation plans

## Usage

**Sub-commands:**

| Command | Purpose |
|---------|---------|
| `/dev-skills:issue-workflow` | Workflow overview |
| `/dev-skills:issue-workflow:create-milestone` | Create GitHub milestone |
| `/dev-skills:issue-workflow:create-user-story` | Create user story issue |
| `/dev-skills:issue-workflow:create-design` | Create design issue |
| `/dev-skills:issue-workflow:create-task` | Create task issue |
| `/dev-skills:issue-workflow:create-test-cases` | Create test cases issue |

**Typical Workflow:**

1. **Create milestone**: Create a milestone for new requirements
   ```
   /dev-skills:issue-workflow:create-milestone
   ```

2. **Create user story**: Break down requirements into user stories
   ```
   /dev-skills:issue-workflow:create-user-story
   ```

3. **Design phase**: Complete design with brainstorming, then create Design Issue
   ```
   /superpowers:brainstorming
   /dev-skills:issue-workflow:create-design
   ```

4. **Task breakdown**: Write plan with writing-plans, then create Task Issue
   ```
   /superpowers:writing-plans
   /dev-skills:issue-workflow:create-task
   ```

5. **Create test cases**: Create acceptance test cases for the task
   ```
   /dev-skills:issue-workflow:create-test-cases
   ```

## Auto Behaviors

- **Label management**: Auto-check and create missing labels (`user-story`, `design`, `task`, `test-cases`)
- **Bidirectional linking**: Auto-create links between related issues
- **Language detection**: Auto-select zh/en template based on conversation language
- **Repository detection**: Auto-detect from `git remote`, prompt if not found

## Priority Rules

For all inputs (milestone, user-story, design, task):
1. First use information from current conversation context
2. Then use command parameters (e.g., `--milestone 1`)
3. Finally query GitHub API and present selection list

## License

MIT
