# hermes-lark-streaming (Cheerwhy) — Analysis Notes

**Repo:** https://github.com/Cheerwhy/hermes-lark-streaming

## What it is

A streaming card plugin for Hermes Gateway that shows typing indicators, tool-call progress, thinking/reasoning steps, and token stats directly in Feishu interactive cards — via CardKit v2.0 streaming API.

**Core mechanism:** AST injection (patcher.py) — modifies `gateway/run.py` at 8 lifecycle hook points:
`on_message_started`, `on_answer_delta`, `on_thinking_delta`, `on_reasoning_delta`, `on_tool_update`, `on_message_completed`, `on_message_aborted`, `on_message_interrupted`.

## Compatibility Notes

| Requirement | Status |
|-------------|--------|
| Hermes version | **>= 0.11.0** (2026.4.23) |
| run.py path | `~/.hermes/hermes-agent/gateway/run.py` |
| Connection mode | **HTTP callback path only** — NOT WebSocket mode |
| Python | >= 3.11 |
| Dependencies | `lark-oapi>=1.4.0`, `PyYAML>=6.0` |
| Installation | `pip install hermes-lark-streaming` → `python -m hermes_lark_streaming install` |

## Why it may NOT be useful for this setup

The user's Hermes gateway runs in **WebSocket mode** (Feishu long connection). The 8 injection points in `run.py` hook into the HTTP request/response callback path. In WebSocket mode, these hooks may never fire.

**Verdict:** Low priority. Only useful if the user switches from WebSocket mode to HTTP callback mode — or if running Hermes in a mode that exercises the HTTP callback path. The streaming typing effect and token stats are cosmetic improvements, not functional ones.

## Key files (if reviewing source)

- `hermes_lark_streaming/patcher.py` — AST injection logic (14817 bytes)
- `hermes_lark_streaming/patch.py` — 8 hook wrappers calling into controller
- `hermes_lark_streaming/config.py` — reads from Hermes config.yaml (`streaming.*` keys)
- `hermes_lark_streaming/__main__.py` — CLI: install/uninstall/status/verify/restore
