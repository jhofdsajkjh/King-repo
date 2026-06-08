# Footer Debug Log (Updated 2026-06-07)

This file is appended with one line per processed message, containing the exact footer string that was injected into the response.

## Current Status ✅

As of 2026-06-07, the footer system is **working correctly**. Sample entries from the log:

```
⏱310.1s · astron-code-latest · 28% · 🔁2
⏱217.2s · astron-code-latest · 110% · 🔁5
⏱37.7s · astron-code-latest · 281% · 🔁7
⏱78.7s · astron-code-latest · 464% · 🔁6
⏱31.9s · astron-code-latest · 64% · 🔁4
```

## What to Look For

- **⏱ value**: Non-zero response time indicates response time was measured correctly ✅
- **Model name**: Should show the actual model (e.g., `astron-code-latest`) ✅
- **% value**: Context usage percentage ✅
- **🔁 value**: Number of API calls made ✅

## Known Issue: `⏱0.0s · 🔁0`

If you see `⏱0.0s · 🔁0`, the issue is **NOT** in the footer injection code (which has been fixed). Check:

1. **Gateway code version**: Ensure the gateway is running the latest code
2. **Agent result keys**: Verify `agent_result` contains `model`, `input_tokens`, `output_tokens`, `api_calls`
3. **Feishu platform parsing**: Check `platforms/feishu.py` for footer marker parsing issues

## How to Inspect

- Run `cat /opt/hermes/gateway/footer_debug.log` to see recent entries
- Use `tail -n 10` for the latest lines
- Each line corresponds to the newest message sent by the gateway

## Fix Verification Log (2026-06-07)

Code review of `/opt/hermes/gateway/run.py` (lines 3969-4015) confirmed:

- ✅ `build_footer_line()` called with `response_text=` keyword
- ✅ `_model_name = agent_result.get("model") or ""`
- ✅ `_context_usage = (_total_tokens / _context_window * 100) if _context_window > 0 else None`
- ✅ Warning-level logging enabled for `FOOTER_CHECK`, `FOOTER_OUT`, `FOOTER_WRITTEN`
- ✅ Footer debug log written to `/opt/hermes/gateway/footer_debug.log`

## References

- `SKILL.md`: gateway-runtime-footer skill documentation
- `runtime_footer.py`: definition of `build_footer_line()`
- `run.py`: footer injection block (lines 3969-4015)
