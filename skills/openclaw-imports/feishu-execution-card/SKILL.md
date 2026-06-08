---
name: feishu-execution-card
description: >
  Build and send Feishu execution result cards (执行结果卡片) with correct rendering.
  Covers the turquoise header format, div+background_style for colored blocks,
  and bottom status bar. Supersedes note-element patterns from feishu-lark skill.
  Trigger: "执行结果卡片", "feishu card", "卡片格式", "execution card", "飞书卡片".
---

# Feishu Execution Result Card

Builds properly-rendered Feishu interactive cards for task execution results.
This skill fixes rendering bugs in the base `feishu-lark` skill's card templates.

## Prerequisites

Requires `FEISHU_APP_ID`, `FEISHU_APP_SECRET`, and `FEISHU_HOME_CHANNEL` in `.env`.
See `feishu-lark` skill section 10 for gateway setup.

## Correct Card Structure

```json
{
  "msg_type": "interactive",
  "card": {
    "header": {
      "title": {"tag": "plain_text", "content": "🤖 已完成｜任务标题"},
      "template": "turquoise"
    },
    "elements": [
      {"tag": "markdown", "content": "状态描述文本"},
      {"tag": "markdown", "content": "```python\ncode here\n```"},
      {"tag": "hr"},
      {"tag": "markdown", "content": "**🔧 工具摘要**"},
      {
        "tag": "div",
        "background_style": "blue",
        "text": {"tag": "lark_md", "content": "✅ `terminal` — 终端执行"},
        "margin": {"top": "4px", "bottom": "4px"}
      },
      {"tag": "hr"},
      {
        "tag": "div",
        "background_style": "green",
        "text": {"tag": "lark_md", "content": "**⏱ 0.1s** · **🤖 SkyClaw v1** · **📡 1次** · **📊 80%**"},
        "margin": {"top": "0", "bottom": "0"}
      }
    ]
  }
}
```

## Critical Fixes (vs feishu-lark base skill)

### 1. Use `div` + `background_style`, NOT `note`

**`note` element is broken for status bars:**
- Only supports `plain_text` — no bold, no colors, no markdown
- Progress bar blocks (`████`) render incorrectly
- No background color support

**Correct replacement:**
```json
{"tag": "div", "background_style": "green",
 "text": {"tag": "lark_md", "content": "**⏱ 0.1s** · **🤖 Model**"},
 "margin": {"top": "0", "bottom": "0"}}
```

### 2. Property is `background_style`, NOT `background`

The base skill template (section 11.6) uses `"background": "blue"` — this is WRONG.
Correct property: `"background_style": "blue"`.

### 3. `div.text` uses `content`, not `text`

```json
// ✅ Correct
"text": {"tag": "lark_md", "content": "bold text"}

// ❌ Wrong — renders empty
"text": {"tag": "lark_md", "text": "bold text"}
```

### 4. Code blocks: use `markdown` with triple-backticks, NOT `code` element

The `code` element in App Bot API often renders with empty content.
Safe alternative: `{"tag": "markdown", "content": "```python\ncode\n```"}`

### 5. Bold text in `markdown` elements may not render

Feishu card markdown has limited syntax support. `**bold**` may show as plain text.
Workaround: use emoji prefixes or capitalization for emphasis.

## Color Convention

| Element | Color | Reason |
|---------|-------|--------|
| Header | `turquoise` | User confirmed "Always" (2026-05-30) |
| Tool summary rows | `blue` | Visual distinction |
| Bottom status bar | `green` | Success/completion indicator |

## Sending via curl

```bash
# 1. Get token
TOKEN=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d '{"app_id":"$FEISHU_APP_ID","app_secret":"$FEISHU_APP_SECRET"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin).get('tenant_access_token',''))")

# 2. Send card (content must be double-JSON-encoded)
curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"receive_id":"$FEISHU_HOME_CHANNEL","msg_type":"interactive","content":'"$(python3 -c "import json; print(json.dumps(json.dumps(CARD_DICT)))")"'}'
```

## Pitfalls

1. **App Bot API content must be double-JSON-encoded**: `content` field = `json.dumps(card_json)` string
2. **`send_message` tool cannot send cards** — must use curl/urllib to Feishu Open API
3. **`note` ≠ `div`**: `note` is plain-text-only footer; `div`+`background_style` is for colored blocks
4. **`background` vs `background_style`**: Only `background_style` works. `background` is silently ignored or causes ErrCode 200621
5. **`lark_md` in `div`, `markdown` as standalone element**: Don't mix — `div.text` must use `lark_md` tag
6. **Token truncated in config**: `config.yaml` shows `mcdr8D...BUQn` — must read full secret from `.env` file
