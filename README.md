# Dev Skills

A collection of Claude Code skills for development workflows.

[中文文档](./README.zh-CN.md)

## Introduction

Dev Skills is a collection of Claude Code skills for enhancing development workflows. Includes `issue-workflow` for PRD-driven GitHub Issue development workflow management, and `feishu-doc` for reading Feishu/Lark documents.

## Skills

### issue-workflow

PRD-driven GitHub Issue development workflow management.

**Features:**
- Complete workflow: PRD Review → Main Issue → Sub Issues → Tasks → Test Cases → Implementation → PR
- Technical feasibility assessment with feature breakdown
- Bilingual support (zh/en)
- Deep integration with [superpowers](https://github.com/anthropics/claude-code-superpowers) skills
- Git worktree isolation for implementation

### feishu-doc

Read Feishu/Lark documents and convert to local JSON format.

**Features:**
- Parse Feishu document links (docx/docs/wiki)
- Download images to local `assets/` directory
- Extract referenced document links
- Output raw blocks JSON for AI analysis
- Integrated with `issue-prd-review` for PRD review workflow

**Requirements:**
```bash
export FEISHU_APP_ID=cli_xxx
export FEISHU_APP_SECRET=xxx
```

**Workflow Overview:**

```
PRD Document
    │
    ▼
issue-prd-review ─→ Main Issue + Technical Review Comment
    │
    ▼ (for each feature)
issue-design ─→ Sub Issue + Design Comment
    │
    ▼ (for each task)
issue-tasks ─→ Task Comment
    │
    ▼ (optional)
issue-test-cases ─→ Test Cases Comment
    │
    ▼
issue-implement ─→ Code Implementation
    │
    ▼
issue-pr ─→ Pull Request
    │
    ▼
Manual merge → Manual close Issue
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
| `issue-workflow` | "workflow"/"next step"/"progress" | Workflow overview and status detection |
| `issue-prd-review` | "review PRD"/"new requirement"/"create issue" | PRD review → Main Issue + Technical Review |
| `issue-design` | "add design"/"create sub issue" | Create Sub Issue + Design Comment |
| `issue-tasks` | "add tasks"/"task breakdown" | Add Task Comment |
| `issue-test-cases` | "test cases"/"acceptance criteria" | Add Test Cases Comment |
| `issue-implement` | "implement"/"develop"/"coding" | Code implementation in worktree |
| `issue-pr` | "create PR"/"pull request" | Create PR linked to Sub Issue |
| `issue-repo` | (auto-called) | Determine target repository |
| `feishu-doc` | Feishu link/"read feishu doc" | Read Feishu document to JSON |

**Typical Workflow:**

1. **PRD Review**: Review PRD and create Main Issue
   ```
   /issue-prd-review
   ```

2. **Create Sub Issues**: Create Sub Issue for each feature with design
   ```
   /issue-design
   ```

3. **Task Breakdown**: Add Task Comment for implementation details
   ```
   /issue-tasks
   ```

4. **Test Cases** (optional): Add acceptance test cases
   ```
   /issue-test-cases
   ```

5. **Implementation**: Implement task in isolated worktree
   ```
   /issue-implement
   ```

6. **Create PR**: Create Pull Request linked to Sub Issue
   ```
   /issue-pr
   ```

## License

MIT
