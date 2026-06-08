---
name: ai-side-income-research
description: AI副业赚钱方向研究 — 平台侦察、竞品分析、变现路径探索
trigger: 用户问赚钱、副业、AI变现、躺赚、被动收入等
---

# AI 副业赚钱研究

## 用户优先级
> 优先方向：牙科CAD AI助手（面向新手技师/义齿加工厂/CAD培训学员）

## 已侦察平台

### AiToEarn（撸图图）
社交媒体 CPS 分发平台，连接广告主和创作者。
详见：`references/aitoearn-reconnaissance.md`

**赚钱路径：**
1. 创作者接任务（小红书/抖音点赞收藏评论任务）
2. 推荐返佣（6个月循环佣金）
3. AI工具订阅

**侦察状态：** 页面可访问，API 路径未知，需浏览器工具抓 JS 渲染内容。

## 侦察方法论

对陌生平台快速侦察的步骤：

1. **路由发现**：sitemap.xml + robots.txt
2. **页面抓取**：curl / Python requests（绕过 JS 渲染）
3. **关键词提取**：正则提取中文高频词判断业务模式
4. **API 探测**：试探常见端点，观察 JSON 响应格式
5. **JS Bundle 分析**：Next.js 等框架的 API 路径隐藏在 JS 中

## 下一步研究
- [ ] AiToEarn 任务监控通知（定时爬取 → 飞书推送）
- [ ] 牙科CAD AI助手市场调研（竞品、定价、目标客户）
- [ ] 更多变现平台侦察
