#!/usr/bin/env python3
"""Hermes CLI Extensions Executor"""
import subprocess
import sys
import os
from pathlib import Path

def run_cmd(cmd, args=[]):
    """运行命令"""
    command = cmd.split()
    full_cmd = command + args
    print(f"Running: {' '.join(full_cmd)}")
    result = subprocess.run(full_cmd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.returncode == 0

def main():
    if len(sys.argv) < 2:
        print("Usage: hermes_cli_extensions.py <command> [args...]")
        print("Commands: self-heal-diagnose, self-heal-heal, auto-pr-status, auto-pr-submit, auto-pr-merge, evolve, audit")
        sys.exit(1)
    
    cmd = sys.argv[1]
    args = sys.argv[2:] if len(sys.argv) > 2 else []
    
    scripts_dir = Path(__file__).parent
    script_path = scripts_dir / f"{cmd}.sh"
    
    if script_path.exists():
        run_cmd(f"bash {script_path}")
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
