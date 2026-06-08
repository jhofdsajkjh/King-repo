---
name: anysearch
description: AI-powered search and content extraction via AnySearch API. Use when user asks to search the web, extract article content, find info on a topic, or research something online. Also use proactively when other tools fail to retrieve content (GitHub README, docs pages, etc.) — AnySearch often succeeds where direct fetch is blocked.
version: 1.0.0
metadata:
  hermes:
    tags: [search, web, extraction, research]
  created: 2026-05-21
trigger_phrases:
  - search
  - 搜索
  - 抓取
  - 提取内容
  - extract
  - find info
  - research
  - 爬
requires_toolsets: [terminal]
---

# AnySearch — Web Search & Content Extraction

AnySearch 是 AI Agent 的搜索基础设施，支持垂直域搜索（23个领域），能穿透 JS 混淆、WeChat 登录墙等普通爬虫无法访问的内容。

## Quick Start

```python
import subprocess, os

# 动态获取技能路径（推荐）
# 或者使用当前 host 的实际路径：
skill_dir = r"C:\Users\Administrator\AppData\Local\hermes\skills\openclaw-imports\anysearch"
os.chdir(skill_dir)

# Search
res = subprocess.run([
    "python", f"{skill_dir}/scripts/anysearch_cli.py", "search",
    "--content_types", "web",
    "--max_results", "5",
    "your search query here"
], capture_output=True, text=True, timeout=30)

# Extract full content from a URL
res = subprocess.run([
    "python", f"{skill_dir}/scripts/anysearch_cli.py", "extract",
    "https://example.com/article"
], capture_output=True, text=True, timeout=30)
```

## CLI Scripts Available

| File | Language | Use |
|------|----------|-----|
| `scripts/anysearch_cli.py` | Python | Primary — use this one |
| `scripts/anysearch_cli.js` | Node.js | Alternative |
| `scripts/anysearch_cli.sh` | Bash | Alternative |

Python CLI is preferred on this host.

## API Key

Already configured in `C:/Users/Administrator/.agents/skills/anysearch/.env`:
```
ANYSEARCH_API_KEY=as_sk_22b8c2c1833c05923fc537cb9eecca4a
```

## Capabilities

- **Search**: Query across web with AI-ranked results
- **Extract**: Pull full article/content from a URL (bypasses many JS-gated pages)
- **Supported content types**: `web`, `news`, `image`, `video`, `shopping`, `finance`, `academic`, `forum`

## Known Limitations

- **WeChat articles** (`mp.weixin.qq.com`) — blocked by login gate. AnySearch cannot access them. Workaround: ask user for article title and search for mirrors, or request user paste content directly.
- **`text/plain` rejection** — `extract` only supports `text/html`. Raw files on `raw.githubusercontent.com` are rejected. Workaround: use the rendered GitHub page URL (e.g. `https://github.com/owner/repo/blob/main/README.md`) instead of the raw URL.
- **Empty GitHub Pages subpaths** — some demo/landing pages return minimal content (<200 chars). If extraction returns very little, the page may be empty or behind a redirect.
- **GitHub login banners** — Some GitHub pages show "You must be signed in" banners in extracted content. Extract the raw file or use the raw.githubusercontent.com URL directly when possible.

## Session Learnings (2026-05-21)

- Successfully extracted `Moore-developers/grok-cli` README (both `README.md` and `README.zh-CN.md`) when skill registry had no match.
- Chinese README confirmed: grok-cli uses OAuth via X Premium+/SuperGrok, no separate API key needed.
- AnySearch is the **fallback tool** when registry search fails and you need content from a specific URL.

## Installation

Copied from WorkBuddy at `C:\Users\Administrator\.workbuddy\skills\anysearch\` → `C:/Users/Administrator/.agents/skills/anysearch/`. Not on any public registry — install by copying from a system that already has it, or request the AnySearch team.

## Troubleshooting: Missing CLI Scripts

The skill may be listed as "enabled" but only contain SKILL.md without the `scripts/` directory.
If `scripts/anysearch_cli.py` is missing, copy from WorkBuddy:

```bash
mkdir -p "C:/Users/Administrator/AppData/Local/hermes/skills/openclaw-imports/anysearch/scripts"
cp "C:/Users/Administrator/.workbuddy/skills/anysearch/scripts/anysearch_cli.py" \
   "C:/Users/Administrator/AppData/Local/hermes/skills/openclaw-imports/anysearch/scripts/"
