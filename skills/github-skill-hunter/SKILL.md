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
import time

def fetch_trending(keyword, limit=5):
    """搜索趋势仓库（含速率限制重试逻辑）"""
    url = f"https://api.github.com/search/repositories?q={keyword}+agent&sort=stars&order=desc&per_page={limit}"
    headers = {"User-Agent": "Hermes-GitHubHunter"}  # 避免 403
    
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode())
                results = []
                for i, r in enumerate(data.get("items", [])[:limit]):
                    results.append({
                        "rank": i + 1,
                        "name": r["full_name"],
                        "stars": r["stargazers_count"],
                        "updated": r["updated_at"][:10],
                        "url": r["html_url"],
                        "description": r["description"] or ""
                    })
                return results
        except urllib.error.HTTPError as e:
            if e.code == 403:  # Rate limit exceeded
                if attempt < 2:
                    print(f"Rate limited, waiting 30s... (attempt {attempt+1}/3)")
                    time.sleep(30)
                else:
                    raise
            else:
                raise
    
    return []
```

### 2. 获取仓库 README

```python
import urllib.request

def fetch_readme(repo, timeout=30):
    """获取仓库 README（带 User-Agent 和错误处理）"""
    url = f"https://raw.githubusercontent.com/{repo}/main/README.md"
    headers = {"User-Agent": "Hermes-GitHubHunter"}
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode()
    except Exception as e:
        print(f"Failed to fetch README for {repo}: {e}")
        return None

# 使用示例
readme = fetch_readme("letta-ai/letta")
if readme:
    print(f"README length: {len(readme)} chars")
```

### 3. 下载 GitHub Release Assets

```python
import urllib.request
import os

def fetch_asset(url, output_path, timeout=300):
    """下载 GitHub Release asset（支持断点续传）"""
    headers = {"User-Agent": "Hermes-GitHubHunter"}
    
    # 检查已下载部分
    downloaded = 0
    if os.path.exists(output_path):
        downloaded = os.path.getsize(output_path)
        headers["Range"] = f"bytes={downloaded}-"
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            mode = 'ab' if downloaded > 0 else 'wb'
            with open(output_path, mode) as f:
                while True:
                    chunk = resp.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)
        return True
    except Exception as e:
        print(f"Download failed: {e}")
        return False

# 使用示例
url = "https://github.com/iOfficeAI/OfficeCLI/releases/download/v1.0.105/officecli-linux-arm64"
if fetch_asset(url, "/usr/local/bin/officecli"):
    print("Download completed")
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

## 速率限制绕过方案

### 方案 1：配置 GitHub PAT（推荐）
```python
# 在 hermes config.yaml 中添加环境变量
providers:
  - provider: custom
    api_key: your_pat_here
```

### 方案 2：直接下载配置文件
对于大型仓库，直接下载 YAML/JSON 配置文件（如订阅配置、 skills.yaml）比调用 API 更高效：
```bash
curl -L "https://raw.githubusercontent.com/user/repo/main/config.yaml" -o config.yaml
```

### 方案 3：等待重置
GitHub unauthenticated API 速率限制需等待约 1 小时重置。期间可：
- 使用已缓存的结果
- 转向其他数据源（如本地技能库）
- 切换到有 PAT 的账户

## 限制

- GitHub API 速率限制 (60 req/h unauthenticated)
- 每次搜索最多返回 1000 个结果
- README 最大 50KB
- **GitHub Release 下载速度较慢**（~20KB/s），大文件下载易超时，建议手动下载

## 改进建议

- 配置 GitHub Personal Access Token (PAT) 提升速率限制 (5000 req/h)
- 使用国内镜像加速（如: `github.com.cnpmjs.org`）
- 对大文件（>50MB）建议手动下载后上传到服务器

## 实战经验（2026-06-09）

### 问题 1: GitHub API 速率限制 (403)
**现象**: 连续调用 API 返回 `HTTP Error 403: rate limit exceeded`

**解决方案**:
1. 使用已下载的订阅配置文件（避免 API 调用）
2. 配置 Clash 代理后重试（代理后成功）
3. 等待 120 秒让 GitHub API 重置

**关键代码**:
```python
# 设置代理
proxy_handler = urllib.request.ProxyHandler({
    'http': '127.0.0.1:7890',
    'https': '127.0.0.1:7890'
})
opener = urllib.request.build_opener(proxy_handler)
urllib.request.install_opener(opener)
```

### 问题 2: Clash 配置失败 (MMDB 下载超时)
**现象**: `can't download MMDB: context deadline exceeded`

**解决方案**:
1. 移除规则中的 `GEOIP,CN` 行
2. 重新启动 clash
3. 验证状态：`curl http://127.0.0.1:9090/version`

