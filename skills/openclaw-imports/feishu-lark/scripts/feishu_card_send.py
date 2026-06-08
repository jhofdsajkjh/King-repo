from typing import Any, Dict

def build_card(context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Build a Feishu interactive card from Hermes agent execution context.
    
    Expected context fields:
    - message: Original user query
    - response: Agent's reply text
    - model: Name of the LLM used
    - response_time_seconds: Float seconds taken
    - api_calls: Number of tool/API calls made
    - output_tokens: Tokens generated
    - failed: Boolean indicating error status
    - error: Error message if failed
    """
    user_query = context.get("message", "N/A")
    response = context.get("response", "")
    model = context.get("model", "Unknown")
    duration = context.get("response_time_seconds", 0.0)
    api_calls = context.get("api_calls", 0)
    tokens = context.get("output_tokens", 0)
    failed = context.get("failed", False)
    error = context.get("error", "")

    # Header style and title based on status
    header_template = "red" if failed else "blue"
    title = "❌ Hermes Task Failed" if failed else "✅ Hermes Response"

    # Card elements
    elements = [
        # User query snippet
        {
            "tag": "note",
            "elements": [{"tag": "plain_text", "content": f"Q: {user_query[:300]}"}]
        },
        {"tag": "hr"}
    ]

    # Main content (Error message or Response)
    if failed and error:
        elements.append({
            "tag": "markdown",
            "content": f"**Error encountered during processing:**\n```\n{error}\n```"
        })
    else:
        # Use markdown for response content
        elements.append({
            "tag": "markdown",
            "content": response
        })

    elements.append({"tag": "hr"})

    # Performance / Model Stats Bar (the "Caveman style" bar)
    status_text = f"🤖 {model}  |  ⏱ {duration}s  |  🔄 {api_calls} calls  |  🎫 {tokens} tokens"
    elements.append({
        "tag": "note",
        "elements": [{"tag": "plain_text", "content": status_text}]
    })

    # Return full card JSON
    return {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"content": title, "tag": "plain_text"},
            "template": header_template
        },
        "elements": elements
    }

if __name__ == "__main__":
    # Test script
    test_ctx = {
        "message": "Hello Hermes",
        "response": "Hello! I am your AI assistant.",
        "model": "MiniMax-m2.7",
        "response_time_seconds": 0.5,
        "api_calls": 1,
        "output_tokens": 20,
        "failed": False
    }
    import json
    print(json.dumps(build_card(test_ctx), indent=2, ensure_ascii=False))