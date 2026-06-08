import os
import json
import yaml
import asyncio
from typing import Any, Dict, Tuple
from pathlib import Path

# Try to import lark-oapi from site-packages
try:
    from lark_oapi.api.im.v1 import CreateMessageRequest, CreateMessageRequestBody
    from lark_oapi.client import Client
except ImportError:
    # Use fallback path if needed (Windows site-packages path may be missing from sys.path)
    import sys
    sys.path.append(r"C:\Users\Administrator\AppData\Local\hermes\pylib")
    from lark_oapi.api.im.v1 import CreateMessageRequest, CreateMessageRequestBody
    from lark_oapi.client import Client

def _load_config() -> Dict[str, Any]:
    config_path = Path(r"C:\Users\Administrator\AppData\Local\hermes\config.yaml")
    if config_path.exists():
        return yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    return {}

def _get_credentials() -> Tuple[str, str, bool]:
    """凭证加载优先级：环境变量 > config.yaml。"""
    app_id = os.environ.get("FEISHU_APP_ID")
    app_secret = os.environ.get("FEISHU_APP_SECRET")
    
    config = _load_config()
    feishu_cfg = config.get("feishu", {})
    
    # 2. Config.yaml
    if not app_id:
        app_id = feishu_cfg.get("app_id")
    if not app_secret:
        app_secret = feishu_cfg.get("app_secret")
        
    card_enabled = feishu_cfg.get("message_card", {}).get("enabled", False)
    return app_id, app_secret, card_enabled

async def handle(event: str, context: Dict[str, Any]) -> Dict[str, Any] | None:
    # Only process agent:end for feishu platform
    if event != "agent:end" or context.get("platform") != "feishu":
        return None

    app_id, app_secret, enabled = _get_credentials()
    if not enabled or not app_id or not app_secret:
        return None

    chat_id = context.get("chat_id")
    if not chat_id:
        return None

    # Import build_card from our script
    from scripts.feishu_card_send import build_card
    
    try:
        card_json = build_card(context)
        
        # Send via Lark SDK
        client = Client.builder().app_id(app_id).app_secret(app_secret).build()
        content_str = json.dumps(card_json, ensure_ascii=False)

        req = (
            CreateMessageRequest.builder()
            .receive_id_type("chat_id")
            .request_body(
                CreateMessageRequestBody.builder()
                .receive_id(chat_id)
                .msg_type("interactive")
                .content(content_str)
                .build()
            )
            .build()
        )
        
        # SDK calls are usually sync, wrap in thread for async safety in gateway
        loop = asyncio.get_event_loop()
        resp = await loop.run_in_executor(None, lambda: client.im.v1.message.create(req))

        if not resp.success():
            print(f"[FeishuCardHook] Failed to send card: {resp.msg}", flush=True)
            return None
            
        # Successfully sent, tell gateway to skip sending default text
        return {"skip_text": True}

    except Exception as e:
        print(f"[FeishuCardHook] Error: {e}", flush=True)
        return None