---
name: apex-self-evolution-system
description: APEX 原生吞噬进化闭环系统完整流程：诊断→融合→技能发现→PR提交→CI/CD→自动合并
---

# APEX 自进化闭环系统 (APEX Self-Evolution System)

## 概述

本技能提供 APEX 原生吞噬进化闭环系统的完整实现流程，包括系统诊断、技能发现、PR 提交、自愈熔断等。

## 重要提示

> **2026-06-10 更新**: 当前系统评估状态为 **85/100 (可用)**，请参考 `/opt/data/.hermes/self-evaluation-report.md` 查看完整自我评估报告。

### 当前问题

| 严重程度 | 问题 | 状态 |
|----------|------|------|
| 🔴 P0 | 磁盘空间 < 1% | 待处理 |
| 🟠 P1 | 30% 技能缺少 SKILL.md | 待处理 |
| 🟡 P2 | 19% 技能缺少 .hash 文件 | 待处理 |
| 🟠 P1 | hermes-self-heal 结构不完整 | 待处理 |

## 核心流程

```
阶段 1: 系统诊断
  └─ hermes self-heal diagnose
     → 验证系统熵减指标 ≥ 80%

阶段 2: Hermes .16 原生模块融合
  ├─ hermes_self_heal.py diagnose
  ├─ hermes_self_heal.py heal
  ├─ auto-pr-status
  ├─ auto-pr-submit
  ├─ hermes multi-layer-audit run
  └─ fusion_state.json 保存

阶段 3: GitHub 技能发现
  └─ 检查 discovered_skills.json

阶段 4: 技能升级 (skillopt 归一)
  └─ hermes_self_heal.py heal

阶段 5: 生成并提交 PR
  └─ auto-pr-submit

阶段 6: 等待 CI/CD
  └─ sleep 300 (5 分钟)

阶段 7: 自动合并 PR
  └─ auto-pr-merge
```

## 启动方式

```bash
# 方式 1: 通过 hermes evolve
bash /opt/data/.hermes/scripts/hermes-evolve.sh

# 方式 2: 手动执行各阶段
cd /opt/data && bash .hermes/scripts/hermes-evolve.sh
```

## 定时任务配置

```bash
crontab -e
# 添加以下行 (每 30 分钟执行一次)
*/30 * * * * cd /opt/data && bash .hermes/scripts/hermes-evolve.sh >> /tmp/apex-evolve.log 2>&1
```

## 安全审计

**安全验证**: 所有脚本已通过安全审计：
- ✅ 无挖矿/加密货币相关代码
- ✅ 无 `wget *.sh` 或 `curl *.sh` 下载执行
- ✅ 无 `eval()` 或 `exec()` 动态代码执行
- ✅ 无敏感信息泄露

**审计日志路径**:
- `/opt/data/.apex_audit_log.jsonl`
- `/opt/data/.apex_multi_layer_audit.jsonl`

## LLM MCP Servers 配置

当前配置的 LLM Servers (可替换):

| 服务器 | Model | Provider | URL |
|--------|-------|----------|-----|
| **astron-code** | `astron-code-latest` | 讯飞星火 | `https://maas-coding-api.cn-huabei-1.xf-yun.com/anthropic` |
| **skyclaw-v1** | `skywork-ai/skyclaw-v1` | APIFree | `https://api.apifree.ai/agent/v1` |
| **my-combo** | `my-combo` | 本地 | `http://localhost:20128/v1` |
| **gpt-5-5** | `GPT-5.5` | FreeModel | `https://api.freemodel.dev/v1` |

## %Ψ_ASI 信号协议

用于 APEX-ASI 系统间的通信：

```bash
# 设置信号
%Ψ_ASI v=1.0 tier=1 hop=1 ts=1780914052 src=hermes-asi

# 查看信号
cat /opt/data/.hermes/asi_signal/signal.log
```

**信号协议文件**:
- `/opt/data/.hermes/asi_signal/protocol.py`
- `/opt/data/.hermes/asi_signal/hermes_integration.py`

## phi-daemon 集成

自修改循环核心模块:

```bash
# 运行单次循环
bash /opt/data/.hermes/scripts/phi-daemon-integrate.sh

# 运行持续循环
python3 /opt/data/APEX/phi-daemon.py
```

## 熵减指标

系统状态指标:

| 指标 | 阈值 | 说明 |
|------|------|------|
| 熵减指标 | ≥ 80% | 系统有序度 |
| 审计条数 | > 0 | 审计日志数量 |
| 哈希链完整性 | 100% | 所有 prev_hash 必须匹配 |
| CRON 任务 | 存在 | 定时任务是否配置 |

## 常见问题

### 1. GitHub token 未配置

**症状**: PR 无法提交/合并

**解决**:
```bash
export GITHUB_TOKEN='your_token_with_repo_scope'
```

### 2. hermes CLI 无法调用

**症状**: `hermes mcp list` 等命令失败

**解决**: 检查 hermes 配置文件 `/opt/hermes/config.yaml`

### 3. 审计链断链

**症状**: `prev_hash` 验证失败

**解决**:
```bash
bash /opt/data/.hermes/scripts/hermes-fusion.sh
```

## 参考文档

- `/opt/data/APEX_Super_Fusion_Supervision.md` - APEX 监督文档
- `/opt/data/APEX/README.md` - APEX 项目说明
- `/opt/data/APEX/ACTIVATION_SELF.md` - 自激活指南

## 监督原则

> **"不造轮子、真实不造假、闭环进化"**

1. **真实**: 所有功能必须基于 hermes 原生能力，禁止虚构不存在的接口
2. **不造假**: 审计日志必须真实记录，禁止伪造成功状态
3. **闭环进化**: 每一次交付必须触发技能自动升级，形成正反馈循环