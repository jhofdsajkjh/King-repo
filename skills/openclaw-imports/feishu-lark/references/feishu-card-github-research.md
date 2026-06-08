# 飞书卡片优质案例参考 (GitHub 调研)

本文件记录通过 GitHub API 调研筛选出的优质飞书卡片实现案例，供后续优化参考。

## 官方 SDK 与规范

| 仓库 | Stars | 类型 | 链接 |
|------|-------|------|------|
| larksuite/oapi-sdk-python | 官方 | Python SDK + FeishuChannel 封装 | https://github.com/larksuite/oapi-sdk-python |
| larksuite/cli | 官方 | MIT 协议 CLI，2500+ API，19 个 AI Agent Skills | https://github.com/larksuite/cli |

**FeishuChannel 模式优势：**
- 封装了事件监听、消息标准化、安全策略、出站发送、媒体上传下载、卡片交互、流式回复
- 一行 `FeishuChannel` 入口，支持 `on("message")` 事件注册
- 支持流式卡片和按钮交互回调

**当前 Hook 方案 vs FeishuChannel：**
- Hook 方案：原生 `lark-oapi` SDK，由 Hermes Gateway `emit_collect` 驱动，无额外进程依赖
- FeishuChannel：更高级封装，支持流式卡片，但需额外的事件循环管理

## 社区实战案例

| 仓库 | Stars | 类型 | 链接 |
|------|-------|------|------|
| AlexAnys/openclaw-feishu | 691 | 飞书 × OpenClaw 配置指南，含 Webhook 机器人卡片、API 配额排查 | https://github.com/AlexAnys/openclaw-feishu |
| op7418/Claude-to-IM-skill | 2584 | Claude Code/Bot 桥接飞书，支持流式预览 + 交互按钮 | https://github.com/op7418/Claude-to-IM-skill |
| agenmod/immortal-skill | 765 | 数字永生框架，支持飞书等 12+ 平台消息推送卡片 | https://github.com/agenmod/immortal-skill |
| y49/tlive | 199 | Terminal Live — 监控 AI 编程 Agent（Claude/Codex）+ 飞书收发 | https://github.com/y49/tlive |
| XUJiahua/alertmanager-webhook-feishu | 59 | Prometheus Alertmanager 飞书集成 | https://github.com/XUJiahua/alertmanager-webhook-feishu |

## 卡片 JSON 设计要点（从案例提取）

1. **Header 配色语义：**
   - `green` — 投资/自动化推送（默认）
   - `red` — 风险提醒/失败
   - `blue` — 通用信息
   - `purple` — AI/科技感
   - `orange` — 提醒

2. **标准结构（最小可用）：**
   ```json
   {
     "config": {"wide_screen_mode": true},
     "header": {"title": {"tag": "plain_text", "content": "标题"}, "template": "blue"},
     "elements": [
       {"tag": "markdown", "content": "Markdown 内容"},
       {"tag": "hr"},
       {"tag": "note", "elements": [{"tag": "plain_text", "content": "底部状态栏"}]}
     ]
   }
   ```

3. **状态栏格式（与终端一致）：**
   ```
   🤖 {模型名}  |  ⏱ {耗时}s  |  🔄 {调用次数} calls  |  🎫 {Token数} tokens
   ```

## 飞书官方资源

- [Card Builder 可视化设计器](https://open.feishu.cn/tool/cardbuilder)
- [Card List 模板库](https://open.feishu.cn/document/home/card-list)
- [Handle Card Callbacks](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/server-side-sdk/python--sdk/handle-callbacks)