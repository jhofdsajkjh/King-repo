import json
import datetime
from typing import Any, Dict

def get_progress_bar(pct: float, length: int = 10) -> str:
    filled = int(round(length * pct / 100))
    return "█" * filled + "░" * (length - filled)

def build_card(context: Dict[str, Any]) -> Dict[str, Any]:
    user_query = context.get("message", "N/A")
    response = context.get("response", "")
    model = context.get("model", "Unknown")
    duration = context.get("response_time_seconds", 0.0)
    api_calls = context.get("api_calls", 0)
    
    total_tokens = context.get("input_tokens", 0) + context.get("output_tokens", 0)
    ctx_limit = context.get("config_context_length")
    
    if ctx_limit:
        ctx_pct = min(100.0, (total_tokens / ctx_limit) * 100)
        ctx_str = f"{total_tokens/1000:.1f}k/{ctx_limit/1000:.1f}k [{get_progress_bar(ctx_pct)}] {ctx_pct:.1f}%"
    else:
        ctx_str = f"{total_tokens/1000:.1f}k tokens"

    failed = context.get("failed", False)
    header_template = "red" if failed else "purple"
    title = f"✍️ {'任务失败' if failed else '已完成'} | {model}"
    
    return {
        "config": {"wide_screen_mode": True},
        "header": {"title": {"content": title, "tag": "plain_text"}, "template": header_template},
        "elements": [
            {"tag": "note", "elements": [{"tag": "plain_text", "content": f"💬 用户提问: {user_query[:100]}"}]},
            {"tag": "hr"},
            {"tag": "markdown", "content": response},
            {"tag": "hr"},
            {"tag": "note", "elements": [{"tag": "plain_text", "content": f"⏱ {duration}s · {model} · 调用API {api_calls} 次 · 上下文 {ctx_str}"}]}
        ]
    }
