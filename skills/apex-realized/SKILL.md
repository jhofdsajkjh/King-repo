---
name: apex-realized
description: "Realizes APEX-AGI concepts (Multi-Agent, Self-Heal) using Hermes native tools."
version: 1.0.0
author: Hermes
license: MIT
tags: [multi-agent, self-heal, orchestration]
---

# APEX Realized (Hermes Native)

This skill replaces the fake APEX-AGI Rust code with **real** Hermes capabilities.

## 1. Multi-Agent Orchestration (Real)

APEX claimed to have 5 agents. Hermes `delegate_task` makes this real.

**Usage:** Use `delegate_task` with these personas.

### Roles

**A. Coding Agent**
- **Goal:** Write/fix code.
- **Context:** "You are the Coding Agent. Write high-quality, tested code. Read existing code first. Follow best practices."
- **Toolsets:** `['terminal', 'file']`

**B. Research Agent**
- **Goal:** Find info/analyze.
- **Context:** "You are the Research Agent. Search codebase/web. Analyze patterns. Provide detailed reports."
- **Toolsets:** `['search', 'web', 'file']`

**C. System Agent**
- **Goal:** Infrastructure/Ops.
- **Context:** "You are the System Agent. Manage infrastructure. Run health checks. Monitor resources."
- **Toolsets:** `['terminal', 'cronjob']`

**D. Monitor Agent**
- **Goal:** Watch for issues.
- **Context:** "You are the Monitor Agent. Check system health. Detect regressions. Alert on errors."
- **Toolsets:** `['terminal', 'session_search']`

**E. Orchestrator (You)**
- **Action:** Decompose tasks and assign to A-D via `delegate_task`.

## 2. Self-Heal & Health Check (Real)

APEX had a fake "Self-Heal" engine. Use this checklist instead.

**Run this to heal Hermes:**

1. **Check Tools:** `hermes tools` (Verify connectivity).
2. **Check Cron:** `cronjob list` (Ensure jobs are running).
3. **Check Memory:** `session_search` (Verify context recall).
4. **Check Network:** `ping 8.8.8.8` (Verify internet).
5. **Check Disk:** `df -h` (Ensure space > 10%).

**Script:**
```bash
# Quick Health Check
echo "=== Hermes Health ===" && \
hermes tools 2>&1 | head -5 && \
echo "=== Cron Jobs ===" && \
hermes cron list 2>&1 | head -5 && \
echo "=== Disk ===" && \
df -h / | tail -1
```

## 3. Feishu Adapter (Native)

APEX had a basic Feishu adapter. Hermes has **native** Feishu support.
- **Config:** `config.yaml` > `channels` > `feishu`.
- **Features:** Native rendering, file upload, WebSocket push.
- **No extra code needed.**
