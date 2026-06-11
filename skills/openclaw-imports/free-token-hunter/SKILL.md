---
name: free-token-hunter
description: 每日自动搜罗免费 Token 资源
category: openclaw-imports
tags:
  - token
  - scraping
  - automation
---

# Free Token Hunter

每日自动搜罗免费 Token 提供商，包括 GitHub 项目、API 服务、优惠活动等。

## 功能

| 功能 | 说明 |
|------|------|
| `hermes free-token --list` | 列出已发现的免费 Token 提供商 |
| `hermes free-token --scan` | 扫描最新免费 Token 资源 |
| `hermes free-token --stats` | 统计资源数量与热度 |
| `hermes free-token --cron` | 触发每日自动扫描 |

## 使用方式

### 基础命令

```bash
# 列出已发现的提供商
hermes skills call free-token-hunter list

# 扫描最新资源
hermes skills call free-token-hunter scan

# 查看统计
hermes skills call free-token-hunter stats

# 手动触发每日扫描（用于 cron）
hermes skills call free-token-hunter cron
```

### Crontab 自动化

```bash
# 编辑 crontab
crontab -e

# 每天 08:00 自动扫描免费 Token
0 8 * * * cd /opt/data && hermes skills call free-token-hunter cron >> /tmp/free-token-scan.log 2>&1
```

## 可能的免费 Token 来源

| 类型 | 示例 |
|------|------|
| GitHub 项目 | fate-zero/openai-api-keys, chatanywhere/GPT_API_v2, OpenFreeGPT, freegpt35 |
| 限时活动 | OpenAI Free Tier, Anthropic Trial, Claude.ai Free |
| 社区共享 | Reddit r/ChatGPT, V2EX 技术分享, 知乎科技板块 |
| 官方优惠 | 新用户注册赠金、教育计划、开发者计划 |
| API服务 | GitHub Copilot Free, Google Gemini API 免费额度 |

## 扫描策略

1. **GitHub 仓库搜索** - 关键词：`free-gpt`, `openai-api-key`, `chatgpt-free`, `copilot-free`
2. **社区论坛爬取** - Reddit (r/ChatGPT), V2EX, 知乎科技板块, 飞书社区
3. **官方新闻订阅** - RSS 订阅 OpenAI/Anthropic/Claude/Gemini 官方博客
4. **GitHub Trending** - 每日监控高 Star 新项目
5. **API 免费额度** - 检查 GitHub Copilot, Google Gemini 等 API 免费额度

## 输出格式

```json
{
  "timestamp": "2026-06-10T08:00:00Z",
  "sources": [
    {
      "name": "GitHub - fate-zero/openai-api-keys",
      "url": "https://github.com/fate-zero/openai-api-keys",
      "stars": 1234,
      "updated": "2026-06-09T10:00:00Z",
      "type": "github",
      "tags": ["free", "token", "api"]
    }
  ],
  "summary": {
    "total": 12,
    "github": 5,
    "community": 4,
    "official": 3
  }
}
```

## 审计日志

路径: `/opt/data/.hermes/cache/free_token_scan.jsonl`

```json
{
  "event_type": "free_token_scan",
  "timestamp": "2026-06-10T08:00:00Z",
  "sources_found": 12,
  "errors": 0,
  "cache_path": "/opt/data/.hermes/cache/free_token_latest.json"
}
```
