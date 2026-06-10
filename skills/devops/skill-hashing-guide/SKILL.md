---
name: skill-hashing-guide
category: devops
description: 生成技能哈希文件并检查权限的完整流程
---

# 技能哈希生成指南

## 概述

为技能目录生成 `.hash` 文件用于 HashPool 检索校验，需检查目录权限并批量生成 SHA256 哈希。

## 操作流程

### 1. 检查权限

```bash
# 列出非 hermes 拥有的技能目录
ls -la /opt/data/skills/ | grep "root root" | awk '{print $9}'

# 常见 root-owned 目录
apex-realized
hashpool-evo-skill
openclaw-imports
search
search-workflow
user-preferences
```

### 2. 修复权限（需要 root）

```bash
# 修复 root-owned 目录
chown -R hermes:hermes /opt/data/skills/{apex-realized,hashpool-evo-skill,openclaw-imports,search,search-workflow,user-preferences}
```

### 3. 生成哈希文件

```python
import hashlib
from pathlib import Path

skills_dir = Path("/opt/data/skills")

for skill_dir in skills_dir.iterdir():
    if not skill_dir.is_dir() or skill_dir.name.startswith('_'):
        continue
    
    sk_file = skill_dir / "SKILL.md"
    if sk_file.exists():
        content = sk_file.read_text(encoding="utf-8")
        sha256_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        hash_file = skill_dir / ".hash"
        hash_file.write_text(f"{sha256_hash}  SKILL.md\n")
        print(f"Generated: {skill_dir.name} -> {sha256_hash[:16]}...")
```

### 4. 验证哈希文件

```bash
# 检查已生成的哈希文件
ls -la /opt/data/skills/*/|.hash 2>/dev/null | head -20

# 验证特定技能哈希
cat /opt/data/skills/hermes-self-heal/.hash
```

## 错误处理

### 权限 denied

**错误：** `PermissionError: [Errno 13] Permission denied`

**原因：** 目录由 root 拥有，hermes 用户无写入权限

**解决：** 执行 `chown -R hermes:hermes <directory>` 或联系管理员授权

### 未找到 SKILL.md

**错误：** `FileNotFoundError: SKILL.md`

**原因：** 技能目录缺少 SKILL.md 文件

**解决：** 补全 SKILL.md 文档或删除空目录

## HashPool 配置

### TTL 阈值

```bash
# 默认 24 小时（86400 秒）
export HASHPOOL_TTL=86400
```

### 频率阈值

```bash
# 默认 3 次
export HASHPOOL_FREQ=3
```

## 相关技能

- `hashpool-evo-skill`：HashPool 自适应清洗范式
- `hermes-cli-extensions`：CLI 扩展命令
- `apex-realized`：APEX 原生吞噬进化闭环

## 更新日志

| 版本 | 变更内容 |
|------|---------|
| v1.1 (2026-06-10) | 增加权限修复步骤、错误处理章节 |
| v1.0 (2026-06-09) | 初始版本：基础哈希生成流程 |