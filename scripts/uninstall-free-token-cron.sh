#!/bin/bash
# 取消 hermes-free-token-hunter crontab 任务

crontab -l | grep -v "free-token-hunter" | crontab -

echo "✅ Crontab 任务已移除"
