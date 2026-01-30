# Dev Skills

A collection of Claude Code skills for development workflows.

## Skills

### issue-workflow

GitHub Issue-based development workflow management.

**Features:**
- Milestone → User Story → Design → Task → Test Cases workflow
- Auto-create labels and bidirectional linking
- Bilingual templates (zh/en, auto-detected)
- Integration with `superpowers:brainstorming` and `superpowers:writing-plans`

**Usage:**

```bash
# Add to your Claude Code skills directory
git clone https://github.com/<your-username>/dev-skills.git ~/.claude/skills/dev-skills
```

**Sub-commands:**
- `/dev-skills:issue-workflow` - Workflow overview
- `/dev-skills:issue-workflow:create-milestone` - Create milestone
- `/dev-skills:issue-workflow:create-user-story` - Create user story
- `/dev-skills:issue-workflow:create-design` - Create design issue
- `/dev-skills:issue-workflow:create-task` - Create task issue
- `/dev-skills:issue-workflow:create-test-cases` - Create test cases issue

## License

MIT
