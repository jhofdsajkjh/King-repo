#!/usr/bin/env python3
"""
hermes llm score calculator - APEX 全域LLM统一适配公式体系
USAGE: hermes skills call apex-llm-unified-formula score --scenario X --metrics A=X F=X ...
"""

import argparse
import json
import sys
from dataclasses import dataclass
from typing import Dict, Optional

# 预设场景配置
SCENARIOS = {
    "code_tasks": {
        "lambda": 0.95, "eta": 1,
        "alpha": 0.50, "beta": 0.20, "gamma": 0.15, "epsilon": 0.10, "delta": 0.05
    },
    "content_tasks": {
        "lambda": 0.95, "eta": 1,
        "alpha": 0.30, "beta": 0.40, "gamma": 0.20, "epsilon": 0.08, "delta": 0.02
    },
    "low_config": {
        "lambda": 0.90, "eta": 1,
        "alpha": 0.35, "beta": 0.20, "gamma": 0.15, "epsilon": 0.25, "delta": 0.05
    },
    "code_cascade": {
        "lambda": 0.95, "eta": 0.85,
        "alpha": 0.50, "beta": 0.20, "gamma": 0.15, "epsilon": 0.10, "delta": 0.05
    },
    "content_cascade": {
        "lambda": 0.95, "eta": 0.85,
        "alpha": 0.30, "beta": 0.40, "gamma": 0.20, "epsilon": 0.08, "delta": 0.02
    },
    "api_mixed": {
        "lambda": 1.0, "eta": 0.90,
        "alpha": 0.50, "beta": 0.20, "gamma": 0.15, "epsilon": 0.10, "delta": 0.05
    }
}

def calculate_score(scenario: str, metrics: Dict[str, float]) -> dict:
    """计算 LLM 总体效能得分"""
    if scenario not in SCENARIOS:
        return {"error": f"Unknown scenario: {scenario}. Available: {list(SCENARIOS.keys())}"}
    
    config = SCENARIOS[scenario]
    
    # 提取指标，缺失则默认 0
    A = metrics.get("A", 0)
    F = metrics.get("F", 0)
    R = metrics.get("R", 0)
    E = metrics.get("E", 0)
    C = metrics.get("C", 0)
    
    # 公式计算
    raw_score = (
        config["alpha"] * A +
        config["beta"] * F +
        config["gamma"] * R +
        config["epsilon"] * E -
        config["delta"] * C
    )
    
    # 应用系数
    S_total = config["eta"] * config["lambda"] * raw_score
    
    # 截断到 [0, 1]
    S_total = max(0.0, min(1.0, S_total))
    
    return {
        "scenario": scenario,
        "config": config,
        "metrics": {
            "accuracy": A,
            "fluency": F,
            "relevance": R,
            "efficiency": E,
            "cost": C
        },
        "score": {
            "raw": round(raw_score, 4),
            "S_total": round(S_total, 4)
        }
    }

def list_scenarios() -> list:
    """列出所有可用场景"""
    return [
        {"name": k, **v} 
        for k, v in SCENARIOS.items()
    ]

def main():
    parser = argparse.ArgumentParser(
        description="APEX LLM 统一评分公式 - 计算综合效能得分"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # score 命令
    score_parser = subparsers.add_parser("score", help="计算得分")
    score_parser.add_argument("--scenario", required=True, help="场景: code_tasks/content_tasks/low_config/code_cascade/content_cascade/api_mixed")
    score_parser.add_argument("--metrics", nargs="+", help="指标: A=0.9 F=0.8 ...")
    
    # list 命令
    subparsers.add_parser("list", help="列出所有场景配置")
    
    args = parser.parse_args()
    
    if args.command == "score":
        # 解析指标
        metrics = {}
        if args.metrics:
            for item in args.metrics:
                if "=" in item:
                    key, value = item.split("=", 1)
                    try:
                        metrics[key.strip()] = float(value.strip())
                    except ValueError:
                        print(f"Warning: Invalid value for {key}: {value}", file=sys.stderr)
        
        result = calculate_score(args.scenario, metrics)
        
        if "error" in result:
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)
        
        # 输出 JSON
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # 附加显示
        print(f"\n📊 评分结果: S_total = {result['score']['S_total']}")
        print(f"   场景: {result['scenario']}")
        print(f"   配置: λ={result['config']['lambda']}, η={result['config']['eta']}")
        
    elif args.command == "list":
        scenarios = list_scenarios()
        print(json.dumps(scenarios, indent=2, ensure_ascii=False))
        
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
