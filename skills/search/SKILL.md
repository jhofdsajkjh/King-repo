---
name: search-skill-system
description: "规范化检索增强框架：SkillBank驱动+Select-Read-Act三段范式，替代大模型随机搜索"
version: 1.0.0
author: 小马
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [检索增强, RAG, SkillBank, Search, ApexSpiral]
    paradigm: Select-Read-Act
    skillbank_version: 1.0
---

# SearchSkill System — 规范化检索增强框架

## 核心范式

**摒弃随机搜索调用，改为 SkillBank 驱动 + Select-Read-Act 三段闭环**

大模型不该"凭直觉随机选关键词"，而应该：
1. **Select** — 从SkillBank筛选适配当前问题的搜索技能
2. **Read** — 读取技能规则，生成精准检索指令
3. **Act** — 执行检索，融合外部信息完成推理输出

---

## SkillBank 技能知识库

### 目录结构

```
search/skillbank/
├── index.md                    # 技能总索引
├── atomic_skills/              # 原子技能库
│   ├── keyword-expand.md       # 关键词扩写
│   ├── entity-trace.md         # 实体溯源
│   ├── time-filter.md          # 时间限定检索
│   ├── multi-source-verify.md  # 多源交叉验证
│   ├── context-recall.md       # 上下文回溯
│   ├── multi-hop.md            # 多跳递进检索
│   └── expert-query.md         # 专业领域检索
├── composite_skills/           # 组合技能（原子技能组合）
├── failure_log.md              # 失效案例记录
└── evolution_log.md           # 技能演进记录
```

### 已注册的原子技能

| 技能ID | 技能名称 | 触发条件 | 输出格式 |
|--------|---------|---------|---------|
| SK-001 | keyword-expand | 初始查询模糊、关键词不足 | 扩写后的5-8个关键词组合 |
| SK-002 | entity-trace | 涉及具体实体（人/公司/产品）| 实体基础信息+关联实体列表 |
| SK-003 | time-filter | 查询涉及时间范围/时事 | 时间范围精确检索式 |
| SK-004 | multi-source-verify | 关键事实需核实 | 多源结果对比表 |
| SK-005 | context-recall | 复杂多轮对话上下文 | 上下文关联摘要 |
| SK-006 | multi-hop | 需要多步推理 | 拆解后的子问题链 |
| SK-007 | expert-query | 专业领域术语 | 专业检索式+术语解释 |

---

## Select-Read-Act 执行流程

### SELECT — 技能筛选

**输入**: 用户问题/任务
**输出**: 适配的技能ID列表

**决策树**:

```
用户问题
  ├── 包含具体实体（公司/人/产品）→ SK-002 entity-trace
  ├── 包含时间线索（昨天/今年/2024）→ SK-003 time-filter
  ├── 模糊/泛化查询 → SK-001 keyword-expand
  ├── 需要核实关键事实 → SK-004 multi-source-verify
  ├── 复杂多轮/上下文丢失 → SK-005 context-recall
  ├── 多步推理/链式问题 → SK-006 multi-hop
  ├── 专业术语/垂直领域 → SK-007 expert-query
  └── 简单事实查询 → 直接检索（无需特殊技能）
```

### READ — 读取技能规则

**输入**: 选定的技能ID
**输出**: 该技能的执行规则 + 检索模板

每个技能都有固定的：
- 触发条件
- 检索式生成规则
- 输出格式模板
- 典型使用场景

### ACT — 执行检索

**输入**: 技能规则约束下的精准检索式
**输出**: 结构化检索结果

执行顺序：
1. 生成检索query
2. 调用搜索引擎
3. 过滤低相关结果
4. 按技能定义格式输出

---

## 检索质量评估

每次检索后记录：

| 指标 | 含义 |
|------|------|
| 检索精度 | 结果与问题相关度（1-5分）|
| 覆盖度 | 关键信息是否完整 |
| 时效性 | 数据是否最新 |
| 可信度 | 来源是否权威 |

**低于3分的检索需记录失败原因，写入 failure_log.md**

---

## 技能自演进机制

### 新技能生成

当现有技能连续2次检索失败：
1. 分析失败原因
2. 提炼新的检索策略
3. 编写新技能卡片
4. 写入 composite_skills/
5. 更新 index.md

### 技能淘汰

连续5次精度低于3的技能：
1. 标记为低效技能
2. 尝试与其他技能合并
3. 若无法优化则移除

---

## 与 ApexSpiral 的集成

ApexSpiral 的仓库学习循环是技能演进的燃料：

- 每轮仓库学习产生新的**技术概念检索需求**
- 这些需求提炼后可用于生成**新的expert-query技能**
- 失败案例驱动 SkillBank 持续迭代优化

---

## 使用示例

**用户问题**: "最近有哪些大模型上下文窗口超过100K？"

**执行流程**:

```
SELECT: 
  - SK-003 time-filter（最近）
  - SK-001 keyword-expand（上下文窗口、大模型）
  - SK-007 expert-query（长上下文技术）

READ:
  - 读取 SK-003 规则：时间限定为近6个月
  - 读取 SK-001 规则：扩写关键词
  - 读取 SK-007 规则：专业检索式模板

ACT:
  - 生成: "大模型 长上下文 100K 2024 2025"
  - 检索
  - 多源验证各厂商数据
  - 输出结构化结果
```

---

## 版本历史

| 版本 | 日期 | 变化 |
|------|------|------|
| 1.0 | 2026-05-20 | 初始框架建立 |

---

*本框架为小马自我进化体系的核心组成部分，源于 APEX SearchSkill 思想，适合 Hermes Agent 体系*
