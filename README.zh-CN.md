# Dev Skills

用于增强开发工作流程的 Claude Code 技能集合。

[English](./README.md)

## 简介

Dev Skills 是一个 Claude Code 技能集合，用于增强开发工作流程。包含 `issue-workflow` 技能帮助团队基于 PRD 驱动的 GitHub Issue 进行规范化的研发流程管理，以及 `feishu-doc` 技能用于读取飞书文档。

## Skills

### issue-workflow

基于 PRD 驱动的 GitHub Issue 研发流程管理技能。

**功能特性：**
- 完整的研发流程：PRD 评审 → 主 Issue → 子 Issue → Task → Test Cases → 实现 → PR
- 技术可行性评估与功能点拆分
- 双语支持（中/英文）
- 与 [superpowers](https://github.com/anthropics/claude-code-superpowers) 技能深度集成
- Git worktree 隔离实现

### feishu-doc

读取飞书文档并转换为本地 JSON 格式。

**功能特性：**
- 解析飞书文档链接（docx/docs/wiki）
- 下载图片到本地 `assets/` 目录
- 提取引用的文档链接
- 输出原始 blocks JSON 供 AI 分析
- 与 `issue-prd-review` 集成，支持 PRD 评审流程

**环境变量配置：**
```bash
export FEISHU_APP_ID=cli_xxx
export FEISHU_APP_SECRET=xxx
```

**流程概览：**

```
PRD 文档
    │
    ▼
issue-prd-review ─→ 主 Issue + 技术评估 Comment
    │
    ▼ (对每个功能点)
issue-design ─→ 子 Issue + Design Comment
    │
    ▼ (对每个 Task)
issue-tasks ─→ Task Comment
    │
    ▼ (可选)
issue-test-cases ─→ Test Cases Comment
    │
    ▼
issue-implement ─→ 代码实现
    │
    ▼
issue-pr ─→ Pull Request
    │
    ▼
手动合并 → 手动关闭 Issue
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
| `issue-workflow` | "研发流程"/"下一步"/"进度" | 流程概览与状态检测 |
| `issue-prd-review` | "评审 PRD"/"新需求"/"创建 Issue" | PRD 评审 → 主 Issue + 技术评估 |
| `issue-design` | "添加设计"/"创建子 Issue" | 创建子 Issue + Design Comment |
| `issue-tasks` | "添加任务"/"任务拆分" | 添加 Task Comment |
| `issue-test-cases` | "测试用例"/"验收标准" | 添加 Test Cases Comment |
| `issue-implement` | "实现"/"开发"/"coding" | 在 worktree 中实现代码 |
| `issue-pr` | "创建 PR"/"pull request" | 创建关联子 Issue 的 PR |
| `issue-repo` | (自动调用) | 确定目标仓库 |
| `feishu-doc` | 飞书链接/"读取飞书文档" | 读取飞书文档为 JSON |

**典型工作流：**

1. **PRD 评审**：评审 PRD 并创建主 Issue
   ```
   /issue-prd-review
   ```

2. **创建子 Issue**：为每个功能点创建子 Issue 并添加设计
   ```
   /issue-design
   ```

3. **任务拆分**：添加 Task Comment 描述实现细节
   ```
   /issue-tasks
   ```

4. **测试用例**（可选）：添加验收测试用例
   ```
   /issue-test-cases
   ```

5. **实现**：在隔离的 worktree 中实现任务
   ```
   /issue-implement
   ```

6. **创建 PR**：创建关联子 Issue 的 Pull Request
   ```
   /issue-pr
   ```

## License

MIT
