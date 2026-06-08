#!/bin/bash
# phi-daemon 集成脚本 - APEX-ASI

echo "🚀 APEX-ASI phi-daemon 集成..."
echo ""

# 设置 PHI_INTERVAL 环境变量（秒）
export PHI_INTERVAL=30

# 运行 phi-daemon
echo "运行 phi-daemon.py once (单次循环)"
python3 /opt/data/APEX/phi-daemon.py once

echo ""
echo "✅ phi-daemon 集成完成"
