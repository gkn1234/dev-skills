# gh CLI 使用经验

## Shell 转义问题：`<!--` 在 jq 表达式中

### 问题

在 zsh 中使用 `gh api --jq` 时，如果 jq 表达式包含 HTML 注释标记 `<!--`，其中的 `!` 会触发 zsh 的历史展开（history expansion），导致 jq 解析失败：

```
failed to parse jq expression
invalid escape sequence "\!" in string literal
```

### 失败示例

```bash
gh api repos/{owner}/{repo}/issues/{number}/comments \
  --jq '.[] | select(.body | contains("<!-- type: design -->")) | .body'
```

### 解决方案

**方案 1（推荐）：用 `test()` 正则替代 `contains()`**

```bash
gh api repos/{owner}/{repo}/issues/{number}/comments \
  --jq '.[] | select(.body | test("type: design")) | .body'
```

**方案 2：关闭历史展开**

```bash
set +H
# 然后执行原命令
```

**方案 3：使用临时文件存放 jq 表达式**

```bash
echo '.[] | select(.body | contains("<!-- type: design -->")) | .body' > /tmp/filter.jq
gh api repos/{owner}/{repo}/issues/{number}/comments | jq -f /tmp/filter.jq
```

### 根本原因

zsh 双引号内的 `!` 被解释为历史展开符号，shell 在传递给 `gh` 之前会尝试展开，导致 `!` 被转义为 `\!`，jq 无法识别该转义序列。

### 适用场景

所有需要在 `--jq` 中匹配 HTML 注释标记（`<!-- ... -->`）的 `gh api` 调用，包括：

- 读取 Issue Comment 中的特定类型标记（`<!-- type: design -->`、`<!-- type: task -->`）
- 过滤包含 HTML 注释的 Markdown 内容
