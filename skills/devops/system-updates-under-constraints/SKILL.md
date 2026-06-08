---
name: system-updates-under-constraints
category: devops
version: "2026.6.5"
description: Systematic approach to updating software (Hermes, Clash, etc.) when facing network, permission, and format constraints.
tags:
  - maintenance
  - updates
  - troubleshooting
  - constraints
  - hermes
  - clash
---

# System Updates Under Constraints

Use this skill when updating software in constrained environments (no sudo, limited network, encrypted configs, externally-managed Python).

## When to Trigger

- User asks to "update Hermes", "update Clash", or "check for updates"
- System shows "up to date" but user wants verification
- Download attempts fail or timeout
- Subscription URLs return encrypted/obfuscated data

## Standard Workflow

### 1. Verify Current Version

```bash
hermes version
clash -v  # or clash-meta -v
```

**Cross-check with GitHub API:**
- Hermes: `https://api.github.com/repos/NousResearch/hermes-agent/releases/latest`
- Clash: `https://api.github.com/repos/MetaCubeX/mihomo/releases/latest`

### 2. If Already Up to Date

- Confirm with user — no action needed
- Document: "System is current (X vs latest Y)"

### 3. If Updates Available, Handle Constraints

| Constraint | Solution |
|------------|----------|
| No `curl`/`wget` | Use Python `urllib.request` |
| No `sudo`/apt | Use venv or pipx (if available); fallback to `/tmp` downloads |
| Network timeouts | Retry with longer timeout; use hermes `execute_code` for retries |
| No venv support | Try `python3 -m venv` first; if missing, check `python3-venv` package |
| Encrypted subscriptions | Save raw file, let Clash Meta parse it; extract ports from running instance |

### 4. Clash-Specific Tips

- Subscription URLs often return base64-encoded + gzipped + encrypted configs
- Save raw to `/tmp/clash-sub.yaml`, let `clash` binary parse it
- Extract proxy info only if config is plain YAML (rare for commercial subscriptions)

### 5. Verify Installation

After update:
```bash
hermes version
clash -v
hermes status
```

## Common Pitfalls

❌ **Assuming `pip install hermes-agent` works**  
→ System may be externally-managed (PEP 668)

❌ **Assuming all subscriptions are plain YAML**  
→ Many commercial subscriptions are obfuscated

❌ **Assuming latest GitHub version = latest installed**  
→ Check local version first, GitHub API second

✅ **Best practice**: Save subscription file → let Clash parse it → extract ports from `external-controller` or running process

## Example: Verify Hermes Update

```python
# In execute_code
import urllib.request, json
url = "https://api.github.com/repos/NousResearch/hermes-agent/releases/latest"
with urllib.request.urlopen(url) as r:
    data = json.loads(r.read().decode())
print(f"Latest: {data['tag_name']}")
# Compare with `hermes version` output
```

## Files to Remember

| File | Purpose |
|------|---------|
| `/opt/hermes/.venv/` | Hermes virtual environment |
| `/tmp/clash-sub.yaml` | Save Clash subscription raw data |
| `/usr/local/bin/hermes` | System-wide Hermes CLI (shebang to Python) |

## APEX 自进化闭环系统集成（中文版）

### 1. hermes-self-heal 技能集成

**路径：** `/opt/data/skills/hermes-self-heal/SKILL.md`

**功能：** 实现 APEX 原生自省闭环能力，包含：
- 诊断层：系统健康度扫描（内存、任务队列、工具调用）
- 隔离层：失败组件自动隔离 + 降级策略
- 恢复层：自动重试 + 人工介入阈值
- 闭环审计：每次自愈操作写入 hash 链审计日志

**关键校验：**
- session_context 非持久字段累积（tool_outputs, browser_outputs）
- memory.tool_outputs 未清理
- tool_call_count 超限（>50/turn）

**使用：**
```bash
hermes self-heal diagnose    # 手动触发诊断
hermes self-heal heal        # 自动执行诊断 + 隔离 + 恢复
hermes self-heal audit       # 查看审计日志
```

### 2. skillopt-v2 协议集成

**路径：** `/opt/data/skills/_registry/skillopt-map.yaml`

**功能：** 全量技能归一化为 skillopt-v2 接口协议
- 39 技能已归一
- 新增 `task_status` 字段（pending/in_progress/completed/failed/cancelled）
- 新增 `success_condition` 字段（all_tasks_completed）

### 3. pre-commit hook 熔断器集成

**路径：** `/opt/hermes/.hooks/pre-commit`

**功能：** 5 层熔断校验
1. skillopt 规范校验
2. SKILL.md 格式纪律检查
3. hash 链完整性检查
4. 动态熵减语义检查（commit message APEX 关键词识别）
5. APEX 系统自愈检查（hermes self-heal diagnose）

