# note 元素限制与 div 替代方案

## 问题发现（2026-05-30）

用户反馈飞书卡片尾部状态栏显示不正常。诊断发现：

- 卡片使用了 `note` 元素承载底部状态信息
- `note` 元素中嵌入了 `lark_md` 文本（含加粗 `**bold**`、进度条 `████` 等）
- 实际渲染效果：加粗丢失、进度条方块字符异常、工具名被吞

## 根因

`note` 元素**只能包含 `plain_text` 子元素**，不支持：
- `lark_md` 或 `markdown` 格式
- 任何富文本（加粗、斜体、链接）
- 特殊字符（如 `████` 方块）可能渲染异常
- 背景色属性

## 修复方案

用 `div` + `background_style` 替代 `note`：

```json
{
  "tag": "div",
  "background_style": "green",
  "text": {
    "tag": "lark_md",
    "content": "**⏱ 0.2s** · **🤖 SkyClaw v1** · **📡 1次** · **📊 80%**"
  },
  "margin": {"top": "8px", "bottom": "0"}
}
```

### background_style 支持值
`blue`, `green`, `yellow`, `red`, `gray` 等

### 使用建议
- 需要彩色背景 + 格式化内容 → 用 `div` + `background_style` + `lark_md`
- 只需要纯文本脚注（无背景色）→ `note` 元素仍然适用
- `div` 内必须用 `tag: "lark_md"`，不能用 `tag: "markdown"`（后者是独立元素）

## 相关坑点
- 见 SKILL.md 坑点 8（note 限制）和坑点 5（div + lark_md + background 渲染问题）
- App Bot API 中 `div` + `background` 可以工作（2026-05-30 实测通过）
- Webhook 模式下 `div` + `background` 可能报 ErrCode 200621，此时降级为 `note`
