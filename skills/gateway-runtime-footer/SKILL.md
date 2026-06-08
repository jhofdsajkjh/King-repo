---
name: gateway-runtime-footer
title: Fixing and Debugging Hermes Gateway Runtime Footer
description: Capture the workflow for fixing footer display issues in Hermes gateway, including code changes, logging, and verification.
category: gateway
version: 1.0
tags: [debugging, footer, runtime, hermes-gateway]
---

## Overview

This skill documents the proven workflow for diagnosing and fixing the Hermes gateway runtime footer displaying `⏱0.0s · 🔁0` (or other missing values). It includes the root causes, the code changes, and verification steps.

### Critical Note (2026-06-08)

The footer bug has been **verified as fixed** in `/opt/hermes/gateway/run.py` (lines 3969-3998). The implementation correctly:
- Uses `response_text=` keyword in `build_footer_line()` call
- Retrieves `model_name` from `agent_result.get("model")`
- Computes `context_usage` from `(input_tokens + output_tokens) / context_window * 100`

**Current status**: `gateway-runtime-footer` skill documentation is accurate. If you see `⏱0.0s · 🔁0`, check:
- Gateway process running latest code (restart if needed)
- `agent_result` contains expected keys (`model`, `input_tokens`, `output_tokens`, `api_calls`)
- Feishu platform-specific footer parsing in `platforms/feishu.py`

### Emergency Note (2026-06-08)

During this session, the following issue was discovered and documented:
- **Symptom**: Gateway was stuck with `process` tool for 1805s
- **Root cause**: `gateway_timeout` set to `1800` in config, but process exceeded it
- **Fix**: Confirmed `agent.gateway_timeout` setting in config.yaml (line 24)

## Problem Statement (Historical)

- Footer injection used the wrong keyword argument `text=` instead of `response_text=`. ❌ (FIXED)
- Model name was fetched from `hook_ctx` which did not contain `model_name`. ❌ (FIXED)
- Context usage was never computed. ❌ (FIXED)
- Logging was suppressed by `HERMES_QUIET=1`, hiding debug output. ❌ (FIXED)
- No persistent verification of the generated footer. ❌ (FIXED)

## Fix Steps (Already Applied)

1. **Parameter Alignment** – In `run.py` change the call to `build_footer_line` to use `response_text=`. ✅
2. **Model Name Source** – Retrieve model from `agent_result.get("model")`. ✅
3. **Context Usage** – Compute from `input_tokens + output_tokens` and the model's `context_window` (default 128 k). ✅
4. **Add Warning‑level Logging** – Use `logger.warning` for `FOOTER_CHECK`, `FOOTER_OUT`, `FOOTER_WRITTEN` so logs appear even when `HERMES_QUIET=1`. ✅
5. **Set `HERMES_QUIET` to `0`** – Ensure logs are not fully suppressed. ✅
6. **Persist Footer Debug Info** – Write the generated footer line to `/opt/hermes/gateway/footer_debug.log` after each response. ✅
7. **Restart the gateway** (kill PID 1) to load the new code. ✅

## Verification

- Send a test message in Feishu.\n- Confirm that the card footer now shows realistic values, e.g. `⏱3.5s · gpt‑4 · 20% · 🔁2`.\n- Inspect `/opt/hermes/gateway/footer_debug.log` for the latest line.\n- Look for `FOOTER_CHECK`, `FOOTER_OUT`, `FOOTER_WRITTEN` entries in the gateway stdout/stderr.\n- **Current status (2026-06-07)**: Log file contains valid entries showing `⏱310.1s · astron-code-latest · 28% · 🔁2` etc.

## References

- `references/footer_debug_log.md`: log of generated footer strings for each response.

- `runtime_footer.py` – definition of `build_footer_line`.
- `run.py` – footer injection block.
- Debug log example: see `references/footer_debug_log.md`.

---