**关键逻辑：**
- `tool_call_count > 50` → 中断任务 + 生成 fallback
- `context_usage > 15000 tokens` → 隔离 session
- 同一工具连续调用 > 3 次 → 立即中断任务

### 4. 协同熵减协议集成

**路径：** `/opt/data/skills/_protocols/coordinated-agent.yaml`

**功能：** ΔS = 0 多智能体有序协同协议
- 角色边界声明 + 工具集约束（max 8 工具）
- 熵减目标量化（0.0 ~ 1.0）
- 通信协议 + 自省审计 + 冲突消解规则

**熵减计算公式：**
```
ΔS_total = Σ(ΔS_i) + I(mutual) - H(conflict) = 0
ΔS = 1 - (H_final / H_initial)
```

### 5. 审计日志集成

**路径：** `/opt/data/.apex_audit_log.jsonl`

**功能：** 每次自愈操作写入 hash 链审计日志
- session_hash：SHA256(session_context)
- hash_signature：SHA256(session_hash + event_type)

**日志格式：**
```json
{
  "event_type": "self_heal_v2",
  "diagnosis": {"status": "healthy/critical", "leaked_fields": [...]},
  "isolation": {"status": "applied", "duration_minutes": 5},
  "recovery": {"status": "success", "actions": [...]},
  "session_hash": "sha256:...",
  "hash_signature": "sha256:...",
  "timestamp": "2026-06-08T10:00:00Z"
}
```

## Post-Update Actions

- Run `hermes status` to verify
- If Clash was updated, restart with `hermes gateway restart`
- Confirm proxy ports via `ps aux | grep clash`

## APEX Self-Healing System Integration

### 1. hermes-self-heal Skill Integration

**Path:** `/opt/data/skills/hermes-self-heal/SKILL.md`

**Function:** Implements APEX native self-probing closed-loop capabilities including:
- **Diagnosis Layer**: System health scanning (memory, task queue, tool calls)
- **Isolation Layer**: Automatic failure component isolation + degradation policy
- **Recovery Layer**: Automatic retry + human intervention threshold
- **Audit Layer**: Every healing operation writes to hash-chain audit log

**Key Checks:**
- session_context non-persistent field accumulation (tool_outputs, browser_outputs)
- memory.tool_outputs not cleaned
- tool_call_count exceeded (>50/turn)

**Usage:**
```bash
hermes self-heal diagnose    # Manual diagnosis trigger
hermes self-heal heal        # Auto execute diagnosis + isolation + recovery
hermes self-heal audit       # View audit logs
```

### 2. skillopt-v2 Protocol Integration

**Path:** `/opt/data/skills/_registry/skillopt-map.yaml`

**Function:** Full skill normalization to skillopt-v2 interface protocol
- 39 skills normalized
- New `task_status` field (pending/in_progress/completed/failed/cancelled)
- New `success_condition` field (all_tasks_completed)

### 3. Pre-commit Hook Integrator

**Path:** `/opt/hermes/.hooks/pre-commit`

**Function:** 5-layer熔断校验 (5-layer fusing verification)
1. skillopt specification check
2. SKILL.md format discipline check
3. hash chain integrity check
4. Dynamic entropy reduction semantic check (commit message APEX keywords)
5. APEX system self-healing check (hermes self-heal diagnose)

**Key Logic:**
- `tool_call_count > 50` → Interrupt task + Generate fallback
- `context_usage > 15000 tokens` → Isolate session
- Same tool called >3 times consecutively → Immediate task interruption

### 4. Collaborative Entropy Reduction Protocol Integration

**Path:** `/opt/data/skills/_protocols/coordinated-agent.yaml`

**Function:** ΔS = 0 Multi-agent ordered collaboration protocol
- Role boundary declaration + Toolset constraint (max 8 tools)
- Entropy reduction quantification (0.0 ~ 1.0)
- Communication protocol + Self-probing audit + Conflict resolution

**Entropy Reduction Formula:**
```
ΔS_total = Σ(ΔS_i) + I(mutual) - H(conflict) = 0
ΔS = 1 - (H_final / H_initial)
```

### 5. Audit Log Integration

**Path:** `/opt/data/.apex_audit_log.jsonl`

**Function:** Writes hash-chain audit log for every healing operation
- session_hash: SHA256(session_context)
- hash_signature: SHA256(session_hash + event_type)

**Log Format:**
```json
{
  "event_type": "self_heal_v2",
  "diagnosis": {"status": "healthy/critical", "leaked_fields": [...]},
  "isolation": {"status": "applied", "duration_minutes": 5},
  "recovery": {"status": "success", "actions": [...]},
  "session_hash": "sha256:...",
  "hash_signature": "sha256:...",
  "timestamp": "2026-06-08T10:00:00Z"
}
```