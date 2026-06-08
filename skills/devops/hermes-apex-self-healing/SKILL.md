---
name: hermes-apex-self-healing
category: devops
version: "2026.6.8"
description: APEX 原生自愈闭环系统：诊断、隔离、恢复、审计四层架构
tags:
  - self-heal
  - auto-recovery
  - error-recovery
  - loop-auditing
  - hash-chain
  - entropy-reduction
---

# Hermes APEX 自愈闭环系统

使用本技能来理解或配置 APEX 原生自愈系统，确保 Hermes Agent 的自省、自修复、闭环审计能力。

## 核心架构（四层）

```
[诊断层] → [隔离层] → [恢复层] → [审计层]
   ↓         ↓          ↓          ↓
扫描健康  限制影响  自动重试  Hash链存证
```

## 诊断层（diagnose）

### 检测项

| 检测项 | 触发阈值 | 处理动作 |
|--------|---------|---------|
| session_context 非持久字段累积 | >10KB | limit_tool_calls + clear_session_context |
| tool_call_count | >50/turn | limit_tool_calls + truncate_context |
| context_usage (input + output) | >15000 tokens | truncate_context |

### 使用命令

```bash
# 完整诊断
hermes self-heal diagnose

# 快速诊断（仅关键路径）
hermes self-heal diagnose --quick

# 导出 JSON 报告
hermes self-heal diagnose --output json
```

## 隔离层（isolate）

### 隔离策略

| 错误类型 | 隔离时长 | 限制措施 |
|---------|---------|---------|
| memory_leak | 5 分钟 | no_new_tools, limited_context |
| tool_call_loop | 永久 | max_tool_calls=10 |
| system_error | 10 分钟 | no_new_tools, limited_context |

## 恢复层（recover）

### 恢复动作

| 动作 | 说明 |
|------|------|
| clear_session_context | 清理非持久字段（tool_outputs, browser_outputs） |
| limit_tool_calls | 设置 tool_call_count limit = 50 |
| truncate_context | 截断 context_usage（保留最近 10000 tokens） |

### 使用命令

```bash
# 自动执行诊断 + 隔离 + 恢复
hermes self-heal heal

# 仅重试失败的任务
hermes self-heal retry
```

## 审计层（audit）

### 审计日志

**路径：** `/opt/data/.apex_audit_log.jsonl`

**日志格式：**
```json
{
  "event_type": "self_heal_v2",
  "diagnosis": {
    "status": "healthy/critical",
    "leaked_fields": ["tool_outputs", "browser_outputs"],
    "total_size_kb": 15.2
  },
  "isolation": {
    "status": "isolated",
    "duration_minutes": 5,
    "restrictions": ["no_new_tools", "limited_context"]
  },
  "recovery": {
    "status": "success",
    "actions": ["limit_tool_calls", "clear_session_context"],
    "cleared_fields": ["tool_outputs", "browser_outputs", ...]
  },
  "session_hash": "sha256:...",
  "hash_signature": "sha256:...",
  "timestamp": "2026-06-08T10:00:00Z"
}
```

### 使用命令

```bash
# 查看最近 100 条自愈记录
hermes self-heal audit --last 100

# 搜索特定错误类型
hermes self-heal audit --error-type memory_leak

# 按时间范围搜索
hermes self-heal audit --since "2026-06-01"
```

## 错误分类与处理策略

| 错误类型 | 处理策略 | 重试次数 | 人工介入阈值 |
|---------|---------|---------|-------------|
| tool_timeout | 重试 + 降级 | 3 | 5 |
| memory_leak | 清理 session + 限制 context | 0 | 1 |
| tool_call_loop | 中断任务 + 生成 fallback | 0 | 1 |
| system_error | 隔离组件 + 降级服务 | 3 | 3 |

## 相关技能

- `system-updates-under-constraints`：系统更新约束处理
- `kanban-worker`：任务分解与工作流
- `self-evolution-cycle`：自进化循环（依赖自愈能力）

## 故障排查

### Q: 自愈失败，如何手动介入？

**A:** 查看诊断报告：
```bash
hermes self-heal diagnose --output json
```

定位失败组件 → 手动清理 → 重新触发自愈：
```bash
# 手动清理 session_context
rm -rf ~/.hermes/cache/session_*

# 重新触发自愈
hermes self-heal heal
```

### Q: 自愈频率过高，如何调整阈值？

**A:** 编辑配置：
```bash
hermes config set self_heal.memory_leak_threshold=2048
hermes config set self_heal.tool_call_loop_threshold=3
```

## 更新日志

| 版本 | 变更内容 |
|------|---------|
| v2.0 (2026-06-08) | 增加 context_usage 检测、session_hash 审计、task_status 自闭环 |
| v1.0 (2026-06-07) | 初始版本：诊断/隔离/恢复/审计基础框架 |
