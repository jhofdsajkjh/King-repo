# 执行结果卡片调试记录（2026-05-30）

## 用户目标
还原模板图片效果：深色主题风格、青绿色标题栏、蓝色工具摘要行、绿色底部状态条。

## 关键发现

### 1. `send_message` 工具不支持 interactive card
- `send_message(message="{json}", target="feishu")` 只发纯文本
- JSON 会被当作普通字符串发送到飞书，不会渲染为卡片
- **必须**用飞书 Open API（curl 或 Python urllib/requests）直接调用

### 2. App Bot API 发卡片的标准流程
```bash
# 1. 获取 token
curl -s https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \
  -H "Content-Type: application/json" \
  -d '{"app_id":"$FEISHU_APP_ID","app_secret":"$FEISHU_APP_SECRET"}'

# 2. 把完整请求体写到文件（避免转义问题）
# 文件内容 = {"receive_id": "...", "msg_type": "interactive", "content": "<双重JSON编码的card>"}

# 3. 用 curl -d @file.json 发送
curl -s "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d @/path/to/request.json
```

### 3. content 字段必须双重 JSON 编码
```python
import json
card = {"header": {...}, "elements": [...]}
request_body = {
    "receive_id": "oc_xxx",
    "msg_type": "interactive",
    "content": json.dumps(card)  # ← 必须是字符串化的 JSON
}
```

### 4. 渲染问题汇总

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| code 块内容为空 | content 双重编码出错，text 字段被吞 | 验证双重编码；或用 markdown 内嵌代码块 |
| `**加粗**` 不生效 | 飞书卡片 markdown 对加粗支持有限 | 用 emoji 前缀替代，不依赖加粗 |
| div 背景色块内容为空 | `div.text` 缺少 `content` 字段（误用 `text`） | 确保 `{"tag": "lark_md", "content": "..."}` |
| 工具名被吞 | `lark_md` 内 `` `code` `` 语法解析问题 | 简化 lark_md 内容，减少内联代码标记 |

### 5. 用户确认的格式约定
- 标题栏：`turquoise`（青绿色）— 2026-05-30 用户说 "Always"
- 工具摘要行：`background: "blue"`
- 底部状态条：`background: "green"`
- 格式：标题 → 状态文本 → 代码块 → 解释 → 分隔线 → 工具摘要 → 分隔线 → 状态条
