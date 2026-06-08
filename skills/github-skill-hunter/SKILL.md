---
name: github-skill-hunter
title: GitHub Skill Hunter - Trending AI Agent & Skill Discovery
description: 自动搜索 GitHub 上的趋势 AI Agent 项目、技能和工具，发现最新最佳实践
category: research
version: 1.0
tags: [github, search, ai-agents, skills, trending]
---

# GitHub Skill Hunter

自动搜索 GitHub 上的趋势 AI Agent 项目、技能和工具，发现最新最佳实践。

## 功能

- **Trending Search**: 搜索今日/本周/本月最热门的 AI Agent 项目
- **Skill Discovery**: 发现 self-improving agent, multi-agent, autonomous agent 相关技能
- **README Analysis**: 提取仓库 README 中的关键模式和能力
- **Star Tracking**: 跟踪 star 数变化和项目活跃度

## 使用场景

1. **每日趋势扫描**: 发现最新的 AI Agent 技术趋势
2. **技能补充**: 从 GitHub 仓库提取最佳实践到 Hermes 技能
3. **竞品分析**: 分析热门项目的设计模式和架构
4. **学习跟进**: 跟踪开源社区的最新进展

## GitHub API 调用示例

### 1. 搜索趋势仓库

```python
import urllib.request
import json

url = "https://api.github.com/search/repositories?q=self-improving+agent&sort=stars&order=desc"
with urllib.request.urlopen(url) as resp:
    data = json.loads(resp.read().decode())
    for repo in data.get("items", [])[:5]:
        print(f"{repo['name']}: {repo['stargazers_count']} stars")
```

### 2. 获取仓库 README

```python
url = "https://raw.githubusercontent.com/letta-ai/letta/main/README.md"
with urllib.request.urlopen(url) as resp:
    readme = resp.read().decode()
    # 分析 self-improvement 能力
```

### 3. 下载 GitHub Release Assets

```python
import urllib.request
import os

# 下载 release asset（大文件）
url = "https://github.com/iOfficeAI/OfficeCLI/releases/download/v1.0.105/officecli-linux-arm64"
with urllib.request.urlopen(url, timeout=300) as resp:
    with open("/path/to/bin/officecli", "wb") as f:
        f.write(resp.read())

# 注意：GitHub 下载可能受网络限制，速度较慢（~20KB/s）
# 建议手动下载或使用国内镜像
```

## 输出格式

### Trending Result
```json
{
  "rank": 1,
  "name": "letta-ai/letta",
  "description": "AI with advanced memory that can learn and self-improve",
  "stars": 23188,
  "language": "Python",
  "updated": "2026-06-07",
  "url": "https://github.com/letta-ai/letta"
}
```

### Skill Pattern Extracted
```json
{
  "pattern_id": "pat-2026-06-07-001",
  "source": "github.com/letta-ai/letta/README",
  "type": "memory_architecture",
  "description": "Multi-memory: semantic + episodic + working",
  "code_examples": [...]
}
```

## 示例工作流

```
用户: "扫描今天的 AI Agent 趋势"
  ↓
Hermes: "正在搜索 GitHub..."
  ↓
GitHub Skill Hunter: "Found 5 trending repos"
  ↓
提取模式: "letta 的 memory_blocks 架构"
  ↓
更新 semantic memory: "memory_blocks_pattern"
  ↓
报告: "发现 letta 的先进内存架构，已记录"
```

## 限制

- GitHub API 速率限制 (60 req/h unauthenticated)
- 每次搜索最多返回 1000 个结果
- README 最大 50KB
- **GitHub Release 下载速度较慢**（~20KB/s），大文件下载易超时，建议手动下载

## 扩展

- 集成 GitHub Webhooks (自动通知)
- Star Watcher (监控 star 变化)
- PR 提取 (从 PR 中提取最佳实践)

## 相关技能

- search-workflow: Consolidated search utilities
- research: Academic and technical research
- self-improving-agent: Lifelong learning system

## 常见问题

### Q: GitHub Release 下载太慢怎么办？
A: GitHub Release 下载速度可能较慢（~20KB/s），特别是大文件（30MB+）。建议：
1. 手动下载并上传到服务器
2. 使用国内镜像或 CDN
3. 使用 `wget -c` 支持断点续传

### Q: 如何选择正确的二进制版本？
A: 根据服务器架构选择：
- x64: `officecli-linux-x64`
- ARM64: `officecli-linux-arm64`（如树莓派、AWS Graviton）

运行 `uname -m` 查看架构。