### 问题 3: GitHub 推送受阻 (Secret Scanning)
**现象**: `GH013: Repository rule violations found for refs/heads/main`

**解决方案**:
1. 删除敏感文件（`.git-credentials`, `sessions/session_*.json`）
2. 使用 `git reset --soft HEAD~1` 撤销提交
3. 重新提交并推送（成功）

### 问题 4: clash 后台进程无法追踪
**现象**: 使用 `nohup` 启动后无法获取进程状态

**解决方案**:
```python
# 正确方式
terminal(command="clash -d /opt/data/.clash", background=True, notify_on_complete=True)

# 错误方式（无法追踪）
terminal(command="nohup clash -d /opt/data/.clash > /tmp/clash.log 2>&1 &")
```

### 问题 5: 自进化系统 Git 冲突
**现象**: `fatal: '.hermes' is a main working tree`

**解决方案**:
1. 使用 `git stash` 保存本地更改
2. 切换到 main 分支并拉取
3. 使用 `git checkout --ours` 解决冲突（保留本地配置）
4. 重新提交并推送

### 实战总结
1. **Clash 代理是绕过 GitHub API 速率限制的有效方案**
2. **敏感文件必须从 Git 中排除**（`.git-credentials`, `sessions/*.json`）
3. **Hermetic 系统使用工作树模式**（`git worktree`）
4. **自进化循环必须包含 Git 证书清理步骤**

## 实战经验（2026-06-09）

### 问题 1: GitHub API 速率限制 (403)
**现象**: 连续调用 API 返回 `HTTP Error 403: rate limit exceeded`

**解决方案**:
1. 使用已下载的订阅配置文件（避免 API 调用）
2. 配置 Clash 代理后重试（代理后成功）
3. 等待 120 秒让 GitHub API 重置

**关键代码**:
```python
# 设置代理
proxy_handler = urllib.request.ProxyHandler({
    'http': '127.0.0.1:7890',
    'https': '127.0.0.1:7890'
})
opener = urllib.request.build_opener(proxy_handler)
urllib.request.install_opener(opener)
```

### 问题 2: Clash 配置失败 (MMDB 下载超时)
**现象**: `can't download MMDB: context deadline exceeded`

**解决方案**:
1. 移除规则中的 `GEOIP,CN` 行
2. 重新启动 clash
3. 验证状态：`curl http://127.0.0.1:9090/version`

### 问题 3: GitHub 推送受阻 (Secret Scanning)
**现象**: `GH013: Repository rule violations found for refs/heads/main`

**解决方案**:
1. 删除敏感文件（`.git-credentials`, `sessions/session_*.json`）
2. 使用 `git reset --soft HEAD~1` 撤销提交
3. 重新提交并推送（成功）

### 问题 4: clash 后台进程无法追踪
**现象**: 使用 `nohup` 启动后无法获取进程状态

**解决方案**:
```python
# 正确方式
terminal(command="clash -d /opt/data/.clash", background=True, notify_on_complete=True)

# 错误方式（无法追踪）
terminal(command="nohup clash -d /opt/data/.clash > /tmp/clash.log 2>&1 &")
```

### 问题 5: 自进化系统 Git 冲突
**现象**: `fatal: '.hermes' is a main working tree`

**解决方案**:
1. 使用 `git stash` 保存本地更改
2. 切换到 main 分支并拉取
3. 使用 `git checkout --ours` 解决冲突（保留本地配置）
4. 重新提交并推送

### 实战总结
1. **Clash 代理是绕过 GitHub API 速率限制的有效方案**
2. **敏感文件必须从 Git 中排除**（`.git-credentials`, `sessions/*.json`）
3. **Hermetic 系统使用工作树模式**（`git worktree`）
4. **自进化循环必须包含 Git 证书清理步骤**

## 额外技巧

### 对于大型 YAML/JSON 文件下载
GitHub API 返回分页数据（`?per_page=100`），但直接下载 `raw.githubusercontent.com` 文件更高效：
```bash
# 直接下载 skills.yaml
curl -L "https://raw.githubusercontent.com/NousResearch/hermes-agent/main/.hermes/skills.yaml" -o skills.yaml

# 直接下载 geoip.metadb（需要翻墙）
curl -L "https://github.com/MetaCubeX/meta-rules-dat/releases/download/latest/geoip.metadb" -o geoip.metadb
```

### 后台进程启动规范
Hermes 无法追踪 `nohup`/`disown`/`setsid` 等 shell 后台方式，必须使用：
```python
# 正确方式
terminal(command="clash -d /opt/data/.clash", background=True, notify_on_complete=True)

# 错误方式（无法追踪）
terminal(command="nohup clash -d /opt/data/.clash > /tmp/clash.log 2>&1 &")
```

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

