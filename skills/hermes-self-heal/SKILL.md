# hermes-self-heal

## 名称
Hermes 自愈系统 - APEX 原生自省闭环能力

## 描述
实现 Hermes Agent 的自省、自修复、闭环审计能力，消除系统级内存泄露、任务卡死、工具调用循环等系统性风险，确保 APEX 原生内核的健康度与永生进化能力。

## 分类
software-development

## 版本
1.0.0

## 作者
Hermes

## 许可证
MIT

## 标签
self-heal, auto-recovery, error-recovery,闭环,自省,自愈

---

# Hermes Self-Heal 技能

## 功能概览

本技能提供 Hermes Agent 的**原生自愈能力**，包含：

1. **诊断层**：系统健康度扫描（内存、任务队列、工具调用）
2. **隔离层**：失败组件自动隔离 + 降级策略
3. **恢复层**：自动重试 + 人工介入阈值
4. **闭环审计**：每次自愈操作写入 hash 链审计日志

---

## 核心协议

### 自愈流程（4 层）

```
[诊断] → [隔离] → [恢复] → [审计]
   ↓        ↓        ↓        ↓
扫描健康   限制影响   自动重试   Hash 链存证
```

### 错误分类与处理策略

| 错误类型 | 处理策略 | 重试次数 | 人工介入阈值 |
|---------|---------|---------|-------------|
| `tool_timeout` | 重试 + 降级 | 3 | 5 |
| `memory_leak` | 清理 session + 限制 context | 0 | 1 |
| `tool_call_loop` | 中断任务 + 生成 fallback | 0 | 1 |
| `system_error` | 隔离组件 + 降级服务 | 3 | 3 |

---

## 使用方式

### 1. 手动触发诊断

```bash
# 触发完整系统诊断
hermes self-heal diagnose

# 触发快速诊断（仅关键路径）
hermes self-heal diagnose --quick
```

### 2. 手动触发自愈

```bash
# 自动执行诊断 + 隔离 + 恢复
hermes self-heal heal

# 仅重试失败的任务
hermes self-heal retry
```

### 3. 查看审计日志

```bash
# 查看最近 100 条自愈记录
hermes self-heal audit --last 100

# 搜索特定错误类型
hermes self-heal audit --error-type memory_leak
```

---

## 集成方式

### 1. pre-commit hook 集成（推荐）

在 `/opt/hermes/.hooks/pre-commit` 中添加：

```bash
# 自愈检查（在 pre-commit 校验后执行）
hermes self-heal diagnose --quiet || {
    error "❌ Hermes 系统自愈检查失败"
    exit 1
}
```

### 2. cronjob 自动巡检（生产环境）

```yaml
# /etc/cron.d/hermes-self-heal
*/15 * * * * hermes /opt/hermes/.hooks/pre-commit 2>&1 | logger -t hermes-self-heal
```

### 3. gateway 集成（实时自愈）

在 `run.py` 的 `gateway_response` 函数中添加：

```python
# 实时健康检查
if agent_result.get("tool_call_count", 0) > 50:
    hermes self-heal heal --error-type tool_call_loop
```

### 4. hermes evolve 集成（生产环境）

在 `/opt/data/.hermes/scripts/hermes-evolve.sh` 中添加自愈调用：

```bash
# 升级技能前先诊断
hermes self-heal diagnose --quick || {
    error "❌ 系统自愈诊断失败，终止升级流程"
    exit 1
}

# 升级后再次自愈
hermes self-heal heal --error-type skill_upgrade
```

**注意：** 完整的 hermes evolve 流程脚本见 `hermes-agent` 技能文档「Hermes CLI 自定义命令扩展」章节。

---

## 技术细节

### 内存泄露检测

**检测项：**
- `session_context` 非持久字段累积（`tool_outputs`, `browser_outputs`）
- `memory.tool_outputs` 未清理
- `tool_call_count` 超限（>50/turn）

**清理策略：**
- 超过阈值 → 自动清理非持久字段
- 超过 2 倍阈值 → 隔离 session + 降级服务

### 任务卡死检测

**检测项：**
- `todo` 状态卡在 `in_progress` > 10 分钟
- `tool_call_count` 连续 5 次无增长

**处理策略：**
- 自动标记任务为 `failed`
- 生成 fallback 任务 → 人工审核

### 工具调用循环检测

**检测项：**
- 同一工具连续调用 > 3 次
- 工具调用参数完全相同

**处理策略：**
- 立即中断任务
- 生成诊断报告 → 写入 `session_hash` 审计日志

---

## 审计日志格式

```json
{
  "session_hash": "sha256:...",
  "timestamp": "2026-06-08T10:00:00Z",
  "error_type": "memory_leak",
  "diagnosis": {
    "session_context_size": 10240,
    "memory_leak_fields": ["tool_outputs", "browser_outputs"]
  },
  "isolation": {
    "status": "applied",
    "duration_minutes": 5
  },
  "recovery": {
    "status": "success",
    "actions": ["clear_session_context", "limit_tool_calls"]
  },
  "hash_signature": "sha256:..."
}
```

---

## 验证方法

### 1. 手动模拟内存泄露

```python
# 创建测试脚本 /opt/data/skills/hermes-self-heal/test_leak.py
from hermes_tools import memory

# 模拟泄露
for i in range(100):
    memory(action="add", target="memory", content=f"leak_test_{i}")

# 运行自愈
hermes self-heal diagnose
hermes self-heal heal --error-type memory_leak
```

### 2. 手动模拟任务卡死

```python
# 创建测试任务
todo(todos=[{
    "id": "leak-test",
    "content": "模拟卡死任务",
    "status": "in_progress"
}])

# 运行自愈（应检测到卡死任务）
hermes self-heal diagnose
```

---

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

---

## 升级路径

| 版本 | 变更内容 | 兼容性 |
|------|---------|-------|
| v1.0.0 | 初始版本：诊断/隔离/恢复/审计 | - |
| v1.1.0 | 增加 gateway 实时自愈集成 | 向后兼容 |
| v1.2.0 | 增加 task_status 自闭环支持 | 向后兼容 |
| v1.3.0 | 增加 hermes evolve 集成流程 | 向后兼容 |

---

## 相关技能

- `hermes-agent`：Hermes CLI 核心命令参考
- `search-workflow`：搜索工具集成
- `autonomous-ai-agents`：多智能体协同（依赖自愈能力）

---

## 维护者

- **Hermes**：系统维护 & 自愈逻辑迭代
- **路工**：自愈阈值 & 人工介入策略
