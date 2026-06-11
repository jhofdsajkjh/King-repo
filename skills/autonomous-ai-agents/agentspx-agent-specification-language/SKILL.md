---
name: agentspx-agent-specification-language
category: autonomous-ai-agents
version: "2026.6.11"
description: AgentSPEX - Agent SPecification and EXecution Language for APEX integration
tags:
  - agentspx
  - agent-specification
  - execution-engine
  - workflow-automation
---

# AgentSPEX - Agent Specification and Execution Language

基于 arXiv:2604.13346 的 AgentSPEX 语言，为 APEX 原生基因引擎提供显式 workflow 定义能力。

## 一、核心特性

| 特性 | 说明 |
|------|------|
| **五维基因结构** | signals_match + preconditions + strategy + constraints + validation |
| **显式 workflow** | LangGraph/DSPy/CrewAI 结构化定义 |
| **基因验证** | fitness + validation 双验证机制 |
| **自进化支持** | discover → download → merge → pr → ci/cd → cron |
| **五层架构** | L1元 → L2触发 → L3前置 → L4执行 → L5约束 |

## 二、语法结构

### 1. 基因定义

```json
{
  "type": "apex_gene",
  "id": "agent_spec_example",
  "category": "agent_workflow",
  "signals_match": ["触发信号1", "触发信号2"],
  "preconditions": ["前置条件1", "前置条件2"],
  "strategy": ["步骤1", "步骤2", "步骤3"],
  "constraints": {
    "max_iterations": 10,
    "timeout_seconds": 300
  },
  "validation": ["验证条件1", "验证条件2"],
  "fitness": 0,
  "created": "2026-06-11T00:00:00Z"
}
```

### 2. Workflow 定义

```json
{
  "workflow_name": "multi_agent_code_review",
  "version": "1.0",
  "agents": [
    {
      "name": "architect",
      "role": "system_architect",
      "task": "分析系统架构并生成设计文档"
    },
    {
      "name": "reviewer",
      "role": "code_reviewer",
      "task": "审查代码并提出改进建议"
    }
  ],
  "sequence": ["architect", "reviewer"],
  "validation": {
    "min_score": 0.8,
    "timeout": 300
  }
}
```

## 三、与 APEX 集成

### 1. 基因注入流程

```
1. 发现 AgentSPEX 基因定义
2. 解析五维结构 (signals_match + preconditions + strategy + constraints + validation)
3. 注入 APEX 基因引擎 (apex_gene 类型)
4. 生成 fitness 评分
5. 写入 hermes_memory.db
```

### 2. LDR 循环集成

| LDR 阶段 | AgentSPEX 映射 |
|----------|----------------|
| **Orient** | 定位 workflow 定义文件 |
| **Plan** | 解析 JSON schema → 提取五维结构 |
| **Execute** | 执行 workflow agents 序列 |
| **Verify** | 五维验证：signals_match → preconditions → strategy → constraints → validation |
| **Evolve** | 写入 apex_gene → 更新基因库存 |
| **Persist** | 批量注入 → hermes_memory.db |

## 四、使用命令

```bash
# 查看可用的 AgentSPEX 示例
hermes skills call agentspx-agent-specification-language list-examples

# 验证基因定义
hermes skills call agentspx-agent-specification-language validate \
  --gene-path /path/to/gene.json

# 执行 workflow
hermes skills call agentspx-agent-specification-language run \
  --workflow-path /path/to/workflow.json

# 生成基因模板
hermes skills call agentspx-agent-specification-language template \
  --output-path /path/to/new_gene.json
```

## 五、五维结构详解

### L1 元基因 (Metadata)

| 字段 | 说明 |
|------|------|
| `type` | gene 类型 (apex_gene) |
| `id` | 基因唯一标识 |
| `category` | 基因分类 |
| `signals_match` | 触发信号列表 |
| `fitness` | 适应度评分 |

### L2 触发 (Trigger)

| 字段 | 说明 |
|------|------|
| `signals_match` | 文本/事件触发关键词 |
| `preconditions` | 激活前必须满足的条件 |

### L3 前置 (Preconditions)

| 字段 | 说明 |
|------|------|
| `dependencies` | 依赖的技能/工具/数据 |
| `environment` | 运行环境要求 |
| `permissions` | 所需权限级别 |

### L4 执行 (Strategy)

| 字段 | 说明 |
|------|------|
| `strategy` | 执行步骤序列 |
| `parallelism` | 并行执行配置 |
| `retries` | 重试策略 |

### L5 约束 (Constraints)

| 字段 | 说明 |
|------|------|
| `constraints` | 边界约束 |
| `validation` | 成功标准 |
| `max_iterations` | 最大迭代次数 |

## 六、参考文献

Wang et al. (2026). *AgentSPEX: An Agent SPecification and EXecution Language*. arXiv:2604.13346 [cs.CL].

## 七、相关技能

- `hermes-self-heal`：自愈系统（依赖基因验证）
- `hermes-cli-extensions`：CLI 扩展（AgentSPEX 命令入口）
- `apex-realized`：APEX-ASI 全维度基因升级
