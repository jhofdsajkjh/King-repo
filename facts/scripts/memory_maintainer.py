#!/usr/bin/env python3
"""
Memory Maintainer v1.0
Automated memory optimization engine for Hermes Agent.
Run inside NAS Docker container or as a Cron Job.
Facts path: /opt/data/.hermes/facts/
"""

import os
import json
import time
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger("MemoryMaintainer")

# ──────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────
FACTS_DIR = Path(os.getenv("HERMES_HOME", "/opt/data")) / ".hermes" / "facts"
MEMORY_FILE = FACTS_DIR / "memory.json"
ARCHIVE_FILE = FACTS_DIR / "archive.json"
THRESHOLD = float(os.getenv("MEMORY_THRESHOLD", "0.8"))
RETENTION_DAYS = int(os.getenv("RETENTION_DAYS", "10"))
MAX_MEMORY_SIZE = int(os.getenv("MAX_MEMORY_CHARS", "3000"))
RETENTION_SECONDS = RETENTION_DAYS * 86400

# ──────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────
def load_json(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path: Path, data: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_usage_rate(entries: list[dict], max_chars: int = MAX_MEMORY_SIZE) -> float:
    total = sum(len(e.get("content", "")) for e in entries)
    return total / max_chars if max_chars else 0.0

def extract_key(entry: dict) -> str:
    """Extract a semantic key from entry content for deduplication."""
    content = entry.get("content", "").lower()
    keywords = ["nas", "windows", "hermes", "feishu", "memory", "ralph", "user"]
    for kw in keywords:
        if kw in content:
            return f"_{kw}_"
    return entry.get("category", "other")

# ──────────────────────────────────────────────
# CORE ENGINE
# ──────────────────────────────────────────────
class MemoryMaintainer:
    def __init__(self):
        self.memory = load_json(MEMORY_FILE)
        self.archive = load_json(ARCHIVE_FILE)
        self.stats = {
            "before_count": len(self.memory),
            "before_rate": get_usage_rate(self.memory),
            "archived": 0,
            "merged": 0,
            "cleared": 0,
        }

    # ── Scoring ──────────────────────────────
    def score_entry(self, entry: dict) -> float:
        now = time.time()
        last = entry.get("last_accessed", now)
        weight = entry.get("weight", 5)
        is_permanent = entry.get("is_permanent", False)
        if is_permanent:
            return 10.0
        recency = max(0.0, 1.0 - (now - last) / RETENTION_SECONDS)
        return weight * 0.5 + recency * 3.0 + min(entry.get("access_count", 0), 10) * 0.2

    # ── Cleanup ──────────────────────────────
    def execute_cleanup(self):
        log.info(f"Starting cleanup — usage: {self.stats['before_rate']:.1%}")
        keep = []
        for entry in self.memory:
            score = self.score_entry(entry)
            if score < 3.0:
                self.archive.append({
                    **entry,
                    "archived_at": datetime.utcnow().isoformat(),
                    "archive_reason": "low_weight_old"
                })
                self.stats["archived"] += 1
            else:
                keep.append(entry)
        self.memory = keep

    # ── Deduplication ────────────────────────
    def deduplicate_entries(self):
        seen = {}
        deduped = []
        for entry in self.memory:
            key = extract_key(entry)
            if key in seen:
                # Keep the newer one
                old = seen[key]
                if entry.get("last_accessed", 0) > old.get("last_accessed", 0):
                    deduped.remove(old)
                    deduped.append(entry)
                    seen[key] = entry
                self.stats["merged"] += 1
            else:
                seen[key] = entry
                deduped.append(entry)
        self.memory = deduped

    # ── Compression ─────────────────────────
    def compress_entries(self):
        for entry in self.memory:
            content = entry.get("content", "")
            # Strip outdated markers
            if "已修复" in content or "已完成" in content:
                entry["content"] = content.replace("已修复", "").replace("已完成", "").strip()
                self.stats["cleared"] += 1
            # Truncate if too long
            if len(entry["content"]) > 150:
                entry["content"] = entry["content"][:147] + "…"

    # ── Report ──────────────────────────────
    def generate_report(self) -> str:
        after_rate = get_usage_rate(self.memory)
        lines = [
            "### 🧠 记忆优化报告",
            "| 指标 | 优化前 | 优化后 | 改善 |",
            "|------|--------|--------|------|",
            f"| Memory 占用 | {self.stats['before_rate']:.0%} | {after_rate:.0%} | -{(self.stats['before_rate']-after_rate)*100:.0f}% |",
            f"| 条目数 | {self.stats['before_count']} | {len(self.memory)} | -{self.stats['before_count']-len(self.memory)} 条 |",
            f"| 归档数 | — | {self.stats['archived']} | +{self.stats['archived']} 条 |",
            f"| 合并数 | — | {self.stats['merged']} | -{self.stats['merged']} 条 |",
        ]
        return "\n".join(lines)

    # ── Persist ─────────────────────────────
    def save(self):
        save_json(MEMORY_FILE, self.memory)
        save_json(ARCHIVE_FILE, self.archive)
        log.info("Memory & Archive persisted.")

    # ── Public API ──────────────────────────
    def maintain(self) -> str:
        if get_usage_rate(self.memory) > THRESHOLD:
            self.execute_cleanup()
        self.deduplicate_entries()
        self.compress_entries()
        self.save()
        return self.generate_report()


# ──────────────────────────────────────────────
# ENTRYPOINT
# ──────────────────────────────────────────────
if __name__ == "__main__":
    maintainer = MemoryMaintainer()
    report = maintainer.maintain()
    print(report)
