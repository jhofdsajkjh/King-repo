# 飞书卡片格式规范（用户偏好，2026-05-21）

## Header 颜色含义

> 用户明确要求：green 投资/自动化推送（默认）；red 风险提醒；其他按需调用

| 颜色 | 含义 | 场景 |
|------|------|------|
| `green` | 绿色 | **投资/自动化推送默认** |
| `red` | 红色 | **风险提醒** |
| `blue` | 蓝色 | 通用信息 |
| `orange` | 橙色 | 提醒 |
| `purple` | 紫色 | AI/科技感 |
| `wathet` | 浅蓝 | 备用 |
| `turquoise` | 青色 | 备用 |
| `grey` | 灰色 | 普通通知 |

## 标准卡片结构（App Bot API 官方格式）

**必须使用 App Bot API，不使用 Webhook。**

```python
import urllib.request, json, datetime

APP_ID = "cli_aa82fa272538dcc8"
APP_SECRET = "mcdr8DXqH4iNWJNir6a70dhYold6BUQn"
CHAT_ID = "oc_a9f3e61c8afd6218eb597a1e9f542cc7"

def get_token():
    data = json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode()
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=data, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read()).get('tenant_access_token', '')

def send_card(title, content_md, template="green", button_text="查看详情", button_url="https://example.com"):
    token = get_token()
    card = {
        "config": {"wide_screen_mode": True},
        "header": {
            "template": template,
            "title": {"tag": "plain_text", "content": title}
        },
        "elements": [
            {"tag": "markdown", "content": content_md},
            {"tag": "hr"},
            {
                "tag": "action",
                "actions": [{
                    "tag": "button",
                    "text": {"tag": "plain_text", "content": button_text},
                    "type": "primary",
                    "url": button_url
                }]
            },
            {
                "tag": "note",
                "elements": [{"tag": "plain_text", "content": f"Hermes 助理 | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"}]
            }
        ]
    }
    payload = {
        "receive_id": CHAT_ID,
        "msg_type": "interactive",
        "content": json.dumps(card)
    }
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id",
        data=json.dumps(payload).encode('utf-8'),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())

# 使用示例
send_card(
    title="📊 A股行情快报 | 2026-05-21",
    content_md="**今日重点：**\n1. 半导体板块继续放量\n2. AI算力资金小幅流入\n3. 绿电政策催化增强\n\n**老铁判断：**\n短线看资金强度，中线看政策持续性。",
    template="green",
    button_text="查看详情",
    button_url="https://example.com"
)
```

## ⚠️ 格式注意

- **不要用 `tag: "lark_md"`** — 这是旧版/非官方格式，会导致渲染异常
- **正确格式：用 `tag: "markdown"`**（官方推荐的富文本组件）
- 曾因混用旧格式导致卡片发到飞书后显示异常，被用户打回重学官方标准
- 如不确定当前标准格式，先查官方文档再发卡

## 卡片元素说明

| 元素 | tag | 说明 |
|------|-----|------|
| 富文本 | `markdown` | 官方推荐的卡片内容组件，支持加粗/斜体/列表/链接等 |
| 分割线 | `hr` | 分隔内容用 |
| 按钮 | `action` + `button` | type: primary(蓝)/danger(红)/default(灰) |
| 底部标注 | `note` | 灰底小字，用于时间戳/来源说明 |

## 移动端阅读优化（经验总结）

> ⚠️ 2026-05-22 根据用户反馈迭代总结：手机飞书阅读优先，格式简洁 > 花哨

**核心教训：**
- 第一版卡片被用户打回："不够整齐易懂，有点乱"
- 根因：分隔线过多（每行都隔）、要点过密、没有对齐
- 修复后用户确认："比之前好很多"

**推荐布局（三区块结构）：**

```
┌─────────────────────────────────────┐
│ header: template + plain_text title │
├─────────────────────────────────────┤
│ markdown: 基因银行（表格对齐）        │
├─────────────────────────────────────┤
│ markdown: 当前进度（表格对齐）        │
├─────────────────────────────────────┤
│ markdown: 系统状态（表格对齐）        │
├─────────────────────────────────────┤
│ hr（分隔线）                         │
├─────────────────────────────────────┤
│ action + button: CTA 按钮            │
├─────────────────────────────────────┤
│ note: 状态栏（⏱ 用时 · 指标 · 进度）  │
└─────────────────────────────────────┘
```

**关键规则：**
- `wide_screen_mode: false` — 手机阅读更舒服，字不会太大
- 分隔线 `hr` 尽量少用 — 只在 major sections 之间放一条，不要每行都隔
- **优先用表格对齐**，不用纯 bullet 列表 — 指标/数值两列对齐更易扫视
- 每个 major block 用 `**粗体标题**` 开头，块之间用 `---` 分隔
- 状态行用 emoji（✅ ❌ 🔄 ⏱）让异常一眼认出
- CTA 按钮放 `hr` 之后、`note` 之前
- 底部 `note` 格式：`⏱ {耗时} · {任务名} · {核心指标}`

**反面教材（不要学）：**
- 每行都用 `---` 分隔 → 用户反馈"有点乱"
- 全是 bullet 点没有对齐 → 指标一多就杂乱
- `wide_screen_mode: true` → 手机上字太大，视野窄

## build_news_card 内容格式

```
title = "AI投资学习日报"
summary = ["- 半导体板块放量上涨", "- AI算力资金继续流入", "- 绿电政策持续催化"]
impact = "短线关注半导体和算力方向，绿电偏中长期逻辑。"
source_url = "https://example.com"
```

- `summary` 每条带 `- ` 前缀
- `impact` 是结论性判断
- `source_url` 是来源链接

## 结尾特色

结尾要有特色，不能套"已完成/处理完毕"等通用模板。可选风格：
- 故事感叙述（一两句话点睛）
- 引导互动（提问/投票/讨论）
- 趣味小结（俏皮话收尾）
