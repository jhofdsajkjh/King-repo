#!/bin/bash
# 自动安装 hermes-free-token-hunter crontab 任务

# 备份现有 crontab
crontab -l > /tmp/crontab_backup_20260611 2>/dev/null || echo "# No crontab" > /tmp/crontab_backup_20260611

# 添加新任务（避免重复）
current_crontab=$(crontab -l 2>/dev/null || true)
if echo "$current_crontab" | grep -q "free-token-hunter"; then
    echo "✅ Crontab 任务已存在，跳过安装"
    exit 0
fi

# 添加新任务
echo "$current_crontab" | { cat; echo "0 8 * * * cd /opt/data && hermes skills call free-token-hunter cron >> /tmp/free-token-scan.log 2>&1"; } | crontab -

echo "✅ Crontab 任务已添加"
crontab -l | grep free-token-hunter
