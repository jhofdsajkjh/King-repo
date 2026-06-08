# 飞书卡片设计器 & 配色速查

## 卡片设计器（可视化设计）

- **Feishu**：https://open.feishu.cn/tool/cardbuilder
- **Lark**：https://open.larksuite.com/tool/cardbuilder

可直接在设计器里拖拽组件，导出 JSON 用于代码中。

## 配色模板速查

| template 值 | 颜色 | 适用场景 |
|------------|------|---------|
| `blue` | 蓝 | 通用信息、进度更新 |
| `green` | 绿 | 成功、完成、正向 |
| `red` | 红 | 错误、紧急告警 |
| `orange` | 橙 | 警告、需人工处理 |
| `purple` | 紫 | 通用/默认（Hermes 标准色） |
| `indigo` | 靛 | 技术类、工程类 |
| `turquoise` | 青 | 增长、营销 |
| `yellow` | 黄 | 高亮、提示 |
| `grey` | 灰 | 低优先级、中性 |
| `wathet` | 浅蓝 | 简洁默认 |

## 常用元素组合

### Hermes 标准卡片（底部状态栏）
```json
{
  "header": {"title": {"tag": "plain_text", "content": "✍️ 已完成 | 标题"}, "template": "purple"},
  "elements": [
    {"tag": "markdown", "content": "**内容**\n\n正文..."},
    {"tag": "hr"},
    {"tag": "column_set", "flex_mode": "bisect", "columns": [
      {"tag": "column", "width": "weighted", "weight": 1, "elements": [{"tag": "markdown", "content": "**状态**\n✅ 正常"}]},
      {"tag": "column", "width": "weighted", "weight": 1, "elements": [{"tag": "markdown", "content": "**待处理**\n⏳ ..."}]}
    ]},
    {"tag": "note", "elements": [{"tag": "plain_text", "content": "⏱ 1m 19s · LongCat-2.0-Preview · 调用API 6 次 · 上下文 56.5k/256.0k [██░░░░░░░░] 22.1%"}]}
  ]
}
```

### 双栏指标卡片
```json
{
  "tag": "column_set",
  "flex_mode": "bisect",
  "columns": [
    {"tag": "column", "width": "weighted", "weight": 1,
     "elements": [{"tag": "markdown", "content": "**指标A**\n\n值1\n值2"}]},
    {"tag": "column", "width": "weighted", "weight": 1,
     "elements": [{"tag": "markdown", "content": "**指标B**\n\n值1\n值2"}]}
  ]
}
```

### 操作按钮行
```json
{
  "tag": "action",
  "actions": [
    {"tag": "button", "text": {"tag": "plain_text", "content": "📋 查看详情"}, "type": "primary", "url": "https://..."},
    {"tag": "button", "text": {"tag": "plain_text", "content": "✅ 已知悉"}, "type": "default"}
  ]
}
```
