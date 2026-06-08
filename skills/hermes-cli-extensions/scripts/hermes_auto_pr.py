#!/usr/bin/env python3
"""hermes auto-pr CLI Extension - GitHub PR 自动化"""

import sys
import os
import json
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime

GITHUB_REPO_OWNER = os.environ.get("GITHUB_REPO_OWNER", "apex")
GITHUB_REPO_NAME = os.environ.get("GITHUB_REPO_NAME", "hermes-self-evolution")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

def run_cmd(cmd):
    """运行命令"""
    print(f"  → {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.returncode == 0

def status():
    """PR 状态查询"""
    print("📋 PR 状态查询")
    print("=" * 60)
    
    if not GITHUB_TOKEN:
        print("⚠️  GitHub token 未配置")
        return False
    
    # 查询当前打开的 PR
    cmd = f"gh pr list --state open --limit 5 --repo {GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout if result.stdout else "(no PRs)")
    return True

def submit():
    """提交 PR"""
    print("🔄 提交 PR...")
    print("=" * 60)
    
    # 1. git add -A
    print("  1. git add -A")
    run_cmd("git add -A")
    
    # 2. git commit -m
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"skill: auto-upgrade at {timestamp}"
    print(f"  2. git commit -m '{commit_msg}'")
    run_cmd(f'git commit -m "{commit_msg}" || true')
    
    # 3. git push origin HEAD
    print("  3. git push origin HEAD")
    run_cmd("git push origin HEAD || git push origin main")
    
    # 4. gh pr create
    print("  4. gh pr create")
    run_cmd(f'gh pr create --title "skill: auto-upgrade" --body "Auto-generated PR at {timestamp}" || true')
    
    # 5. 保存 PR 信息
    pr_info = {
        "timestamp": datetime.now().isoformat(),
        "status": "submitted",
        "commit_msg": commit_msg
    }
    pr_info_path = Path("/opt/data/.hermes/cache/last_pr.json")
    pr_info_path.parent.mkdir(parents=True, exist_ok=True)
    with open(pr_info_path, "w") as f:
        json.dump(pr_info, f, indent=2)
    
    print(f"✅ PR 已提交: {pr_info_path}")
    return True

def merge():
    """合并 PR"""
    print("🔄 合并 PR...")
    print("=" * 60)
    
    if not GITHUB_TOKEN:
        print("⚠️  GitHub token 未配置")
        return False
    
    # 查询最新打开的 PR
    cmd = f"gh pr list --state open --limit 1 --json number --repo {GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if not result.stdout.strip():
        print("  → 无打开的 PR")
        return False
    
    try:
        pr = json.loads(result.stdout.strip())
        pr_number = pr[0]["number"]
        print(f"  → 合并 PR #{pr_number}")
        
        # 合并 PR
        merge_cmd = f"gh pr merge {pr_number} --squash --repo {GITHUB_REPO_OWNER}/{GITHUB_REPO_NAME}"
        run_cmd(merge_cmd)
        
        # 保存合并信息
        merge_info = {
            "timestamp": datetime.now().isoformat(),
            "status": "merged",
            "pr_number": pr_number
        }
        merge_info_path = Path("/opt/data/.hermes/cache/last_merge.json")
        with open(merge_info_path, "w") as f:
            json.dump(merge_info, f, indent=2)
        
        print(f"✅ PR 已合并: {merge_info_path}")
        return True
    except Exception as e:
        print(f"❌ 错误: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: hermes_auto_pr.py <command>")
        print("Commands: status, submit, merge")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "status":
        success = status()
    elif command == "submit":
        success = submit()
    elif command == "merge":
        success = merge()
    else:
        print(f"Unknown command: {command}")
        success = False
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