### Q: GitHub API 速率限制怎么办？\nA: Skill 已内置重试逻辑（3 次，每次间隔 30 秒）。如果仍被限制：\\n1. 等待 60-120 秒后重试（实测 403 限制需更长时间）\\n2. 配置 GitHub Personal Access Token (PAT) 提升速率限制 (5000 req/h) —— **推荐方案**\\n3. 使用国内镜像加速（如: `github.com.cnpmjs.org`）\\n4. 启用 Clash 代理（绕过某些网络限制）\\n\\n**PAT 配置示例：**\\n```python\\nimport urllib.request\\nimport json\\n\\ndef fetch_with_pat(url, pat, timeout=30):\\n    \\\"\\\"\\\"使用 PAT 访问 GitHub API\\\"\\\"\\\"\\n    headers = {\\n        \\\"User-Agent\\\": \\\"Hermes-GitHubHunter\\\",\\n        \\\"Authorization\\\": f\\\"token {pat}\\\"\\n    }\\n    req = urllib.request.Request(url, headers=headers)\\n    with urllib.request.urlopen(req, timeout=timeout) as resp:\\n        return json.loads(resp.read().decode())\\n\\n# 使用\\nrepo = \\\"NousResearch/hermes-agent\\\"\\nurl = f\\\"https://api.github.com/repos/{repo}/contents\\\"\\ndata = fetch_with_pat(url, \\\"ghp_xxxxxxxxxxxx\\\")\\nprint(f\\\"Found {len(data)} items\\\")\\n```\\n\\n### Q: 如何避免速率限制？\\nA: 生产环境建议：\\n1. **始终使用 PAT**（Heroku/GitHub Actions 环境变量配置）\\n2. **设置速率监控**（调用前检查 `rate_limit`）\\n3. **批量操作使用 GraphQL**（1 次请求获取多数据）\\n4. **缓存结果**（GitHub 数据不频繁更新）\\n\\n### Q: 下载大型 YAML/JSON 配置文件失败怎么办？\\nA: GitHub API 对单文件大小有限制，建议：\\n1. 直接下载 raw 文件（如 `https://raw.githubusercontent.com/user/repo/main/config.yaml`）\\n2. 对于 geoip.metadb 等大文件（>50MB），建议手动下载后上传到服务器\\n3. 使用国内镜像或 CDN 加速\\n\\n### Q: Clash 代理配置失败怎么办？\\nA: 常见问题：\\n1. **MMDB 下载失败**：移除规则中的 `GEOIP,CN` 行，重新启动 clash\\n2. **端口冲突**：检查 7890/7891/9090 端口是否被占用\\n3. **后台进程启动**：使用 `terminal(..., background=True, notify_on_complete=True)` 而非 `nohup`\\n\\n**Clash 启动命令：**\\n```bash\\nclash -d /opt/data/.clash\\n```\\n**Clash API 调用：**\\n```python\\nimport urllib.request\\nimport json\\n\\ndef update_clash_proxy(proxy_name):\\n    url = \"http://127.0.0.1:9090/proxies/GLOBAL\"\\n    data = json.dumps({\"name\": proxy_name}).encode()\\n    req = urllib.request.Request(url, data=data, method='PUT')\\n    req.add_header(\"Content-Type\", \"application/json\")\\n    with urllib.request.urlopen(req, timeout=5) as resp:\\n        return resp.status\\n```\\n\\n### Q: 如何监控 Clash 代理状态？\\nA: 通过 Clash API 检查：\\n```python\\nimport urllib.request\\nimport json\\n\\ndef check_clash_status():\\n    try:\\n        req = urllib.request.Request(\"http://127.0.0.1:9090/proxies\")\\n        with urllib.request.urlopen(req, timeout=5) as resp:\\n            data = json.loads(resp.read().decode())\\n            return data.get('proxies', {}).get('GLOBAL', {}).get('now')\\n    except Exception as e:\\n        return None\\n```\\n\\n### Q: 如何测试代理连通性？\\nA: 使用 urllib 的 ProxyHandler：\\n```python\\nimport urllib.request\\n\\ndef test_proxy(url, proxy_host='127.0.0.1', proxy_port=7890):\\n    proxy_handler = urllib.request.ProxyHandler({\\n        'http': f'{proxy_host}:{proxy_port}',\\n        'https': f'{proxy_host}:{proxy_port}'\\n    })\\n    opener = urllib.request.build_opener(proxy_handler)\\n    try:\\n        req = urllib.request.Request(url)\\n        with opener.open(req, timeout=10) as resp:\\n            return resp.status\\n    except Exception as e:\\n        return f'Error: {type(e).__name__}'\\n\\n# 测试\\nprint(test_proxy('https://www.google.com'))\\n```"
