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
| `omni-fusion` | omni-fusion 融合增强 | `bash /opt/data/.hermes/scripts/omni-fusion-enhance.sh` |
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

### APEX 三阶融合升维配置

要启用完整的 APEX 三阶融合能力，需要配置以下环境变量：

```bash
# GitHub Token (必需，拥有 repo 权限)
export GITHUB_TOKEN='your_github_personal_access_token'

# GitHub 仓库所有者（可选）
export GITHUB_REPO_OWNER='apex'

# GitHub 仓库名（可选）
export GITHUB_REPO_NAME='hermes-self-evolution'
```

### 调试与验证

```bash
# 诊断系统状态
bash /opt/hermes/.cli_extensions/hermes-cli.sh self-heal-diagnose

# 查看审计日志
bash /opt/hermes/.cli_extensions/hermes-cli.sh audit

# 运行安全闭环审计
python3 /opt/hermes/.cli_extensions/hermes_security_audit.py run

# 查看多层审计链
python3 /opt/hermes/.cli_extensions/hermes_multi_layer_audit.py run

# 测试 hermes .16 状态
cat /opt/data/.hermes/v16/active.json
```

### APEX 自进化闭环触发

```bash
# 完整流程（诊断 → 发现 → 下载 → 升级 → PR → CI → 合并）
bash /opt/data/.hermes/scripts/hermes-evolve.sh
```

