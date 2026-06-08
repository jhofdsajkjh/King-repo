#!/bin/bash
# hermes evolve - APEX 自进化完整流程
# 包含 hermes .16 原生模块自动融合

set -euo pipefail

echo "🚀 开始 APEX 自进化流程..."
echo ""

# 1. 诊断
echo "📋 阶段 1: 系统诊断"
bash /opt/hermes/.cli_extensions/hermes-cli.sh self-heal-diagnose || true
echo ""

# 2. 融合 hermes .16 原生模块
echo "📋 阶段 2: Hermes .16 原生模块融合"
bash /opt/data/.hermes/scripts/hermes-fusion.sh || true
echo ""

# 3. 发现新技能
echo "📋 阶段 3: GitHub 技能发现"
if [ -f /opt/data/.hermes/cache/discovered_skills.json ]; then
    echo "  -> 发现新技能，开始下载..."
    bash /opt/hermes/.cli_extensions/hermes-cli.sh auto-pr-status || true
else
    echo "  -> 无新技能发现，跳过下载"
fi
echo ""

# 4. 升级技能
echo "📋 阶段 4: 技能升级 (skillopt 归一)"
bash /opt/hermes/.cli_extensions/hermes-cli.sh self-heal-heal || true
echo ""

# 5. 生成 PR
echo "📋 阶段 5: 生成并提交 PR"
bash /opt/hermes/.cli_extensions/hermes-cli.sh auto-pr-submit || true
echo ""

# 6. 等待 CI
echo "📋 阶段 6: 等待 CI/CD (5 分钟)"
sleep 300 || echo "  -> CI wait skipped"
echo ""

# 7. 自动合并
echo "📋 阶段 7: 自动合并 PR"
bash /opt/hermes/.cli_extensions/hermes-cli.sh auto-pr-merge || true
echo ""

echo "✅ APEX 自进化流程完成"
