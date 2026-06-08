# Feishu Message Card Reply Hook

此方案允许 Hermes 在飞书回复时，自动将传统的文本回复替换为富文本交互卡片，并附带运行时统计数据。

## 1. 核心原理 (Hook 拦截)
通过拦截 `agent:end` 事件。Hook 脚本构建卡片并通过 API 发送，然后返回 `{"skip_text": True}`。

## 2. 核心补丁 (gateway/run.py)
在 `run.py` 中定位 `agent:end` 触发点，将其改为：

```python
# 修补后逻辑示例
hook_ctx["model"] = agent_result.get("model", "")
hook_ctx["response_time_seconds"] = round(_response_time, 1)
hook_ctx["api_calls"] = _api_calls
hook_ctx["input_tokens"] = agent_result.get("input_tokens", 0)
hook_ctx["output_tokens"] = agent_result.get("output_tokens", 0)

_hook_results = await self.hooks.emit_collect("agent:end", {
    **hook_ctx,
    "response": (response or "")[:500],
})

# 如果 Hook 返回了 skip_text，则清空原始回复以阻止发送
if any(isinstance(r, dict) and r.get("skip_text") for r in _hook_results):
    response = ""
```

## 3. Hook 文件结构
- `~/.hermes/hooks/feishu-card/HOOK.yaml`: 定义监听事件为 `agent:end`。
- `~/.hermes/hooks/feishu-card/handler.py`: 调用 `lark_oapi` 发送卡片。
- `~/.hermes/scripts/feishu_card_send.py`: 负责 JSON 拼接和进度条计算。
