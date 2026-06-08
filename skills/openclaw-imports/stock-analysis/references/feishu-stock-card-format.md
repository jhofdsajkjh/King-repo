# Feishu 股票卡片标准格式 (Validated 2026-05-21)

经过实测验证的飞书卡片格式，用于推送 A股个股分析。

## 验证通过的结构

```python
{
  "config": {"wide_screen_mode": True},
  "header": {
    "template": "green",   # green=投资/自动化推送, red=风险提醒, purple=AI科技感
    "title": {"tag": "plain_text", "content": "📊 今日股讯 | 2026-05-20"}
  },
  "elements": [
    {"tag": "markdown", "content": "内容（支持 ## 标题、**加粗**、- 列表、> 引用等）"},
    {"tag": "hr"},
    {
      "tag": "action",
      "actions": [
        {"tag": "button", "text": {"tag": "plain_text", "content": "查看详情"}, "type": "primary", "url": "https://..."}
      ]
    },
    {"tag": "note", "elements": [{"tag": "plain_text", "content": "🐯 由 小马 整理 | Wind 实时行情"}]}
  ]
}
# payload: {"msg_type": "interactive", "card": card}
```

## 配色选择

| 场景 | template |
|------|----------|
| 投资/自动化推送（默认） | green |
| 风险提醒 | red |
| 通用信息 | blue |
| 提醒 | orange |
| AI 科技感 | purple |
| 浅蓝 | wathet |
| 青色 | turquoise |
| 普通通知 | grey |

## 手机排版要点（用户明确要求）

- 每只股票用 `---` 分隔，不用表格（手机屏幕窄）
- 每股一行：名称代码 + 状态 emoji + 价格 + 涨跌幅
- 关键数据放前面（量比/PE/位置）
- 结论用 emoji + 简短词语，不用长句
- 桌面端长报告格式仅用于非推送场景

## 飞书卡片示例（实测有效）

```markdown
📈 创业板个股追踪

今天盘面挺有意思，4只创业板股票涨跌各半。

---

**【强势股】300429 强力新材**
• 现价 **16.30** | 涨幅 **+4.55%** ↑
• 成交额 **11.13亿**
• 低开高走，振幅达 8.7%
• 结论：低位反弹，量能配合

---

⚠️ **基本面数据暂时缺失**
PE/PB/市值等指标 Wind 接口暂不可用

---

📝 **今日小结**：创业板小票活跃，光伏和化工材料方向有资金关注。

🐯 由 小马 整理 | Wind 实时行情
```

## 注意

- `tag: note` 的 `elements` 必须是 `{"tag": "plain_text"}`，不能用 `lark_md`
- 展示型按钮（`type: primary` + `url`）无需后端回调，直接跳转链接
- Header 颜色在 template 字段设置，不是 background 字段
