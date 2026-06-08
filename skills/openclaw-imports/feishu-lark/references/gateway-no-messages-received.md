# Troubleshooting: Gateway Connected but No Messages Received

If the Hermes Gateway shows `✓ feishu connected` in the logs, but sending messages in the Feishu chat does not trigger any incoming message events in the logs:

1. **Root Cause:** Feishu application is not subscribed to message receive events.
2. **Fix Steps:**
   - Log into [Feishu Open Platform](https://open.feishu.cn/app).
   - Navigate to **"事件与回调" (Events & Callbacks)** → **"事件配置" (Event Configuration)**.
   - Ensure the "订阅方式" (Subscription Method) is **"使用长连接接收事件" (Use long connection)**.
   - Click **"添加事件" (Add Event)** and ensure **`im.message.receive_v1`** is in the "已添加事件" (Added Events) list.
   - Ensure the required permissions (`im:message`, `im:message:send_as_bot`) are enabled under **"权限管理" (Permission Management)**.
   - Publish a new version of the app if requested.
   - Messages sent to the bot should now appear in `gateway.log` as `Incoming event: im.message.receive_v1`.

Note: You do NOT need to restart the Gateway. The existing WebSocket connection will start pushing events as soon as the app configuration is updated and published.
