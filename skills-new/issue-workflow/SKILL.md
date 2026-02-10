---
name: issue-workflow
description: 当用户提到"研发流程"/"开发流程"/"workflow"/"下一步"/"继续"/"流程状态"、需要了解整体工作流、或询问当前进度时使用。自动检测 Issue 状态并触发对应技能。
---

# Issue Workflow - PRD 驱动研发流程

## 职责

检测当前 Issue 状态，自动触发对应的下游技能。

## 前置：仓库检测

调用 `issue-repo` 技能确定目标仓库。

## 流程概览

```
issue-repo ─→ 确定目标仓库
    │
    ▼
一无所有
    │
    ▼
issue-prd-review ─→ 主 Issue + 子 Issue(s)
    │
    ▼ (对每个子 Issue)
issue-design ─→ Design Comment
    │
    ▼
issue-tasks ─→ Task Comment(s)
    │
    ▼
issue-test-cases ─→ Test Cases Comment(s)
    │
    ▼ (对每个 Task)
issue-implement ─→ 代码实现
    │
    ▼
issue-pr ─→ Pull Request
    │
    ▼
手动合并 ─→ 手动关闭 Issue
```

## 状态检测与技能触发

### 无 Issue 时

| 用户输入 | 触发技能 |
|----------|----------|
| 提供 PRD 文档 | → `issue-prd-review` |
| "开始新需求" | → `issue-prd-review` |

### 有主 Issue 时

检测主 Issue 状态：

```bash
# 检测是否有评估 Comment
gh api repos/{owner}/{repo}/issues/{issue号}/comments \
  --jq '.[] | select(.body | contains("<!-- type: review -->"))' | head -1
```

| 状态 | 触发技能 |
|------|----------|
| 无评估 Comment | → `issue-prd-review`（继续评估） |
| 有评估，无子 Issue | → `issue-prd-review`（创建子 Issues） |
| 有子 Issues | → 进入子 Issue 流程 |

### 有子 Issue 时

检测子 Issue 的 Comment 类型：

```bash
gh api repos/{owner}/{repo}/issues/{issue号}/comments \
  --jq '[.[] | .body | capture("<!-- type: (?<type>[^,>]+)") | .type] | unique'
```

| 已有 Comment | 触发技能 |
|--------------|----------|
| 无 | → `issue-design` |
| design | → `issue-tasks` |
| design, task | → `issue-test-cases` |
| design, task, test-cases | → `issue-implement` |
| 已有 PR | 提示：手动合并后关闭 Issue |

## 使用示例

```
用户: 我有一个 PRD 需要评审
助手: [触发 issue-prd-review]

用户: Issue #123 下一步
助手: [检测状态：已有 design]
      [触发 issue-tasks]

用户: 当前进度？
助手: 主 Issue #100，3 个子 Issue：
      - #101: 待设计 → issue-design
      - #102: 待实现 → issue-implement
      - #103: 待合并
```
