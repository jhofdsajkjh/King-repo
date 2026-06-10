#!/usr/bin/env python3
"""
hermes free-token-hunter CLI Extension
每日自动搜罗免费 Token 资源
"""

import sys
import os
import json
import re
import time
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
import urllib.request
from urllib.error import URLError, HTTPError

CACHE_DIR = Path("/opt/data/.hermes/cache")
SCAN_LOG = CACHE_DIR / "free_token_scan.jsonl"
LATEST_SCAN = CACHE_DIR / "free_token_latest.json"

def ensure_cache_dir():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

def load_cache():
    """加载缓存"""
    if LATEST_SCAN.exists():
        with open(LATEST_SCAN, "r") as f:
            return json.load(f)
    return {"timestamp": None, "sources": []}

def save_cache(data):
    """保存缓存"""
    ensure_cache_dir()
    with open(LATEST_SCAN, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def log_scan_event(event):
    """记录扫描事件"""
    ensure_cache_dir()
    with open(SCAN_LOG, "a") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

def search_github(query):
    """在 GitHub 搜索项目"""
    try:
        url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=5"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Hermes-Agent/1.0',
            'Accept': 'application/vnd.github.v3+json'
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            results = []
            for item in data.get('items', []):
                results.append({
                    "name": item['full_name'],
                    "url": item['html_url'],
                    "stars": item['stargazers_count'],
                    "updated": item['updated_at'],
                    "description": item.get('description', ''),
                    "type": "github",
                    "tags": ["free", "token"] + (item.get('topics', []))
                })
            return results
    except Exception as e:
        return [{"error": str(e)}]

def search_reddit(query):
    """在 Reddit 搜索（简化版）"""
    try:
        url = f"https://www.reddit.com/search.json?q={query}&sort=relevance&limit=3"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Hermes-Agent/1.0'
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            results = []
            for item in data.get('data', {}).get('children', []):
                post = item['data']
                results.append({
                    "name": post.get('title', 'N/A'),
                    "url": f"https://reddit.com{post.get('permalink', '')}",
                    "ups": post.get('ups', 0),
                    "updated": datetime.fromtimestamp(post['created']).isoformat(),
                    "type": "reddit",
                    "tags": ["community", "free"]
                })
            return results
    except Exception as e:
        return [{"error": str(e)}]

def scan_all_sources():
    """扫描所有免费 Token 来源"""
    print("🔍 开始扫描免费 Token 资源...")
    print("=" * 60)
    
    scan_start = datetime.now()
    
    # GitHub 搜索
    print("\n📦 GitHub 搜索...")
    github_queries = [
        "free-gpt", 
        "openai-api-key",
        "chatgpt-free",
        "token-sharing"
    ]
    
    github_results = []
    for query in github_queries:
        print(f"  → 搜索: {query}")
        results = search_github(query)
        github_results.extend(results)
        time.sleep(1)  # 避免限流
    
    # Reddit 搜索
    print("\n💬 Reddit 搜索...")
    reddit_queries = ["free gpt", "chatgpt free access", "free api key"]
    
    reddit_results = []
    for query in reddit_queries:
        print(f"  → 搜索: {query}")
        results = search_reddit(query)
        reddit_results.extend(results)
        time.sleep(1)
    
    # 合并结果
    all_results = github_results + reddit_results
    
    # 生成唯一标识
    for i, item in enumerate(all_results):
        if 'error' not in item:
            item['id'] = hashlib.md5(
                f"{item.get('name', '')}:{item.get('url', '')}".encode()
            ).hexdigest()[:12]
    
    # 保存结果
    output = {
        "timestamp": scan_start.isoformat(),
        "completed": datetime.now().isoformat(),
        "sources": all_results,
        "summary": {
            "total": len(all_results),
            "github": len(github_results),
            "reddit": len(reddit_results),
            "errors": sum(1 for x in all_results if 'error' in x)
        }
    }
    
    save_cache(output)
    log_scan_event({
        "event_type": "free_token_scan",
        "timestamp": output["timestamp"],
        "completed": output["completed"],
        "sources_found": output["summary"]["total"],
        "errors": output["summary"]["errors"]
    })
    
    return output

def cmd_list():
    """列出已发现的资源"""
    cache = load_cache()
    print(f"📋 已发现的免费 Token 资源 ({len(cache.get('sources', []))} 个)")
    print("=" * 60)
    
    for source in cache.get('sources', [])[:20]:
        if 'error' not in source:
            print(f"• {source['name']}")
            print(f"  URL: {source['url']}")
            if source.get('stars'):
                print(f"  ⭐ {source['stars']} stars")
            if source.get('updated'):
                print(f"  📅 {source['updated']}")
            print()

def cmd_scan():
    """扫描最新资源"""
    result = scan_all_sources()
    print("\n" + "=" * 60)
    print("✅ 扫描完成!")
    print(f"  总数: {result['summary']['total']}")
    print(f"  GitHub: {result['summary']['github']}")
    print(f"  Reddit: {result['summary']['reddit']}")
    print(f"  错误: {result['summary']['errors']}")
    print(f"\n  结果已保存到: {LATEST_SCAN}")
    print(f"  日志已追加到: {SCAN_LOG}")

def cmd_stats():
    """统计资源"""
    cache = load_scan()
    summary = cache.get('summary', {})
    print(f"📊 统计信息")
    print("=" * 60)
    print(f"  总数: {summary.get('total', 0)}")
    print(f"  GitHub: {summary.get('github', 0)}")
    print(f"  Reddit: {summary.get('reddit', 0)}")
    print(f"  错误: {summary.get('errors', 0)}")
    if cache.get('timestamp'):
        print(f"  上次扫描: {cache['timestamp']}")

def cmd_cron():
    """Cron 触发"""
    print(" Cron: 每日自动扫描任务")
    print("=" * 60)
    cmd_scan()

def main():
    if len(sys.argv) < 2:
        print("Usage: hermes_free_token.py <command>")
        print("Commands: list, scan, stats, cron")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "list":
        cmd_list()
    elif command == "scan":
        cmd_scan()
    elif command == "stats":
        cmd_stats()
    elif command == "cron":
        cmd_cron()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()
