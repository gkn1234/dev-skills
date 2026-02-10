# GitHub CI/CD 集成技术调研

## 概述

将 dev-skills 技能与 GitHub CI/CD 结合，实现产研自动化流程。

## 目标流程

```
飞书群聊
   │ @机器人 + PRD链接 + 目标仓库
   ▼
飞书机器人 ──POST dispatches──▶ GitHub Action
                                    │
                                    ▼ claude-code-action
                               Claude (PRD Review)
                                    │ 使用 feishu-doc 读取 PRD
                                    ▼
                               创建主 Issue（评审结果）
                                    │
                                    ▼
                           研发评论指令 ──trigger──▶ Action
                                    │
                                    ▼
                               Claude (后续流程)
                                    │
                                    ▼ 循环直到完成
```

## 技术方案

### 1. 外部触发机制

**飞书 → GitHub 触发**：使用 `repository_dispatch` 事件

```bash
POST https://api.github.com/repos/{owner}/{repo}/dispatches
Authorization: token {PAT}
Content-Type: application/json

{
  "event_type": "prd-review",
  "client_payload": {
    "prd_url": "https://feishu.cn/docs/xxx",
    "requester": "zhangsan"
  }
}
```

对应 workflow 配置：

```yaml
on:
  repository_dispatch:
    types: [prd-review]
```

**限制**：
- 只能触发默认分支上的 workflow
- 需要有 `repo` 权限的 Personal Access Token (PAT)
- 返回 204 表示成功，无法同步获取执行结果

### 2. Claude 集成方案

