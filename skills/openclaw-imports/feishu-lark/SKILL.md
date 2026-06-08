---
name: feishu-lark
description: >
  Send messages and interactive cards to Feishu (飞书) and Lark channels via webhooks or Bot API.
  Configure Hermes gateway for bidirectional communication (chat with agent from Feishu).
  Create rich-text announcements, marketing updates, and team notifications. Trigger phrases:
  "post to feishu", "feishu message", "lark message", "feishu webhook", "lark webhook",
  "send to feishu", "send to lark", "feishu bot", "lark bot", "飞书", "飞书机器人",
  "connect feishu to hermes", "feishu gateway", "chat with agent from feishu".
allowed-tools:
  - Bash
  - WebFetch
  - WebSearch
---

# Feishu / Lark Messaging Skill

You are a messaging specialist for Feishu (飞书, ByteDance's Chinese workplace platform) and Lark (the international version). Your job is to send messages, interactive cards, and marketing content to Feishu/Lark group chats via Custom Bot Webhooks or the App Bot API.

## References
- [Gateway Troubleshooting: No messages received](references/gateway-no-messages-received.md)
- [hermes-lark-streaming plugin analysis](references/hermes-lark-streaming.md) — CardKit v2.0 streaming cards via AST injection; HTTP path only, not WebSocket mode
- [飞书卡片格式规范（用户偏好）](references/feishu-card-conventions.md) — Header颜色含义、标准结构(build_news_card)、结尾特色
- [执行结果卡片调试记录](references/execution-result-card-debugging.md) — send_message不支持卡片、App Bot API双重编码、code块/加粗/div渲染坑点
- [执行结果卡片 — 已验证可工作的发送脚本](references/execution-result-card-working-script.md) — 2026-05-30 实测通过，含完整 Python 脚本
- [note 元素限制与 div 替代方案](references/note-element-limitations.md) — note不支持富文本、进度条渲染异常、div+background_style修复方案

## Prerequisites

Check which credentials are available:

```bash
echo "FEISHU_WEBHOOK_URL is ${FEISHU_WEBHOOK_URL:+set}"
echo "FEISHU_WEBHOOK_SECRET is ${FEISHU_WEBHOOK_SECRET:+set}"
echo "FEISHU_APP_ID is ${FEISHU_APP_ID:+set}"
echo "FEISHU_APP_SECRET is ${FEISHU_APP_SECRET:+set}"
```

### Two Integration Modes

| Mode | Credentials Required | Capabilities |
|------|---------------------|--------------|
| **Custom Bot Webhook** (simple) | `FEISHU_WEBHOOK_URL` (+ optional `FEISHU_WEBHOOK_SECRET`) | Send text, rich text, interactive cards to a single group |
| **App Bot API** (full featured) | `FEISHU_APP_ID` + `FEISHU_APP_SECRET` | Send to any chat, upload images, at-mention users, manage cards, receive events |

**Hermes gateway note:** If the user says "connect Feishu to Hermes" or wants to chat with the agent from Feishu, use **App Bot API / gateway mode**, not Custom Bot Webhook. See section 10 below for complete gateway setup and troubleshooting. A webhook URL is only for outbound posting to one group.

If no credentials are set, instruct the user:

> **Custom Bot Webhook (quickest setup):**
> 1. Open a Feishu/Lark group chat
> 2. Click the group name at the top to open Group Settings
> 3. Go to **Bots** > **Add Bot** > **Custom Bot**
> 4. Name the bot and optionally set a Signature Verification secret
> 5. Copy the webhook URL and add to `.env`:
>    ```
>    FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/{webhook_id}
>    FEISHU_WEBHOOK_SECRET=your_secret_here  # optional, for signed webhooks
>    ```
>
> **App Bot API (for advanced use):**
> 1. Go to [Feishu Open Platform](https://open.feishu.cn/app) or [Lark Developer Console](https://open.larksuite.com/app)
> 2. Create a new app, enable the Bot capability
> 3. Add required permissions: `im:message:send_as_bot`, `im:chat:readonly`
> 4. Publish and approve the app, then add to `.env`:
>    ```
>    FEISHU_APP_ID=cli_xxxxx
>    FEISHU_APP_SECRET=xxxxx
>    ```

### Webhook URL Formats

- **Feishu (China):** `https://open.feishu.cn/open-apis/bot/v2/hook/{webhook_id}`
- **Lark (International):** `https://open.larksuite.com/open-apis/bot/v2/hook/{webhook_id}`

### API Base URLs

- **Feishu (China):** `https://open.feishu.cn/open-apis`
- **Lark (International):** `https://open.larksuite.com/open-apis`

---

## 1. Custom Bot Webhook Messages

### 1.1 Plain Text Message

```bash
curl -s -X POST "${FEISHU_WEBHOOK_URL}" \
  -H "Content-Type: application/json" \
  -d '{
    "msg_type": "text",
    "content": {
      "text": "Hello from OpenClaudia! This is a test message."
    }
  }'
```

**At-mention everyone in the group:**

```bash
curl -s -X POST "${FEISHU_WEBHOOK_URL}" \
  -H "Content-Type: application/json" \
  -d '{
    "msg_type": "text",
    "content": {
      "text": "<at user_id=\"all\">Everyone</at> Important announcement: new release is live!"
    }
  }'
```

### 1.2 Rich Text Message (Post)

Rich text supports bold, links, at-mentions, and images in a structured format.

```bash
curl -s -X POST "${FEISHU_WEBHOOK_URL}" \
  -H "Content-Type: application/json" \
  -d '{
    "msg_type": "post",
    "content": {
      "post": {
        "zh_cn": {
          "title": "产品更新公告",
          "content": [
            [
              {"tag": "text", "text": "我们很高兴地宣布 "},
              {"tag": "a", "text": "v2.0 版本", "href": "https://example.com/changelog"},
              {"tag": "text", "text": " 已正式发布！"}
            ],
            [
              {"tag": "text", "text": "主要更新："}
            ],
            [
              {"tag": "text", "text": "1. 全新用户界面\n2. 性能提升 50%\n3. 支持暗色模式"}
            ],
            [
              {"tag": "at", "user_id": "all", "user_name": "所有人"}
            ]
          ]
        }
      }
    }
  }'
```

**English version (for Lark):**

```bash
curl -s -X POST "${FEISHU_WEBHOOK_URL}" \
  -H "Content-Type: application/json" \
  -d '{
    "msg_type": "post",
    "content": {
      "post": {
        "en_us": {
          "title": "Product Update Announcement",
          "content": [
            [
              {"tag": "text", "text": "We are excited to announce that "},
              {"tag": "a", "text": "v2.0", "href": "https://example.com/changelog"},
              {"tag": "text", "text": " is now live!"}
            ],
            [
              {"tag": "text", "text": "Key updates:"}
            ],
            [
              {"tag": "text", "text": "1. Brand new UI\n2. 50% performance improvement\n3. Dark mode support"}
            ],
            [
              {"tag": "at", "user_id": "all", "user_name": "Everyone"}
            ]
          ]
        }
      }
    }
  }'
```

### Rich Text Tag Reference

| Tag | Purpose | Attributes |
|-----|---------|------------|
| `text` | Plain text | `text`, `un_escape` (boolean, interpret `\n` etc.) |
| `a` | Hyperlink | `text`, `href` |
| `at` | At-mention | `user_id` (use `"all"` for everyone), `user_name` |
| `img` | Image (App Bot only) | `image_key` (requires uploading image first) |
| `media` | Video/file (App Bot only) | `file_key`, `image_key` |

### 1.3 Signed Webhook Requests

If `FEISHU_WEBHOOK_SECRET` is set, the webhook requires a signature for verification.

**Generate a signed request:**

```bash
# Calculate timestamp and signature
TIMESTAMP=$(date +%s)
STRING_TO_SIGN="${TIMESTAMP}\n${FEISHU_WEBHOOK_SECRET}"
SIGN=$(printf '%b' "${STRING_TO_SIGN}" | openssl dgst -sha256 -hmac "" -binary | openssl base64)

# For proper HMAC-SHA256 signing:
SIGN=$(echo -ne "${TIMESTAMP}\n${FEISHU_WEBHOOK_SECRET}" | openssl dgst -sha256 -hmac "" -binary | base64)

curl -s -X POST "${FEISHU_WEBHOOK_URL}" \
  -H "Content-Type: application/json" \
  -d "{
    \"timestamp\": \"${TIMESTAMP}\",
    \"sign\": \"${SIGN}\",
    \"msg_type\": \"text\",
    \"content\": {
      \"text\": \"Signed message from OpenClaudia.\"
    }
  }"
```

**Feishu signature algorithm details:**
1. Concatenate `timestamp + "\n" + secret` as the string to sign
2. Compute HMAC-SHA256 with an empty key over that string
3. Base64-encode the result
4. Include both `timestamp` and `sign` in the request JSON body

---

## 2. Interactive Card Messages

Interactive cards are the most powerful message format. They support headers, content sections, images, action buttons, and structured layouts.

### 2.1 Basic Card Structure

```json
{
  "msg_type": "interactive",
  "card": {
    "header": {
      "title": {
        "tag": "plain_text",
        "content": "Card Title Here"
      },
      "template": "blue"
    },
    "elements": []
  }
}
```

### Header Color Templates

> **用户规范（2026-05-21）：green 投资/自动化推送（默认）；red 风险提醒；其他按需调用；内容风格保持原样（不用表格堆砌，讲故事方式）**
>
> ⚠️ **已废弃格式（2026-05-21 修正）：不要再用 `tag: "lark_md"` — 这是旧版格式，官方推荐用 `tag: "markdown"`。首次发卡务必先在官方文档确认当前标准格式，曾因用错格式被用户打回重发。**

| Template | Color | Best For |
|----------|-------|----------|
| `green` | Green | **投资/自动化推送默认** |
| `red` | Red | **风险提醒** |
| `blue` | Blue | 通用信息 |
| `orange` | Orange | 提醒 |
| `purple` | Purple | AI/科技感 |
| `wathet` | Light blue | 备用 |
| `turquoise` | Teal | 备用 |
| `grey` | Grey | 普通通知 |

### 2.2 Card Elements Reference

**Markdown Content Block:**

```json
{
  "tag": "markdown",
  "content": "**Bold text** and *italic text*\n[Link text](https://example.com)\nList:\n- Item 1\n- Item 2"
}
```

**Divider:**

```json
{
  "tag": "hr"
}
```

**Note (small gray footer text):**

```json
{
  "tag": "note",
  "elements": [
    {"tag": "plain_text", "content": "Sent via OpenClaudia Marketing Toolkit"}
  ]
}
```

**Image Block:**

```json
{
  "tag": "img",
  "img_key": "img_v2_xxx",
  "alt": {"tag": "plain_text", "content": "Image description"},
  "title": {"tag": "plain_text", "content": "Image Title"}
}
```

**Action Buttons:**

```json
{
  "tag": "action",
  "actions": [
    {
      "tag": "button",
      "text": {"tag": "plain_text", "content": "View Details"},
      "type": "primary",
      "url": "https://example.com/details"
    },
    {
        "tag": "div",
        "text": {"tag": "lark_md", "content": status_bar},
        "background_style": "green",
        "margin": {"top": "0", "bottom": "0"}
    }
  ]
}
```

**Button types:** `primary` (blue), `danger` (red), `default` (gray)

**Multi-column Layout:**

```json
{
  "tag": "column_set",
  "flex_mode": "bisect",
  "columns": [
    {
      "tag": "column",
      "width": "weighted",
      "weight": 1,
      "elements": [
        {"tag": "markdown", "content": "**Left Column**\nContent here"}
      ]
    },
    {
      "tag": "column",
      "width": "weighted",
      "weight": 1,
      "elements": [
        {"tag": "markdown", "content": "**Right Column**\nContent here"}
      ]
    }
  ]
}
```

### Official Card Structure (App Bot API)

> Must use App Bot API, not Webhook. Include `config.wide_screen_mode: True` for full-width cards.

```json
{
  "msg_type": "interactive",
  "card": {
    "config": {"wide_screen_mode": true},
    "header": {
      "template": "green",
      "title": {"tag": "plain_text", "content": "标题"}
    },
    "elements": [
      {"tag": "markdown", "content": "内容（加粗/斜体/列表/链接）"},
      {"tag": "hr"},
      {
        "tag": "action",
        "actions": [{
          "tag": "button",
          "text": {"tag": "plain_text", "content": "查看详情"},
          "type": "primary",
          "url": "https://example.com"
        }]
      },
      {"tag": "note", "elements": [{"tag": "plain_text", "content": "Hermes 助理 | 2026-05-21"}]}
    ]
  }
}
```

**Card elements:** `markdown` (rich content), `hr` (divider), `action`+`button` (CTA), `note` (footer)

### 2.3 Full Card Example: Product Announcement

```bash
curl -s -X POST "${FEISHU_WEBHOOK_URL}" \
  -H "Content-Type: application/json" \
  -d '{
    "msg_type": "interactive",
    "card": {
      "header": {
        "title": {
          "tag": "plain_text",
          "content": "New Feature Launch: AI-Powered Analytics"
        },
        "template": "turquoise"
      },
      "elements": [
        {
          "tag": "markdown",
          "content": "We are thrilled to announce our latest feature!\n\n**AI-Powered Analytics** is now available to all Pro and Enterprise users.\n\nKey highlights:\n- **Smart Insights**: Automatic trend detection and anomaly alerts\n- **Natural Language Queries**: Ask questions in plain English\n- **Predictive Forecasting**: 90-day revenue and growth projections\n- **Custom Dashboards**: Drag-and-drop report builder"
        },
        {
          "tag": "hr"
        },
        {
          "tag": "markdown",
          "content": "**Availability:** Rolling out now, fully live by end of week\n**Documentation:** [View the guide](https://example.com/docs/analytics)\n**Feedback:** Reply in this thread or submit via [feedback form](https://example.com/feedback)"
        },
        {
          "tag": "action",
          "actions": [
            {
              "tag": "button",
              "text": {"tag": "plain_text", "content": "Try It Now"},
              "type": "primary",
              "url": "https://example.com/analytics"
            },
            {
              "tag": "button",
              "text": {"tag": "plain_text", "content": "Read Docs"},
              "type": "default",
              "url": "https://example.com/docs/analytics"
            }
          ]
        },
        {
          "tag": "note",
          "elements": [
            {"tag": "plain_text", "content": "Product Team | Released 2025-01-15"}
          ]
        }
      ]
    }
  }'
```

---

## 3. App Bot API (Full Featured)

The App Bot API requires `FEISHU_APP_ID` and `FEISHU_APP_SECRET`. It provides full messaging capabilities including sending to any chat, uploading images, and managing messages.

### 3.1 Get Tenant Access Token

All App Bot API calls require a `tenant_access_token`. Tokens expire after 2 hours.

```bash
# For Feishu (China)
FEISHU_API_BASE="https://open.feishu.cn/open-apis"

# For Lark (International)
# FEISHU_API_BASE="https://open.larksuite.com/open-apis"

TENANT_TOKEN=$(curl -s -X POST "${FEISHU_API_BASE}/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{
    \"app_id\": \"${FEISHU_APP_ID}\",
    \"app_secret\": \"${FEISHU_APP_SECRET}\"
  }" | python3 -c "import json,sys; print(json.load(sys.stdin).get('tenant_access_token',''))")

echo "Token: ${TENANT_TOKEN:0:10}..."
```

### 3.2 List Chats the Bot Belongs To

```bash
curl -s "${FEISHU_API_BASE}/im/v1/chats?page_size=20" \
  -H "Authorization: Bearer ${TENANT_TOKEN}" | \
  python3 -c "
import json, sys
data = json.load(sys.stdin)
for chat in data.get('data', {}).get('items', []):
    print(f\"Chat ID: {chat['chat_id']}  |  Name: {chat.get('name', 'N/A')}  |  Type: {chat.get('chat_type', 'N/A')}\")
"
```

### 3.3 Send Message to a Chat

```bash
CHAT_ID="oc_xxxxx"  # Replace with actual chat_id

# Send a text message
curl -s -X POST "${FEISHU_API_BASE}/im/v1/messages?receive_id_type=chat_id" \
  -H "Authorization: Bearer ${TENANT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"receive_id\": \"${CHAT_ID}\",
    \"msg_type\": \"text\",
    \"content\": \"{\\\"text\\\": \\\"Hello from the App Bot!\\\"}\"
  }"
```

**Send a rich text message via the API:**

```bash
curl -s -X POST "${FEISHU_API_BASE}/im/v1/messages?receive_id_type=chat_id" \
  -H "Authorization: Bearer ${TENANT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"receive_id\": \"${CHAT_ID}\",
    \"msg_type\": \"post\",
    \"content\": $(python3 -c "
import json
content = {
    'zh_cn': {
        'title': 'App Bot 消息',
        'content': [
            [
                {'tag': 'text', 'text': '这是一条通过 App Bot API 发送的 '},
                {'tag': 'a', 'text': '富文本消息', 'href': 'https://example.com'},
                {'tag': 'text', 'text': '。'}
            ]
        ]
    }
}
print(json.dumps(json.dumps(content)))
")
  }"
```

**Send an interactive card via the API:**

```bash
curl -s -X POST "${FEISHU_API_BASE}/im/v1/messages?receive_id_type=chat_id" \
  -H "Authorization: Bearer ${TENANT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"receive_id\": \"${CHAT_ID}\",
    \"msg_type\": \"interactive\",
    \"content\": $(python3 -c "
import json
card = {
    'header': {
        'title': {'tag': 'plain_text', 'content': 'Marketing Update'},
        'template': 'turquoise'
    },
    'elements': [
        {'tag': 'markdown', 'content': '**Campaign Performance This Week**\n\n- Impressions: **120,450** (+12%)\n- Clicks: **8,320** (+8%)\n- Conversions: **342** (+15%)\n- Cost per Conversion: **\$14.20** (-5%)'},
        {'tag': 'hr'},
        {'tag': 'action', 'actions': [
            {'tag': 'button', 'text': {'tag': 'plain_text', 'content': 'View Full Report'}, 'type': 'primary', 'url': 'https://example.com/report'}
        ]},
        {'tag': 'note', 'elements': [{'tag': 'plain_text', 'content': 'Auto-generated by OpenClaudia Marketing Toolkit'}]}
    ]
}
print(json.dumps(json.dumps(card)))
")
  }"
```

### 3.4 Upload an Image

Upload an image to get an `image_key` for use in cards and rich text messages.

```bash
IMAGE_KEY=$(curl -s -X POST "${FEISHU_API_BASE}/im/v1/images" \
  -H "Authorization: Bearer ${TENANT_TOKEN}" \
  -F "image_type=message" \
  -F "image=@/path/to/image.png" | python3 -c "import json,sys; print(json.load(sys.stdin).get('data',{}).get('image_key',''))")

echo "Image key: ${IMAGE_KEY}"
```

### 3.5 Send to a Specific User (by email or user_id)

```bash
# By email (receive_id_type=email)
curl -s -X POST "${FEISHU_API_BASE}/im/v1/messages?receive_id_type=email" \
  -H "Authorization: Bearer ${TENANT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"receive_id\": \"user@company.com\",
    \"msg_type\": \"text\",
    \"content\": \"{\\\"text\\\": \\\"Direct message from the marketing bot.\\\"}\"
  }"
```

---

## 4. Message Templates

### 4.1 Product Announcement

```bash
send_product_announcement() {
  local TITLE="$1"
  local VERSION="$2"
  local FEATURES="$3"
  local DOCS_URL="$4"
  local CTA_URL="$5"

  curl -s -X POST "${FEISHU_WEBHOOK_URL}" \
    -H "Content-Type: application/json" \
    -d "$(python3 -c "
import json
card = {
    'msg_type': 'interactive',
    'card': {
        'header': {
            'title': {'tag': 'plain_text', 'content': '${TITLE}'},
            'template': 'green'
        },
        'elements': [
            {'tag': 'markdown', 'content': '**Version ${VERSION}** is now available!\n\n${FEATURES}'},
            {'tag': 'hr'},
            {'tag': 'action', 'actions': [
                {'tag': 'button', 'text': {'tag': 'plain_text', 'content': 'Get Started'}, 'type': 'primary', 'url': '${CTA_URL}'},
                {'tag': 'button', 'text': {'tag': 'plain_text', 'content': 'Release Notes'}, 'type': 'default', 'url': '${DOCS_URL}'}
            ]},
            {'tag': 'note', 'elements': [{'tag': 'plain_text', 'content': 'Product Team | $(date +%Y-%m-%d)'}]}
        ]
    }
}
print(json.dumps(card))
")"
}
```

### 4.2 Team Update / Weekly Report

```bash
curl -s -X POST "${FEISHU_WEBHOOK_URL}" \
  -H "Content-Type: application/json" \
  -d '{
    "msg_type": "interactive",
    "card": {
      "header": {
        "title": {"tag": "plain_text", "content": "Weekly Marketing Report - W03 2025"},
        "template": "blue"
      },
      "elements": [
        {
          "tag": "column_set",
          "flex_mode": "bisect",
          "columns": [
            {
              "tag": "column",
              "width": "weighted",
              "weight": 1,
              "elements": [
                {"tag": "markdown", "content": "**Traffic**\n\nSessions: **45,230**\nUnique Visitors: **32,100**\nBounce Rate: **42%**"}
              ]
            },
            {
              "tag": "column",
              "width": "weighted",
              "weight": 1,
              "elements": [
                {"tag": "markdown", "content": "**Conversions**\n\nSignups: **580**\nTrials: **120**\nPaid: **34**"}
              ]
            }
          ]
        },
        {"tag": "hr"},
        {
          "tag": "markdown",
          "content": "**Top Performing Content:**\n1. \"10 Tips for Better SEO\" - 8,200 views\n2. \"Product Comparison Guide\" - 5,100 views\n3. \"Customer Success Story: Acme Corp\" - 3,800 views\n\n**Action Items:**\n- [ ] Publish Q1 campaign landing page\n- [ ] Review ad spend allocation\n- [ ] Schedule social media posts for next week"
        },
        {
          "tag": "action",
          "actions": [
            {
              "tag": "button",
              "text": {"tag": "plain_text", "content": "Full Dashboard"},
              "type": "primary",
              "url": "https://example.com/dashboard"
            }
          ]
        },
        {
          "tag": "note",
          "elements": [
            {"tag": "plain_text", "content": "Marketing Team | Auto-generated weekly report"}
          ]
        }
      ]
    }
  }'
}'
```

---

## 5. Helper: Build and Send Cards Programmatically

For complex or dynamic cards, use Python to construct the JSON payload:

```bash
python3 -c "
import json, subprocess, os

webhook_url = os.environ.get('FEISHU_WEBHOOK_URL', '')
if not webhook_url:
    print('Error: FEISHU_WEBHOOK_URL not set')
    exit(1)

# Build card dynamically
card = {
    'msg_type': 'interactive',
    'card': {
        'header': {
            'title': {'tag': 'plain_text', 'content': 'Dynamic Card Title'},
            'template': 'blue'
        },
        'elements': []
    }
}

# Add content blocks
card['card']['elements'].append({
    'tag': 'markdown',
    'content': 'This card was built programmatically.\n\n**Key metrics:**\n- Users: 10,000\n- Revenue: \$50,000'
})

# Add a divider
card['card']['elements'].append({'tag': 'hr'})

# Add buttons
card['card']['elements'].append({
    'tag': 'action',
    'actions': [
        {
            'tag': 'button',
            'text': {'tag': 'plain_text', 'content': 'Learn More'},
            'type': 'primary',
            'url': 'https://example.com'
        }
    ]
})

# Add footer
card['card']['elements'].append({
    'tag': 'note',
    'elements': [{'tag': 'plain_text', 'content': 'Sent via OpenClaudia'}]
})

payload = json.dumps(card)
result = subprocess.run(
    ['curl', '-s', '-X', 'POST', webhook_url,
     '-H', 'Content-Type: application/json',
     '-d', payload],
    capture_output=True, text=True
)
print(result.stdout)
"
```

---

## 6. Bilingual Support (Chinese + English)

When sending messages that need both Chinese and English content, use the rich text `post` format which supports multiple locales. Feishu will display the locale matching the user's language setting.

```bash
curl -s -X POST "${FEISHU_WEBHOOK_URL}" \
  -H "Content-Type: application/json" \
  -d '{
    "msg_type": "post",
    "content": {
      "post": {
        "zh_cn": {
          "title": "重要通知：系统维护",
          "content": [
            [
              {"tag": "text", "text": "我们将于 "},
              {"tag": "text", "text": "1月25日 22:00-02:00 (北京时间)", "un_escape": true},
              {"tag": "text", "text": " 进行系统维护。"}
            ],
            [
              {"tag": "text", "text": "维护期间服务将暂时不可用。如有问题请联系 "},
              {"tag": "a", "text": "技术支持", "href": "https://example.com/support"},
              {"tag": "text", "text": "。"}
            ]
          ]
        },
        "en_us": {
          "title": "Important: Scheduled Maintenance",
          "content": [
            [
              {"tag": "text", "text": "We will perform scheduled maintenance on "},
              {"tag": "text", "text": "January 25, 10:00 PM - 2:00 AM (CST)"},
              {"tag": "text", "text": "."}
            ],
            [
              {"tag": "text", "text": "Services will be temporarily unavailable. For questions, contact "},
              {"tag": "a", "text": "Support", "href": "https://example.com/support"},
              {"tag": "text", "text": "."}
            ]
          ]
        }
      }
    }
  }'
```

---

## 7. Error Handling

### Webhook Response Codes

| Code | StatusMessage | Meaning |
|------|---------------|---------|
| 0 | `"success"` | Message sent successfully |
| 9499 | `"Bad Request"` | Malformed JSON or missing required fields |
| 19001 | `"param invalid"` | Invalid msg_type or content format |
| 19002 | `"sign match fail"` | Signature verification failed (check timestamp and secret) |
| 19021 | `"request too fast"` | Rate limit: max 100 messages per minute per webhook |
| 19024 | `"bot not in chat"` | Bot has been removed from the group |

### Common Troubleshooting

**Message not delivered:**
- Verify the webhook URL is correct and the bot is still in the group
- Check that `msg_type` matches the content structure
- For signed webhooks, ensure the timestamp is within 1 hour of current time

**Card not rendering:**
- Validate JSON structure: header and elements are both required
- Button URLs must start with `http://` or `https://`
- Markdown in cards supports a limited subset: bold, italic, links, lists, tables

**API token errors:**
- Tenant access tokens expire after 2 hours; re-fetch before sending
- Ensure the app has been published and approved in the developer console
- Verify `im:message:send_as_bot` permission is granted

### Rate Limits

| Integration | Limit |
|-------------|-------|
| Custom Bot Webhook | 100 messages/minute per webhook |
| App Bot API (messages) | 50 messages/second per app |
| App Bot API (token refresh) | 500 requests/hour |

---

## 8. Workflow: Post Marketing Content to Feishu/Lark

When the user asks to send marketing content to Feishu or Lark, follow this workflow:

### Step 1: Check Credentials

Verify that `FEISHU_WEBHOOK_URL` or `FEISHU_APP_ID` + `FEISHU_APP_SECRET` are set. If not, guide the user through setup.

### Step 2: Determine Message Type

| User Intent | Recommended Format |
|-------------|-------------------|
| Quick text update | Plain text (`msg_type: text`) |
| Formatted announcement | Rich text (`msg_type: post`) |
| Marketing report with metrics | Interactive card with columns |
| Product launch | Interactive card with buttons |
| Event notification | Interactive card with CTA buttons |
| Alert or warning | Interactive card with `red`/`orange` header |

### Step 3: Compose the Message

- Use the appropriate template from section 4
- Adapt content to the user's requirements
- For bilingual groups, provide both `zh_cn` and `en_us` content

### Step 4: Preview and Confirm

Show the user the full JSON payload before sending. Explain what the message will look like.

**Never auto-send without explicit user confirmation.**

### Step 5: Send

Execute the curl command and report the response.

### Step 6: Verify

Check the response code. If `code: 0`, the message was delivered. If there is an error, troubleshoot using the error table above.

---

## 9. Advanced: Message Card JSON Schema Quick Reference

```
{
  "msg_type": "interactive",
  "card": {
    "header": {                          // Required
      "title": {
        "tag": "plain_text",
        "content": "string"
      },
      "template": "blue|green|red|..."   // Header color
    },
    "elements": [                        // Required, array of blocks
      {"tag": "markdown", "content": "..."}, // Rich content
      {"tag": "hr"},                         // Divider line
      {"tag": "img", "img_key": "...", "alt": {...}}, // Image
      {                                      // Multi-column layout
        "tag": "column_set",
        "flex_mode": "bisect|trisect|...",
        "columns": [
          {"tag": "column", "width": "weighted", "weight": 1, "elements": [...]}
        ]
      },
      {                                      // Action buttons
        "tag": "action",
        "actions": [
          {"tag": "button", "text": {...}, "type": "primary|danger|default", "url": "..."}
        ]
      },
      {                                      // Footer note
        "tag": "note",
        "elements": [{"tag": "plain_text", "content": "..."}]
      }
    ]
  }
}
```

---

## 10. Hermes Gateway: Bidirectional Communication Setup

The Hermes gateway enables **bidirectional** communication: the agent can send messages to Feishu/Lark AND receive messages from users. This is different from webhooks (outbound only).

### 10.1 Prerequisites

- Feishu/Lark App created at [https://open.feishu.cn/app](https://open.feishu.cn/app) (China) or [https://open.larksuite.com/app](https://open.larksuite.com/app) (International)
- App ID and App Secret
- Bot capability enabled in the app

### 10.2 Gateway Configuration

Add to `~/.hermes/.env` or `~/AppData/Local/hermes/.env`:

```bash
FEISHU_APP_ID=cli_xxxxx
FEISHU_APP_SECRET=xxxxx
FEISHU_DOMAIN=feishu          # or 'lark' for international
FEISHU_CONNECTION_MODE=websocket
```

Set the home channel in `~/AppData/Local/hermes/config.yaml`:

```yaml
gateway:
  feishu:
    home_channel: oc_xxxxx    # Group chat_id or private chat_id
```

**Get chat_id:**
- For group chats: Use the App Bot API (section 3.2) to list chats
- For private chats: The chat_id format is `oc_` followed by a hash

### 10.3 Critical Step: Configure Event Subscriptions in Feishu Open Platform

**This is the most commonly missed step.** Even if the gateway connects successfully via WebSocket, it will NOT receive messages unless event subscriptions are configured.

#### Steps:

1. **Open Feishu Open Platform**
   - Go to [https://open.feishu.cn/app](https://open.feishu.cn/app) (China) or [https://open.larksuite.com/app](https://open.larksuite.com/app) (International)
   - Select your app

2. **Navigate to Event Configuration (事件配置)**
   - Left sidebar: Click "事件与回调" (Events & Callbacks) → "事件配置" (Event Configuration)

3. **Set Subscription Method to WebSocket**
   - Click "订阅方式" (Subscription Method)
   - Select "使用长连接接收事件" (Use long connection to receive events) — this should show a green "推荐" (Recommended) badge
   - **Do NOT use "配置请求网址" (Configure request URL)** — that's for HTTP callbacks, not gateway mode

4. **Add Required Events**
   - Click the blue "添加事件" (Add Event) button in the top right
   - Search for and add: **`im.message.receive_v1`** (接收消息)
   - This event is REQUIRED to receive user messages sent to the bot

5. **Grant Required Permissions**
   - The event will prompt you to enable permissions
   - Required permissions:
     - `im:message` (获取与发送单聊、群组消息)
     - `im:message:send_as_bot` (以应用身份发消息)
   - Go to "权限管理" (Permission Management) in the left sidebar and enable these

6. **Publish the App Version**
   - If you modified events or permissions, go to "版本管理与发布" (Version Management & Publishing)
   - Click "创建版本" (Create Version) → "申请发布" (Apply for Publishing)
   - For enterprise self-built apps, publishing is usually instant (no review needed)

7. **Set Availability Scope**
   - Go to "可用性" (Availability) in the left sidebar
   - Ensure your Feishu account is in the "可用范围" (Available Scope)
   - Or set to "全员可用" (Available to All)

### 10.4 Start the Gateway

```bash
hermes gateway start
```

**Expected log output:**

```
Hermes Gateway Starting...
Messaging platforms + cron scheduler
Press Ctrl+C to stop

[2026-05-18 13:09:56] ✓ feishu connected (feishu domain)
[2026-05-18 13:09:56] WebSocket URL: wss://msg-frontier.feishu.cn/ws/v2/...
```

### 10.5 Verify Bidirectional Communication

**Test outbound (agent → Feishu):**

```bash
hermes send feishu "Test message from Hermes"
```

**Test inbound (Feishu → agent):**

1. Open the Feishu group or private chat configured as `home_channel`
2. Send a message to the bot
3. Check gateway logs: `tail -f ~/AppData/Local/hermes/logs/gateway.log`
4. You should see incoming message events in the logs

### 10.6 Troubleshooting

**For detailed troubleshooting of the "gateway connected but no messages received" issue, see `references/gateway-no-messages-received.md`.**

#### Gateway connects but no messages received

**Symptom:** Gateway logs show `✓ feishu connected` but when you send messages in Feishu, nothing appears in the logs.

**Root cause:** Event subscriptions not configured in Feishu Open Platform.

**Fix:**
1. Go to Feishu Open Platform → Your App → "事件配置" (Event Configuration)
2. Check if "已添加事件" (Added Events) list is empty
3. If empty, click "添加事件" (Add Event) and add `im.message.receive_v1`
4. Ensure subscription method is "使用长连接接收事件" (WebSocket), not HTTP callback
5. Publish the new app version if prompted
6. **No need to restart the gateway** — Feishu will start pushing events through the existing WebSocket connection

#### "No user allowlists configured" warning

**Symptom:** Gateway logs show:

```
WARNING: No user allowlists configured. All unauthorized users will be rejected.
```

**Fix:** Add to `.env`:

```bash
GATEWAY_ALLOW_ALL_USERS=true
```

Or configure platform-specific allowlists:

```bash
FEISHU_ALLOWED_USERS=ou_xxxxx;ou_yyyyy;
```

Restart the gateway after changing `.env`.

#### "Feishu dependencies not installed" error

**Symptom:** `hermes send feishu` fails with:

```
Feishu dependencies not installed. Run: pip install 'hermes-agent[feishu]'
```

**Fix:**

```bash
pip install 'hermes-agent[feishu]'
```

This installs `lark-oapi`, `qrcode`, and other Feishu-specific dependencies.

#### Wrong .env file location

**Symptom:** Changes to `.env` have no effect.

**Check which .env file Hermes reads:**

```bash
hermes config env-path
```

**Common locations:**
- Windows: `C:\Users\<user>\AppData\Local\hermes\.env`
- Linux/macOS: `~/.config/hermes/.env` or `~/.hermes/.env`

**Do NOT edit** `~/.hermes/.env` if Hermes reads from `AppData/Local/hermes/.env`.

#### Gateway process management

**Check if gateway is running:**

```bash
# Windows (Git Bash)
ps aux | grep "hermes gateway"

# Or check logs
tail -20 ~/AppData/Local/hermes/logs/gateway.log
```

**Stop the gateway:**

```bash
# Find PID
ps aux | grep "hermes gateway"

# Kill process
kill <PID>
```

**Restart the gateway:**

```bash
hermes gateway stop
hermes gateway start
```

### 10.7 Webhook vs Gateway: When to Use Which

| Feature | Custom Bot Webhook | Hermes Gateway (App Bot) |
|---------|-------------------|--------------------------|
| **Direction** | Outbound only (agent → Feishu) | Bidirectional (agent ↔ Feishu) |
| **Setup complexity** | Very simple (1 minute) | Moderate (requires app + event config) |
| **Use case** | Notifications, alerts, reports | Interactive chat with the agent |
| **Credentials** | Webhook URL only | App ID + App Secret |
| **Event subscriptions** | Not needed | **Required** (`im.message.receive_v1`) |
| **Permissions** | None | `im:message`, `im:message:send_as_bot` |
| **Infrastructure** | None (just curl) | Gateway process must run continuously |

**Rule of thumb:**
- User wants to **send notifications to Feishu** → Use webhook (section 1-2)
- User wants to **chat with the agent from Feishu** → Use gateway (section 10)

---

## 11. Hermes 推送卡片标准格式（必须遵守）

Hermes 主动推送统一使用 App Bot API，不使用 Webhook。飞书群 ID：`oc_a9f3e61c8afd6218eb597a1e9f542cc7`

### 11.1 标准卡片结构

```python
import urllib.request, json, datetime

APP_ID = "cli_aa82fa272538dcc8"
APP_SECRET = "mcdr8DXqH4iNWJNir6a70dhYold6BUQn"

def get_token():
    data = json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode()
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=data, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        result = json.loads(resp.read())
        # tenant_access_token is at TOP LEVEL, not under result['data']
        return result.get('tenant_access_token', '')

def send_hermes_card(chat_id, title, content_md, template="purple",
                      status_bar="", note="Hermes 助理 | 自动生成"):
    """Hermes 标准推送卡片"""
    token = get_token()
    # 底部状态栏
    if status_bar:
        footer = {"tag": "note", "elements": [{"tag": "plain_text", "content": status_bar}]}
    else:
        footer = {"tag": "note", "elements": [{"tag": "plain_text", "content": note}]}

    card = {
        "header": {
            "title": {"tag": "plain_text", "content": f"✍️ 已完成 | {title}"},
            "template": template
        },
        "elements": [
            {"tag": "markdown", "content": content_md},
            {"tag": "hr"},
            {
                "tag": "column_set", "flex_mode": "bisect", "columns": [
                    {"tag": "column", "width": "weighted", "weight": 1,
                     "elements": [{"tag": "markdown", "content": "**状态**\n✅ 正常运行中\n**时间：** " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}]},
                    {"tag": "column", "width": "weighted", "weight": 1,
                     "elements": [{"tag": "markdown", "content": "**待处理**\n⏳ 等待下一步指令"}]}
                ]
            },
            footer
        ]
    }
    payload = json.dumps({
        "receive_id": chat_id,
        "msg_type": "interactive",
        "content": json.dumps(card)
    }).encode('utf-8')
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id",
        data=payload,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())
```

**配色规范（2026-05-21 用户确认）：**
- `green` — 投资/自动化推送（**默认**）
- `red` — 风险提醒
- `blue` — 通用信息
- `orange` — 提醒
- `purple` — AI/科技感
- `grey` — 普通通知

### 11.2 实时状态栏（底部 note）

底部 note 显示运行时状态，格式与终端一致：

```
⏱ {耗时} · {模型名} · 调用API {N} 次 · 上下文 {已用k}/{上限k} [{进度条}] {百分比}%
```

**示例：**
```
⏱ 1m 19s · LongCat-2.0-Preview · 调用API 6 次 · 上下文 56.5k/256.0k [██░░░░░░░░] 22.1%
```

底部 note 显示运行时状态，格式与终端一致（**用户已确认的标准格式**）：

```
⏱ {耗时} · {任务名} · 新增 {N} 个基因 · 累计 {N} 个 · 扫描 {N} 个仓库
```

**示例：**
```
⏱ 1m 19s · hermes-self-evolution · 新增 3 个基因 · 累计 28 个 · 扫描 6 个仓库
```

在 `note` 元素的 `content` 字段中传入上述格式字符串即可。

### 11.3 何时用实时 PATCH，何时只用最终结果（重要）

**不要**在任务执行过程中实时 PATCH 更新卡片。理由：
- 每次 PATCH 都是一次 API 调用 + LLM 上下文消耗
- 刷屏干扰体验，用户真正需要的是结果而不是过程直播
- cron 任务的 deliver 机制本身就会触发通知，再叠加 PATCH 会造成重复

**推荐策略：只推送最终结果**

| 场景 | 做法 |
|------|------|
| Cron 定时任务 | `deliver=local`，脚本执行完毕后自己调用 `send_hermes_card()` 发送最终结果卡片 |
| 用户发起的即时任务 | 任务完成后发一条最终卡片（成功/失败各一种 template） |
| 超长任务（>30分钟） | 开始发一条"启动"卡片，结束后 PATCH 为完成状态（最多 1 次中间更新） |

**Cron 任务发飞书的标准模式：**

```yaml
# cronjob 配置
deliver: local        # 不要让 cron 原生 deliver 发通知
no_agent: true        # 脚本自己处理所有逻辑
script: python <path_to_script.py>
```

脚本内部在任务完成后调用 `send_hermes_card()` 发送最终结果。这样飞书只收到一条完整的结果卡片，不会重复通知。

**不要做的事情：**
- 每分钟 PATCH 更新进度条
- 循环内打印日志并实时推送
- cron 的 deliver 设为 `origin` 且脚本也发卡片（重复推送）

### 11.4 消息实时更新（PATCH）

仅在超长任务（>30分钟）场景下，定期刷新卡片状态：

```python
def patch_hermes_card(message_id, elements, token):
    """PATCH 更新已发送卡片的 elements（含底部状态栏）"""
    payload = json.dumps({
        "content": json.dumps({"elements": elements})
    }).encode('utf-8')
    req = urllib.request.Request(
        f"https://open.feishu.cn/open-apis/im/v1/messages/{message_id}",
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    )
    req.get_method = lambda: 'PATCH'
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())
```

**实时更新模式：**
1. 发送初始卡片，记录返回的 `message_id`
2. 每次状态变化：构建新的 `elements` 数组，PATCH 更新
3. 任务结束：最后一次 PATCH 更新为最终状态

**注意：** PATCH 只能更新 `elements`，不能修改 `header`。飞书卡片更新有频率限制，避免超过 5 次/秒。

### 11.5 使用示例

```python
# 发送初始卡片（带进度条）
send_hermes_card(
    chat_id="oc_a9f3e61c8afd6218eb597a1e9f542cc7",
    title="evolver.py 执行中",
    content_md="**基因提取进度**\n\n正在扫描 6 个仓库...\n当前：core-engine",
    template="purple",
    status_bar="⏱ 0m 0s · LongCat-2.0-Preview · 调用API 0 次 · 上下文 0.0k/256.0k [░░░░░░░░░░] 0.0%"
)
```

### 11.6 执行结果卡片模板（Execution Result Card）

用户偏好的任务执行结果展示格式，模拟深色主题终端风格：

```python
def send_execution_result_card(chat_id, title, status_text, code_lines, explanation,
                                tool_summaries, elapsed, model, api_calls, context_used,
                                context_max, pct, template="blue"):
    """发送执行结果卡片，带工具摘要和底部状态栏"""
    # 代码块
    code_content = "\n".join(code_lines) if code_lines else ""
    code_block = f"```{code_content}```" if code_content else ""

    # 工具摘要 — 每行一个 div，蓝色背景
    # 注意：App Bot API 中 div+lark_md+background 可能报 ErrCode 200621
    # 安全替代：用 note 元素（无背景色但兼容性好）
    tool_elements = []
    for tool in tool_summaries:
        tool_elements.append({
            "tag": "div",
            "text": {"tag": "lark_md", "content": f"🔵 `{tool['name']}` ✅ 完成 · {tool['duration']}s · `{tool['args']}`"},
            "background_style": "blue",
            "margin": {"top": "4px", "bottom": "4px"}
        })

    # 底部状态栏 — 绿色背景
    status_bar = f"⏱ *{elapsed}* · {model} · 调用API {api_calls} 次 · 上下文 {context_used}/{context_max} [{'█' * int(pct/10) + '░' * (10 - int(pct/10))}] {pct}%"

    card = {
        "header": {
            "title": {"tag": "plain_text", "content": f"🤖 已完成｜{title}"},
            "template": "turquoise"  # 用户偏好：执行结果卡片统一用 turquoise
        },
        "elements": [
            {"tag": "markdown", "content": status_text},
            {"tag": "code", "text": code_content, "language": "text"} if code_content else None,
            {"tag": "markdown", "content": explanation},
            {"tag": "hr"},
            {"tag": "markdown", "content": "**🔧 工具摘要**"},
        ] + tool_elements + [
            {"tag": "hr"},
            {"tag": "div", "text": {"tag": "lark_md", "content": status_bar}, "background": "green"}
        ]
    }
    # 过滤 None
    card["elements"] = [e for e in card["elements"] if e is not None]
    # 然后调用 send_hermes_card 或直接用 API 发送
```

**颜色含义：**
- 标题栏 `turquoise` — 通用执行结果（用户偏好，2026-05-30 确认"Always"）
- 工具行 `background: "blue"` — 每个工具调用（注意：App Bot API 中 `div`+`lark_md`+`background` 可能报 ErrCode 200621，见坑点 5）
- 底部状态栏 `background: "green"` — 运行时状态

**可用背景色：** `blue`, `green`, `red`, `orange`, `yellow`, `purple`, `grey`, `wathet`, `turquoise`

---

### ⚠️ 坑点 (Pitfalls)

1. **Terminal timeout 上限 600s**：`terminal` 工具 foreground 模式最大 timeout 为 600 秒。设置 `timeout=10000` 会被拒绝并报错。如需长时间操作，用 `background=true` + `notify_on_complete=true`。

2. **App Bot API 发卡片时 content 需双重 JSON 编码**：`content` 字段必须是 `json.dumps(card_json)`（字符串化的 JSON），不是直接传 JSON 对象。

3. **`send_message` 工具不支持 interactive card**：`send_message` 只支持纯文本和 Markdown。要发带颜色的卡片，必须用飞书 Open API 直接调用（Section 3.3 或 11.1 的方法）。

4. **`lark_md` vs `markdown` tag**：`div` 元素内用 `tag: "lark_md"`，独立元素用 `tag: "markdown"`。混用会导致渲染失败。

5. **`div` + `background` + `lark_md` 在 App Bot API 中的坑**：
   - `div` + `background` 在 App Bot API 中**可以工作**（2026-05-30 实测通过），但 JSON 结构必须严格正确
   - `div.text` 必须是 `{"tag": "lark_md", "content": "..."}` — 注意是 `content` 不是 `text`
   - 如果 `content` 字段缺失或拼错，背景色块会渲染但内容为空
   - Webhook 模式下也可能报 ErrCode 200621（`parse card json err`），此时降级为 `note` 元素
   - **安全替代方案**：用 `note` 元素（无背景色但兼容性好），或用 `markdown` 代码块模拟效果

6. **`code` 元素在 App Bot API 中内容为空**：
   - 卡片 JSON 中 `{"tag": "code", "text": "...", "language": "text"}` 结构正确
   - 但如果 `content` 字段双重 JSON 编码出错，code 块的 `text` 内容可能被吞掉
   - **排查方法**：用 `python3 -c "import json; print(json.dumps(json.dumps(card)))"` 验证双重编码
   - **安全替代**：用 `markdown` 元素内嵌 ````text...``` 代码块，渲染效果相同且更可靠

7. **`markdown` 元素中加粗（`**bold**`）不渲染**：
   - 飞书卡片的 `markdown` 元素对 Markdown 语法支持有限
   - `**加粗**` 在某些卡片版本中不生效，显示为纯文本
   - **替代方案**：用 emoji 前缀（如 `▶`、`•`）或大写字母突出关键信息，不依赖加粗

6. **执行结果卡片标题栏颜色**：用户要求所有执行结果统一用 `turquoise`（青绿色），不是 `blue`。2026-05-30 用户确认 "Always"。

8. **`note` 元素不支持富文本（2026-05-30 确认）**：
   - `note` 元素只能包含 `plain_text` 子元素，不支持 `lark_md` 或任何 Markdown 格式
   - 进度条方块字符（`████`）在 `note` 中可能渲染异常
   - 无法在 `note` 中加粗、变色或设置背景色
   - **修复方案**：用 `div` + `background_style` 替代 `note`，配合 `lark_md` 文本实现彩色背景 + 格式化内容：
     ```json
     {
       "tag": "div",
       "background_style": "green",
       "text": {"tag": "lark_md", "content": "**⏱ 0.2s** · **🤖 SkyClaw v1** · **📡 1次** · **📊 80%**"},
       "margin": {"top": "8px", "bottom": "0"}
     }
     ```
   - `background_style` 支持值：`blue`, `green`, `yellow`, `red`, `gray` 等
   - 如果只需要纯文本脚注（无背景色需求），`note` 元素仍然适用

9. **执行结果卡片标题栏颜色**：用户要求所有执行结果统一用 `turquoise`（青绿色），不是 `blue`。2026-05-30 用户确认 "Always"。

10. **App Bot API: `receive_id` 必须放在 POST body 中**：
   - 飞书消息发送 API 的 `receive_id` 参数必须放在请求体（POST body）中，不能放在 URL 查询参数里
   - ❌ 错误：`/im/v1/messages?receive_id_type=chat_id&receive_id=oc_xxx`
   - ✅ 正确：URL 只带 `receive_id_type=chat_id`，`receive_id` 放在 JSON body 中
   - 如果放在 URL 里会报 `invalid receive_id` 错误（code 230001）

11. **Token 响应结构：`tenant_access_token` 在顶层**：
   - 飞书 token API 返回的 `tenant_access_token` 在响应顶层，不在 `data` 字段下
   - ❌ 错误：`result['data']['tenant_access_token']`
   - ✅ 正确：`result['tenant_access_token']`
   - 响应格式：`{"code": 0, "expire": 2917, "msg": "ok", "tenant_access_token": "t-xxx"}`

12. **App Secret 在 config.yaml 中被截断**：
   - `hermes config show` 或 `config.yaml` 中 app_secret 显示为 `mcdr8D...BUQn`（截断）
   - 必须从 `.env` 文件读取完整值：`grep FEISHU_APP_SECRET ~/.hermes/.env | cut -d'=' -f2-`
   - 用 Python 读取最可靠：遍历 .env 文件行，找到 `FEISHU_APP_SECRET=` 开头的行

### 11.8 安全/情报通报模板 (Security Intel Template)

适用于高危漏洞、投毒攻击、技术预警。使用 `red` 或 `orange` 标题。

```python
content_md = """**【预警通报】{标题}**

**通报来源：** {来源}
**风险等级：** <font color='red'>**高危 (Urgent)**</font>
**影响范围：** {范围}

---

### 🚨 攻击详情
1. **{要点1}**：{描述}
2. **{要点2}**：{描述}

### 🛡️ 应急处置建议
- **[立即行动]** {步骤1}
- **[环境检查]** {步骤2}
- **[安全固化]** {步骤3}

---
"""
```

**坑点排查 (Pitfalls):**
- **API 基地址错误**：使用 `urllib` 或 `requests` 直接调用时，URL **必须** 包含 `/open-apis/` 前缀。
  - ✅ `https://open.feishu.cn/open-apis/im/v1/messages`
  - ❌ `https://open.feishu.cn/im/v1/messages` (会导致 404 Not Found)
- **Markdown 样式限制**：飞书卡片不支持所有 Markdown 语法（如 `<font>` 仅在部分版本/字段生效），优先使用加粗和列表。
- **Terminal timeout 上限 600s**：`terminal` 工具 foreground 模式最大 timeout 为 600 秒，不可设更高值。
- **`send_message` 不支持 interactive card**：发带颜色/背景的卡片必须走飞书 Open API，不能用 `send_message` 工具。
- **App Bot API content 需双重 JSON 编码**：`content` 字段必须是 `json.dumps(card_json)` 字符串，不是直接传对象。

See also section 11.6 for the execution result card template and additional pitfalls.

---

### 用户消息格式约定（必须遵守）

所有主动推送的消息统一使用以下格式，禁止偏离：

```
✍️ 已完成 | [状态词，一句话概括]

[主要信息内容]

---
[可选：补充说明/引导互动]
```

- 顶部标题：`✍️ 已完成 | ` 开头，后跟简短状态词（不用"处理结果"等通用词）
- 主要内容：简洁条目，重点加粗
- 分隔线 `---` 用于区分正文和底部引导
- 不用文章总结模板，除非用户明确要求总结文章
- 不用冗长的解释性前缀（如"好的，我来帮你..."）

**示例：**
```
✍️ 已完成 | Rust 编译错误已定位

发现 4 个编译错误，均在 gene.rs 中：
1. **函数未定义**：xxx
2. **类型不匹配**：xxx

---
错误修复后执行 cargo build --release 验证。
```

- **Start with webhooks.** Custom Bot Webhooks require zero code infrastructure and can be set up in under a minute.
- **Use interactive cards** for anything beyond simple text. They are more readable and actionable.
- **Include action buttons** in every marketing card. Drive recipients to a landing page, dashboard, or sign-up form.
- **Leverage bilingual support** if your team uses both Feishu and Lark, or has members in China and internationally.
- **Respect rate limits.** For bulk messaging (e.g., sending to multiple groups), add a 1-second delay between requests.
- **Test in a private group first** before sending to large team channels.
- **Keep card content concise.** Cards have a maximum content size of approximately 30KB. For very long reports, link to an external page.
- **Use the Feishu Message Card Builder** for visual card design: [https://open.feishu.cn/tool/cardbuilder](https://open.feishu.cn/tool/cardbuilder) (Feishu) or [https://open.larksuite.com/tool/cardbuilder](https://open.larksuite.com/tool/cardbuilder) (Lark).
