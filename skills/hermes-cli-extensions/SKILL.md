---
name: hermes-cli-extensions
description: Hermes CLI 扩展技能 - 提供 self-heal, auto-pr, evolve 命令
category: software-development
tags:
  - cli
  - extensions
  - automation
---

# Hermes CLI Extensions

提供 hermes CLI 的扩展命令支持。

## Commands

| Command | Description | Usage |
|---------|-------------|-------|
| `self-heal-diagnose` | 系统自愈诊断 | `bash /opt/hermes/.cli_extensions/hermes-cli.sh self-heal-diagnose` |
| `self-heal-heal` | 系统自愈恢复 | `bash /opt/hermes/.cli_extensions/hermes-cli.sh self-heal-heal` |
| `auto-pr-status` | PR 状态查询 | `bash /opt/hermes/.cli_extensions/hermes-cli.sh auto-pr-status` |
| `auto-pr-submit` | 提交 PR | `bash /opt/hermes/.cli_extensions/hermes-cli.sh auto-pr-submit` |
| `auto-pr-merge` | 合并 PR | `bash /opt/hermes/.cli_extensions/hermes-cli.sh auto-pr-merge` |
| `evolve` | 完整自进化流程 | `bash /opt/data/.hermes/scripts/hermes-evolve.sh` |
| `audit` | 查看审计日志 | `bash /opt/hermes/.cli_extensions/hermes-cli.sh audit` |

## Usage

### 基础命令调用

```bash
# 诊断系统健康度
bash /opt/hermes/.cli_extensions/hermes-cli.sh self-heal-diagnose

# 查看审计日志
bash /opt/hermes/.cli_extensions/hermes-cli.sh audit

# 执行自进化流程
bash /opt/data/.hermes/scripts/hermes-evolve.sh
```

### Crontab 自动化配置

```bash
# 编辑 crontab
crontab -e

# 添加任务（每 30 分钟执行一次自进化）
*/30 * * * * cd /opt/data && bash .hermes/scripts/hermes-evolve.sh >> /tmp/apex-evolve.log 2>&1
```

### APEX 自进化闭环触发

```bash
# 完整流程（诊断 → 发现 → 下载 → 升级 → PR → CI → 合并）
bash /opt/data/.hermes/scripts/hermes-evolve.sh
```

