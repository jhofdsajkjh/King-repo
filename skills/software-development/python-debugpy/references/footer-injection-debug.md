# Footer Injection Debugging

## Common Issues with Hermes Gateway Footer

### Symptom: Footer shows `⏱0.0s · 🔁0` — all values are zero

#### Root Causes

1. **Silent `TypeError` from wrong keyword argument**
   - `build_footer_line()` uses `response_text` but call site passed `text=`
   - Caught by `except Exception: pass` → completely silent failure
   - **Fix:** Compare function signature against call site keyword args

2. **`model_name` source wrong**
   - `hook_ctx` dict lacks `model_name` key (only has `platform`, `user_id`, `session_id`, `message`)
   - **Fix:** Use `agent_result.get("model")` instead

3. **`context_usage` never computed**
   - No key in `hook_ctx` or `agent_result` for context usage
   - **Fix:** Compute from `input_tokens + output_tokens` / `model.context_window`

4. **Stale `.pyc` bytecode**
   - Long-running gateway process loads old `.pyc` from `__pycache__/`
   - Source file has the fix but bytecode doesn't
   - **Fix:** `rm gateway/__pycache__/run.cpython-*.pyc && kill -9 1`

5. **`HERMES_QUIET=1` suppressing logs**
   - `HERMES_QUIET=1` sets log level to WARN+
   - `logger.info()` calls produce no output
   - **Fix:** Use `logger.warning()` for debug logging, or set `HERMES_QUIET=0`

#### Debug Checklist
- [ ] Verify keyword args match function signature
- [ ] Verify all data sources (`agent_result` keys) exist
- [ ] Check `.pyc` timestamps vs source timestamps
- [ ] Confirm log level isn't suppressing diagnostic output
- [ ] Kill process and delete `__pycache__/` before restart
- [ ] Test `build_footer_line()` with known-good args to verify it works

#### Reference
- `gateway/run.py` — footer injection at ~line 3970
- `gateway/runtime_footer.py` — `build_footer_line()` signature
- `gateway/platforms/feishu.py` — `__HERMES_FOOTER__` parsing in `_build_interactive_card_payload()`