**使用官方 Action**：[anthropics/claude-code-action@v1](https://github.com/anthropics/claude-code-action)

核心特性：
- 自动模式检测（交互模式 vs 自动化模式）
- 支持 `@claude` 触发 + 自定义 prompt 自动执行
- 内置 GitHub 工具（读写文件、创建 PR、评论 Issue 等）
- 支持 `CLAUDE.md` 作为项目级指令
- 进度追踪（`track_progress: true`）

认证方式：
| 方式 | 适用场景 |
|------|---------|
| Anthropic API | 最简单，用 `ANTHROPIC_API_KEY` |
| AWS Bedrock | 企业级，需配置 OIDC |
| Google Vertex AI | 企业级，需 Workload Identity |

### 3. Issue 交互机制

**触发配置**：

```yaml
on:
  issue_comment:
    types: [created]

jobs:
  claude:
    if: contains(github.event.comment.body, '@claude')
    # 或自定义指令：contains(github.event.comment.body, '/next-step')
```

**可用上下文变量**：

```yaml
${{ github.event.issue.number }}      # Issue 号
${{ github.event.issue.body }}        # Issue 原始内容
${{ github.event.comment.body }}      # 用户输入的评论/指令
${{ github.actor }}                   # 操作人
```

**交互模式**：
- Claude 输出集中问题 → 在 Issue 评论中一次性列出所有待确认项
- 用户回复评论 → 触发新的 Action 执行
- 无会话记忆 → 通过 skill 从 Issue 内容重建上下文

**限制**：
- `issue_comment` 只能触发默认分支的 workflow
- 每次评论触发是独立执行

### 4. 技能加载方案

**插件市场来源**：

| 插件市场 | Git URL | 包含插件 |
|----------|---------|----------|
| `claude-plugins-official` | `https://github.com/anthropics/claude-plugins-official.git` | typescript-lsp, context7, playwright 等 |
| `superpowers-marketplace` | `https://github.com/obra/superpowers.git` | superpowers |
| `dev-skills` | 当前仓库 | dev-skills |
| `anthropic-agent-skills` | `https://github.com/anthropics/skills.git` | document-skills, example-skills |

**优先使用 LSP**：`typescript-lsp` 插件提供代码分析能力（Go to Definition、Find References），比 Grep/Glob 更精准。

**marketplace.json 格式**（当前仓库已符合规范）：

```json
{
  "name": "dev-skills",
  "plugins": [
    {
      "name": "dev-skills",
      "skills": [
        "./skills/issue-workflow",
        "./skills/feishu-doc",
        ...
      ]
    }
  ]
}
```

### 5. 权限配置

**Bash 命令默认禁用**，需要显式开启：

```yaml
claude_args: |
  --allowedTools "Bash(gh:*),Bash(git:*),Bash(python:*),Bash(pip:*)"
```

**环境变量传递**：

```yaml
settings: |
  {
    "env": {
      "ANTHROPIC_BASE_URL": "${{ secrets.ANTHROPIC_BASE_URL }}",
      "FEISHU_APP_ID": "${{ secrets.FEISHU_APP_ID }}",
      "FEISHU_APP_SECRET": "${{ secrets.FEISHU_APP_SECRET }}"
    }
  }
```

**注意**：如果使用自定义 API 代理，需要配置 `ANTHROPIC_BASE_URL`。

## 完整 Workflow 示例

```yaml
name: PRD Review & Development Workflow

on:
  # 外部触发（飞书机器人）
  repository_dispatch:
    types: [prd-review]

  # Issue 评论触发（研发指令）
  issue_comment:
    types: [created]

permissions:
  contents: write
  issues: write
  pull-requests: write

jobs:
  claude:
    runs-on: ubuntu-latest

    # 条件：外部触发 或 评论中包含 @claude
    if: |
      github.event_name == 'repository_dispatch' ||
      contains(github.event.comment.body, '@claude')

    steps:
      - uses: actions/checkout@v4

      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}

          # 添加插件市场
          plugin_marketplaces: |
            https://github.com/anthropics/claude-plugins-official.git
            https://github.com/obra/superpowers.git
            https://github.com/your-org/agents-9ab59f9f11.git

          # 安装技能
          plugins: |
            typescript-lsp@claude-plugins-official
            superpowers@superpowers-marketplace
            dev-skills@dev-skills

          # PRD Review 时的 prompt
          prompt: |
            ${{ github.event_name == 'repository_dispatch' && format('
              使用 issue-prd-review 技能评审 PRD。
              PRD 链接: {0}
              请求人: {1}
            ', github.event.client_payload.prd_url, github.event.client_payload.requester) || '' }}

          # 开启必要的 Bash 权限
          claude_args: |
            --allowedTools "Bash(gh:*),Bash(git:*),Bash(python:*),Bash(pip:*)"

          # 传递环境变量（包括 API 代理和飞书凭证）
          settings: |
            {
              "env": {
                "ANTHROPIC_BASE_URL": "${{ secrets.ANTHROPIC_BASE_URL }}",
                "FEISHU_APP_ID": "${{ secrets.FEISHU_APP_ID }}",
                "FEISHU_APP_SECRET": "${{ secrets.FEISHU_APP_SECRET }}"
              }
            }
```

## 技术可行性总结

| 检查项 | 状态 | 说明 |
|--------|------|------|
| 外部触发 | ✅ | `repository_dispatch` |
| Claude 集成 | ✅ | `claude-code-action@v1` 官方支持 |
| Issue 交互 | ✅ | `issue_comment` 事件 |
| 技能加载 | ✅ | `plugin_marketplaces` + `plugins` |
| dev-skills 格式 | ✅ | 符合 marketplace 规范 |
| superpowers 加载 | ✅ | 从 `obra/superpowers` 安装 |
| LSP 支持 | ✅ | `typescript-lsp@claude-plugins-official` |
| Bash 权限 | ⚠️ | 需配置 `--allowedTools` |
| 环境变量 | ✅ | 通过 `settings.env` 传递 |
| 会话记忆 | ⚠️ | 无，需通过 skill 从 Issue 重建上下文 |

## 待实现

1. **飞书机器人开发**（不在本次调研范围）
   - 接收 @消息
   - 解析 PRD 链接和目标仓库
   - 调用 GitHub API 触发 dispatch

2. **dev-skills 仓库公开或配置访问权限**
   - 确保 GitHub Action 可以 clone 仓库

3. **目标代码仓配置**
   - 添加 workflow 文件
   - 配置 Secrets：
     - `ANTHROPIC_API_KEY`
     - `ANTHROPIC_BASE_URL`（如使用 API 代理）
     - `FEISHU_APP_ID`
     - `FEISHU_APP_SECRET`

## 参考资料

- [Claude Code Action 官方仓库](https://github.com/anthropics/claude-code-action)
- [Claude Code GitHub Actions 文档](https://code.claude.com/docs/en/github-actions)
- [Claude Plugins Official](https://github.com/anthropics/claude-plugins-official) - typescript-lsp, context7, playwright 等
- [GitHub repository_dispatch 文档](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#repository_dispatch)
- [GitHub issue_comment 文档](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#issue_comment)
- [superpowers 插件市场](https://github.com/obra/superpowers)
