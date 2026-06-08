# AiToEarn（撸图图）平台侦察报告
时间：2026-05-20 | 用途：AI副业赚钱研究

## 平台基本信息
- 网址：https://aitoearn.cn/zh-CN?role=creator
- 标题：AiToEarn - 付费推广任务 - 用社交媒体赚钱
- 架构：Next.js SSR + 浏览器插件自动化发布
- 后端：Istio + Cloudflare

## 赚钱路径

### 路径一：创作者接任务（流量变现）
- 小红书任务推广（点赞收藏评论、笔记推广、话题打卡）
- 抖音任务推广
- 即梦推广任务
- 计费：固定价格 / 千次互动 / 封顶金额
- 部分有粉丝限制，部分"不限"

### 路径二：推荐返佣
- 每推荐一个付费用户，6个月内持续返佣
- 专属推广链接 + 实时追踪收益

### 路径三：AI工具订阅
- 视频生成、图片创作工具订阅

## 侦察命令
```bash
# 路由发现
curl -sL "https://aitoearn.cn/sitemap-0.xml"
curl -sL "https://aitoearn.cn/task-sitemap.xml"

# 关键页面
curl -sL "https://aitoearn.cn/zh-CN/affiliates"   # 推荐计划
curl -sL "https://aitoearn.cn/zh-CN/pricing"       # 定价
curl -sL "https://aitoearn.cn/zh-CN/websit/plugin-guide"  # 浏览器插件

# 任务详情
curl -sL "https://aitoearn.cn/zh-CN/task/<task-id>"
```

## API 状态
- Next.js 客户端渲染，API 路径隐藏在 JS bundle 中
- 所有测试路径均 404
- JSON 格式：`{"data":{}, "code":404, "message":"...", "timestamp":...}`

## Next Step
- [ ] 任务数据爬取（需浏览器工具或 JS bundle 逆向）
- [ ] 任务监控通知（定时爬取 → 飞书推送）
