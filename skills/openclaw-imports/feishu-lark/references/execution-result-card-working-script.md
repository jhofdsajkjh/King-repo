# 执行结果卡片 — 已验证可工作的发送脚本

2026-05-30 实测通过。修复了以下问题：
1. `note` 元素不支持富文本 → 改用 `div` + `background_style`
2. `receive_id` 放在 URL 查询参数 → 改为 POST body
3. Token 在 `result['data']` 下 → 实际在顶层 `result['tenant_access_token']`
4. App Secret 在 config 中被截断 → 从 .env 文件读取

## 完整可运行脚本

```python
import re, json, urllib.request, urllib.error

env_path = r"C:\Users\Administrator\AppData\Local\hermes\.env"
with open(env_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 从 .env 读取完整 App Secret（config.yaml 中会被截断）
for line in content.split('\n'):
    if 'FEISHU_APP_SECRET' in line and not line.lstrip().startswith('#'):
        secret = line.split('=', 1)[1].strip()
        break

# 获取 tenant_access_token
payload = {"app_id": "cli_aa82fa272538dcc8", "app_secret": secret}
data = json.dumps(payload).encode()
req = urllib.request.Request(
    "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
    data=data,
    headers={"Content-Type": "application/json"}
)
resp = urllib.request.urlopen(req, timeout=10)
result = json.loads(resp.read().decode())
access_token = result['tenant_access_token']  # 顶层，不在 data 下

# 构建卡片
card_content = {
    "config": {"wide_screen_mode": True},
    "header": {
        "title": {"tag": "plain_text", "content": "🤖 已完成｜测试任务"},
        "template": "turquoise"
    },
    "elements": [
        {"tag": "markdown", "content": "这是一条测试卡片消息。"},
        {"tag": "markdown", "content": "```python\nprint('Hello, Feishu!')\n```"},
        {"tag": "hr"},
        {
            "tag": "div",
            "text": {"tag": "lark_md", "content": "**🔧 工具摘要**\n✅ `send_message` — 飞书消息发送\n✅ `terminal` — 终端执行"},
            "background_style": "blue",
            "margin": {"top": "8px", "bottom": "8px"}
        },
        {
            "tag": "div",
            "text": {"tag": "lark_md", "content": "⏱ 0.1s · 🤖 SkyClaw v1 · 📡 1次 · 📊 80%"},
            "background_style": "green",
            "margin": {"top": "0", "bottom": "0"}
        }
    ]
}

# 发送 — receive_id 在 POST body 中
message = {
    "receive_id": "oc_a9f3e61c8afd6218eb597a1e9f542cc7",
    "msg_type": "interactive",
    "content": json.dumps(card_content)
}

card_data = json.dumps(message).encode()
card_req = urllib.request.Request(
    "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id",
    data=card_data,
    headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
)
card_resp = urllib.request.urlopen(card_req, timeout=10)
card_result = json.loads(card_resp.read().decode())
print(f"Card sent! Code: {card_result.get('code')}")
print(f"Message ID: {card_result.get('data', {}).get('message_id', 'N/A')}")
```

## 关键修复点

### 1. div + background_style 替代 note

```json
// ❌ note 不支持富文本、无背景色
{"tag": "note", "elements": [{"tag": "plain_text", "content": "⏱ 0.1s · ..."}]}

// ✅ div + background_style 支持 lark_md + 彩色背景
{
  "tag": "div",
  "background_style": "green",
  "text": {"tag": "lark_md", "content": "⏱ 0.1s · 🤖 SkyClaw v1 · 📡 1次 · 📊 80%"},
  "margin": {"top": "0", "bottom": "0"}
}
```

可用背景色：`blue`, `green`, `red`, `orange`, `yellow`, `purple`, `grey`, `wathet`, `turquoise`

### 2. receive_id 必须放 POST body

```python
# ❌ 错误：放在 URL 查询参数
url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id&receive_id=oc_xxx"

# ✅ 正确：放在 POST body
message = {
    "receive_id": "oc_xxx",
    "msg_type": "interactive",
    "content": json.dumps(card_content)
}
url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id"
```

### 3. Token 在响应顶层

```python
# ❌ 错误
access_token = result['data']['tenant_access_token']

# ✅ 正确
access_token = result['tenant_access_token']
```

## 渲染效果

- 标题栏：青绿色（turquoise）
- 内容区：Markdown 文本 + 代码块
- 工具摘要：蓝色背景 + lark_md 格式化
- 底部状态：绿色背景 + 一行紧凑状态信息