```

Verify with:
```bash
python scripts/anysearch_cli.py search --content_types web --max_results 1 "test query"
```

Discovered 2026-05-29: skill showed "enabled" but scripts/ dir was empty.

## Troubleshooting: Missing CLI Scripts

The skill may be listed as "enabled" but only contain SKILL.md without the `scripts/` directory.
If `scripts/anysearch_cli.py` is missing, copy from WorkBuddy:

```bash
mkdir -p "C:/Users/Administrator/AppData/Local/hermes/skills/openclaw-imports/anysearch/scripts"
cp "C:/Users/Administrator/.workbuddy/skills/anysearch/scripts/anysearch_cli.py" \
   "C:/Users/Administrator/AppData/Local/hermes/skills/openclaw-imports/anysearch/scripts/"
```

Verify with:
```bash
python scripts/anysearch_cli.py search --content_types web --max_results 1 "test query"
```

Discovered 2026-05-29: skill showed "enabled" but scripts/ dir was empty.

## Troubleshooting: Missing CLI Scripts

The skill may be listed as "enabled" but only contain SKILL.md without the `scripts/` directory.
If `scripts/anysearch_cli.py` is missing, copy from WorkBuddy:

```bash
mkdir -p "C:/Users/Administrator/AppData/Local/hermes/skills/openclaw-imports/anysearch/scripts"
cp "C:/Users/Administrator/.workbuddy/skills/anysearch/scripts/anysearch_cli.py" \
   "C:/Users/Administrator/AppData/Local/hermes/skills/openclaw-imports/anysearch/scripts/"
```

Verify with:
```bash
python scripts/anysearch_cli.py search --content_types web --max_results 1 "test query"
```

Discovered 2026-05-29: skill showed "enabled" but scripts/ dir was empty.

## Troubleshooting: Missing CLI Scripts

The skill may be listed as "enabled" but only contain SKILL.md without the `scripts/` directory.
If `scripts/anysearch_cli.py` is missing, copy from WorkBuddy:

```bash
mkdir -p "C:/Users/Administrator/AppData/Local/hermes/skills/openclaw-imports/anysearch/scripts"
cp "C:/Users/Administrator/.workbuddy/skills/anysearch/scripts/anysearch_cli.py" \
   "C:/Users/Administrator/AppData/Local/hermes/skills/openclaw-imports/anysearch/scripts/"
```

Verify with:
```bash
python scripts/anysearch_cli.py search --content_types web --max_results 1 "test query"
```

Discovered 2026-05-29: skill showed "enabled" but scripts/ dir was empty.

## Troubleshooting: Missing CLI Scripts

The skill may be listed as "enabled" but only contain SKILL.md without the `scripts/` directory.
If `scripts/anysearch_cli.py` is missing, copy from WorkBuddy:

```bash
mkdir -p "C:/Users/Administrator/AppData/Local/hermes/skills/openclaw-imports/anysearch/scripts"
cp "C:/Users/Administrator/.workbuddy/skills/anysearch/scripts/anysearch_cli.py" \
   "C:/Users/Administrator/AppData/Local/hermes/skills/openclaw-imports/anysearch/scripts/"
```

Verify with:
```bash
python scripts/anysearch_cli.py search --content_types web --max_results 1 "test query"
```

Discovered 2026-05-29: skill showed "enabled" but scripts/ dir was empty.

## Troubleshooting: Missing CLI Scripts

The skill may be listed as "enabled" but only contain SKILL.md without the `scripts/` directory.
If `scripts/anysearch_cli.py` is missing, copy from WorkBuddy:

```bash
mkdir -p "C:/Users/Administrator/AppData/Local/hermes/skills/openclaw-imports/anysearch/scripts"
cp "C:/Users/Administrator/.workbuddy/skills/anysearch/scripts/anysearch_cli.py" \
   "C:/Users/Administrator/AppData/Local/hermes/skills/openclaw-imports/anysearch/scripts/"
```

Verify with:
```bash
python scripts/anysearch_cli.py search --content_types web --max_results 1 "test query"
```

Discovered 2026-05-29: skill showed "enabled" but scripts/ dir was empty.

## Troubleshooting: Missing CLI Scripts

The skill may be listed as "enabled" but only contain SKILL.md without the `scripts/` directory.
If `scripts/anysearch_cli.py` is missing, copy from WorkBuddy:

```bash
mkdir -p "C:/Users/Administrator/AppData/Local/hermes/skills/openclaw-imports/anysearch/scripts"
cp "C:/Users/Administrator/.workbuddy/skills/anysearch/scripts/anysearch_cli.py" \
   "C:/Users/Administrator/AppData/Local/hermes/skills/openclaw-imports/anysearch/scripts/"
