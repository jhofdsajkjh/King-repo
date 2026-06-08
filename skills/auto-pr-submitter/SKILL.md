---
name: auto-pr-submitter
title: Auto PR Submitter - Automated Pull Request Generation
description: 技能更新后自动生成 PR，触发 CI/CD 验证，用户审核后合并
category: devops
version: 1.0
tags: [github, pr, automation, ci-cd, deployment]
---

# Auto PR Submitter

技能更新后自动生成 PR，触发 CI/CD 验证，用户审核后合并。

## 功能

- **Pattern Detection**: 检测需要更新的技能模式
- **PR Generation**: 自动生成 Pull Request
- **CI/CD Trigger**: 触发 GitHub Actions 验证
- **Approval Workflow**: 用户审核后自动合并
- **Branch Management**: 管理 feature branches

## 使用场景

1. **技能更新**: 从外部知识提取后自动生成 PR
2. **模式同步**: 同步 GitHub 仓库的更新到本地技能
3. **自动修复**: 自动提交 bug 修复 PR
4. **文档更新**: 自动生成文档更新 PR

## PR 生成流程

```
┌─────────────────────────────────────────────────────────┐
│                   PR GENERATION WORKFLOW                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. 检测变更 → 2. 创建 feature branch                   │
│        │             │                                  │
│        ▼             ▼                                  │
│  3. 生成 commit → 4. 创建 PR                            │
│        │             │                                  │
│        ▼             ▼                                  │
│  5. CI/CD 验证 → 6. 等待审核                            │
│        │             │                                  │
│        ▼             ▼                                  │
│  7. 合并到 main                         │                  │
│                                         ▼                  │
│                                   完成                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## GitHub CLI 示例

### 1. 创建分支

```bash
# 创建 feature branch
git checkout -b feature/update-memory-pattern

# 或使用 GitHub CLI
gh workflow run create_branch --ref main
```

### 2. 提交变更

```bash
# 添加文件
git add skills/memory-pattern/SKILL.md

# 提交变更
git commit -m "feat: update memory pattern based on letta research"

# 推送到远程
git push origin feature/update-memory-pattern
```

### 3. 创建 PR

```bash
# 创建 PR
gh pr create   --title "feat: update memory pattern from letta research"   --body "Update memory pattern based on Letta's multi-memory architecture. refs #123"   --base main   --head feature/update-memory-pattern
```

### 4. 合并 PR

```bash
# 自动合并（需要权限）
gh pr merge --merge

# 或使用 squash
gh pr merge --squash
```

## GitHub API 示例

### 创建 PR (Python)

```python
import urllib.request
import json

def create_github_pr(token, owner, repo, title, body, head, base="main"):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    
    headers = {
        "Authorization": f"token {token}",
        "Content-Type": "application/json"
    }
    
    data = json.dumps({
        "title": title,
        "body": body,
        "head": head,
        "base": base
    }).encode()
    
    req = urllib.request.Request(url, data=data, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return {"error": str(e.code), "body": e.read().decode()}
```

### 评论 PR

```python
def comment_pr(token, owner, repo, pr_number, comment):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"
    
    headers = {
        "Authorization": f"token {token}",
        "Content-Type": "application/json"
    }
    
    data = json.dumps({"body": comment}).encode()
    
    req = urllib.request.Request(url, data=data, headers=headers)
    
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())
```

## CI/CD 配置

### .github/workflows/pr-validation.yml

```yaml
name: PR Validation

on:
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      
      - name: Install dependencies
        run: |
          pip install pyyaml
      
      - name: Validate skill files
        run: |
          python scripts/validate_skills.py
      
      - name: Run tests
        run: |
          pytest tests/
```

## 输出格式

### PR Created
```json
{
  "pr_number": 42,
  "title": "feat: update memory pattern from letta research",
  "url": "https://github.com/owner/repo/pull/42",
  "status": "open",
  "created_at": "2026-06-07T12:00:00Z"
}
```

### CI Status
```json
{
  "status": "success",
  "checks": [
    {"name": "validate_skills", "status": "completed", "conclusion": "success"},
    {"name": "unit_tests", "status": "completed", "conclusion": "success"}
  ]
}
```

## 示例工作流

```
用户: "扫描今天的 AI Agent 趋势"
  ↓
GitHub Skill Hunter: "Found letta's memory pattern"
  ↓
更新 skill 文件: skills/memory-pattern/SKILL.md
  ↓
Auto PR Submitter: "Creating PR #42"
  ↓
CI/CD: "Running validation..."
  ↓
用户: "/approve"
  ↓
Auto PR Submitter: "Merging to main"
  ↓
完成: "Pattern updated!"
```

## 安全考虑

- PR 必须通过 CI/CD 验证才能合并
- 敏感信息（API keys）不应提交到 PR
- 使用 `.gitignore` 排除敏感文件
- 启用分支保护规则

## 限制

- 需要 GitHub PAT (Personal Access Token)
- PR 合并需要仓库写权限
- CI/CD 作业可能失败需要人工干预

## 相关技能

- github-skill-hunter: GitHub repository discovery
- self-improving-agent: Lifelong learning system
- github-pr-workflow: PR management
