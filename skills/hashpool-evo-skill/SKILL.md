---
name: hashpool-evo-skill
description: APEX 引擎的自适应哈希池缓存清洗范式
---

# HashPool-Evo-Skill

## 核心功能
基于 TTL + 频率阈值的混合淘汰算法，实现缓存自动清洗。

## 适用场景
在长生命周期运行的 Agent 系统中，清理无效轨迹指纹，提升 HashPool 检索命中率。

## 参数配置
- `ttl_seconds`: 缓存条目生命周期。
- `frequency_threshold`: 访问频次阈值。
