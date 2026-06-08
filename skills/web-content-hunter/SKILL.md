---
name: web-content-hunter
title: Web Content Hunter - ArXiv & Tech Blog Content Extraction
description: 从 arXiv 论文、技术博客提取最新 AI/ML 研究和最佳实践
category: research
version: 1.0
tags: [arxiv, research, tech-blogs, content-extraction, learning]
---

# Web Content Hunter

从 arXiv 论文、技术博客提取最新 AI/ML 研究和最佳实践。

## 功能

- **ArXiv Search**: 搜索和提取最新 AI/ML 论文
- **Tech Blog Extraction**: 抓取掘金、知乎、Medium 等技术博客
- **Content Analysis**: 提取代码示例、设计模式、最佳实践
- **Trend Detection**: 识别热门研究方向和技术趋势

## 使用场景

1. **每日研究扫描**: 提取今日最热门的 AI 论文
2. **技术跟进**: 跟踪开源社区的最新进展
3. **模式提取**: 从博客中提取可复用的设计模式
4. **知识补充**: 将外部知识整合到 Hermes 技能

## ArXiv API 示例

### 搜索最新论文

```python
import urllib.request
import xml.etree.ElementTree as ET

# ArXiv API endpoint
url = "http://export.arxiv.org/api/query?search_query=all:ai&start=0&max_results=5&sortBy=submittedDate&sortOrder=descending"

with urllib.request.urlopen(url) as resp:
    data = resp.read().decode()
    # 解析 XML 获取论文信息
    root = ET.fromstring(data)
    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        title = entry.find("{http://www.w3.org/2005/Atom}title").text
        published = entry.find("{http://www.w3.org/2005/Atom}published").text
        print(f"{title} ({published})")
```

### 按类别搜索

```python
# AI/ML 论文
url = "http://export.arxiv.org/api/query?search_query=cat:cs.AI&start=0&max_results=10"

# 机器学习论文
url = "http://export.arxiv.org/api/query?search_query=cat:cs.LG&start=0&max_results=10"

# 自动代理论文
url = "http://export.arxiv.org/api/query?search_query=cat:cs.MA&start=0&max_results=10"
```

## 技术博客抓取

### 掘金（Juejin）

```python
import urllib.request
import json

# 掘金热门文章 API
url = "https://api.juejin.cn/content_api/v1/content/query_list"

# POST body
data = json.dumps({
    "cursor": "0",
    "size": 20,
    "category": 2  # 技术
}).encode()

req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read().decode())
    for item in result.get("data", []):
        print(f"{item['title']} - {item['author_name']}")
```

### Medium

```python
import urllib.request
import json

# Medium 最新文章
url = "https://medium.com/feed/tag/artificial-intelligence"

# 解析 RSS/Atom feed
```

## 输出格式

### ArXiv Paper
```json
{
  "arxiv_id": "2406.12345",
  "title": "Self-Improving Agents with Advanced Memory",
  "authors": ["John Doe", "Jane Smith"],
  "published": "2024-06-15",
  "category": "cs.AI",
  "abstract": "We propose...",
  "url": "https://arxiv.org/abs/2406.12345"
}
```

### Blog Post
```json
{
  "source": "juejin",
  "title": "如何构建自进化 AI Agent",
  "author": "张三",
  "published": "2024-06-15",
  "url": "https://juejin.cn/post/123456",
  "categories": ["人工智能", "开发"],
  "content_summary": "..."
}
```

## 示例工作流

```
用户: "扫描今天的 AI 研究趋势"
  ↓
Hermes: "正在抓取 ArXiv..."
  ↓
Web Content Hunter: "Found 5 papers"
  ↓
提取模式: "self-improving agent with memory"
  ↓
更新 semantic memory: "memory_architecture_pattern"
  ↓
报告: "发现新论文：Self-Improving Agents with Advanced Memory"
```

## 限制

- ArXiv API 速率限制 (每 3 秒 1 次请求)
- 博客网站可能有反爬机制
- 某些内容需要 JavaScript 渲染

## 相关技能

- search-workflow: Consolidated search utilities
- anysearch: AI-powered search
- research: Academic research tools
