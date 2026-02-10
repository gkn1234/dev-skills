---
name: issue-repo
description: 当需要确定目标 GitHub 仓库时自动调用。优先检测当前项目的 git remote，支持用户指定其他仓库。其他 issue-* 技能的前置依赖。
---

# Issue Repo - 仓库检测

## 职责

确定目标 GitHub 仓库（owner/repo），供其他 issue-* 技能使用。

## 检测优先级

1. **当前对话上下文**：如果用户已指定仓库，直接使用
2. **当前项目 git remote**：优先检测
3. **当前登录用户的仓库**：列出用户有权限的仓库供选择
4. **用户输入**：以上都失败时询问用户

## 检测命令

```bash
# 1. 从当前项目 git remote 检测
gh repo view --json owner,name --jq '"\(.owner.login)/\(.name)"'

# 备选：从 git remote URL 解析
git remote get-url origin | sed -E 's|.*github.com[:/]([^/]+/[^/.]+).*|\1|'

# 2. 获取当前登录用户
gh auth status --json user --jq '.user'

# 3. 列出用户有权限的仓库（最近活跃）
gh repo list --limit 10 --json nameWithOwner --jq '.[].nameWithOwner'
```

## 输出

检测成功后，输出格式：

```
仓库: owner/repo
```

后续技能使用此值进行 GitHub API 调用。

## 使用场景

| 场景 | 处理 |
|------|------|
| 用户指定 `--repo owner/repo` | 直接使用 |
| 当前项目有 remote | 使用检测到的仓库 |
| 无 remote，有登录用户 | 列出用户仓库供选择 |
| 无 remote，无登录 | 提示用户登录或手动输入 |
| 用户要切换仓库 | 更新当前仓库 |

## 示例

```
助手: [检测仓库] 当前仓库: anthropic/claude-code

用户: 用 myorg/myrepo 仓库
助手: [更新仓库] 切换到: myorg/myrepo
```