```

Verify with:
```bash
python scripts/anysearch_cli.py search --content_types web --max_results 1 "test query"
```

Discovered 2026-05-29: skill showed "enabled" but scripts/ dir was empty.

## Troubleshooting: Missing CLI Scripts

The skill may be listed as "enabled" but only contain SKILL.md without the `scripts/` directory.
If `scripts/anysearch_cli.py` is missing, copy from WorkBuddy:

```bash
mkdir -p "C:/Users/Administrator/AppData/Local/hermes/skills/openclaw-imports/anysearch/scripts"
cp "C:/Users/Administrator/.workbuddy/skills/anysearch/scripts/anysearch_cli.py" \
   "C:/Users/Administrator/AppData/Local/hermes/skills/openclaw-imports/anysearch/scripts/"
```

Verify with:
```bash
python scripts/anysearch_cli.py search --content_types web --max_results 1 "test query"
```

Discovered 2026-05-29: skill showed "enabled" but scripts/ dir was empty.

## Troubleshooting: Missing CLI Scripts

The skill may be listed as "enabled" but only contain SKILL.md without the `scripts/` directory.
If `scripts/anysearch_cli.py` is missing, copy from WorkBuddy:

```bash
mkdir -p "C:/Users/Administrator/AppData/Local/hermes/skills/openclaw-imports/anysearch/scripts"
cp "C:/Users/Administrator/.workbuddy/skills/anysearch/scripts/anysearch_cli.py" \
   "C:/Users/Administrator/AppData/Local/hermes/skills/openclaw-imports/anysearch/scripts/"
```

Verify with:
```bash
python scripts/anysearch_cli.py search --content_types web --max_results 1 "test query"
```

Discovered 2026-05-29: skill showed "enabled" but scripts/ dir was empty.

## Troubleshooting: Missing CLI Scripts

The skill may be listed as "enabled" but only contain SKILL.md without the `scripts/` directory.
If `scripts/anysearch_cli.py` is missing, copy from WorkBuddy:

```bash
mkdir -p "C:/Users/Administrator/AppData/Local/hermes/skills/openclaw-imports/anysearch/scripts"
cp "C:/Users/Administrator/.workbuddy/skills/anysearch/scripts/anysearch_cli.py" \
   "C:/Users/Administrator/AppData/Local/hermes/skills/openclaw-imports/anysearch/scripts/"
```

Verify with:
```bash
python scripts/anysearch_cli.py search --content_types web --max_results 1 "test query"
```

Discovered 2026-05-29: skill showed "enabled" but scripts/ dir was empty.

## Troubleshooting: Missing CLI Scripts

The skill may be listed as "enabled" but only contain SKILL.md without the `scripts/` directory.
If `scripts/anysearch_cli.py` is missing, copy from WorkBuddy:

```bash
mkdir -p "C:/Users/Administrator/AppData/Local/hermes/skills/openclaw-imports/anysearch/scripts"
cp "C:/Users/Administrator/.workbuddy/skills/anysearch/scripts/anysearch_cli.py" \
   "C:/Users/Administrator/AppData/Local/hermes/skills/openclaw-imports/anysearch/scripts/"
```

Verify with:
```bash
python scripts/anysearch_cli.py search --content_types web --max_results 1 "test query"
```

Discovered 2026-05-29: skill showed "enabled" but scripts/ dir was empty.

## Troubleshooting: Missing CLI Scripts

The skill may be listed as "enabled" but only contain SKILL.md without the `scripts/` directory.
If `scripts/anysearch_cli.py` is missing, copy from WorkBuddy:

```bash
mkdir -p "C:/Users/Administrator/AppData/Local/hermes/skills/openclaw-imports/anysearch/scripts"
cp "C:/Users/Administrator/.workbuddy/skills/anysearch/scripts/anysearch_cli.py" \
   "C:/Users/Administrator/AppData/Local/hermes/skills/openclaw-imports/anysearch/scripts/"
```

Verify with:
```bash
python scripts/anysearch_cli.py search --content_types web --max_results 1 "test query"
```

Discovered 2026-05-29: skill showed "enabled" but scripts/ dir was empty.

## Troubleshooting: Missing CLI Scripts

The skill may be listed as "enabled" but only contain SKILL.md without the `scripts/` directory.
If `scripts/anysearch_cli.py` is missing, copy from WorkBuddy:

```bash
mkdir -p "C:/Users/Administrator/AppData/Local/hermes/skills/openclaw-imports/anysearch/scripts"
cp "C:/Users/Administrator/.workbuddy/skills/anysearch/scripts/anysearch_cli.py" \
   "C:/Users/Administrator/AppData/Local/hermes/skills/openclaw-imports/anysearch/scripts/"
```

Verify with:
```bash
python scripts/anysearch_cli.py search --content_types web --max_results 1 "test query"
```

Discovered 2026-05-29: skill showed "enabled" but scripts/ dir was empty.
