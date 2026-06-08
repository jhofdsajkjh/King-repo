---
name: system-updates-under-constraints
category: devops
version: "2026.6.5"
description: Systematic approach to updating software (Hermes, Clash, etc.) when facing network, permission, and format constraints.
tags:
  - maintenance
  - updates
  - troubleshooting
  - constraints
  - hermes
  - clash
---

# System Updates Under Constraints

Use this skill when updating software in constrained environments (no sudo, limited network, encrypted configs, externally-managed Python).

## When to Trigger

- User asks to "update Hermes", "update Clash", or "check for updates"
- System shows "up to date" but user wants verification
- Download attempts fail or timeout
- Subscription URLs return encrypted/obfuscated data

## Standard Workflow

### 1. Verify Current Version

```bash
hermes version
clash -v  # or clash-meta -v
```

**Cross-check with GitHub API:**
- Hermes: `https://api.github.com/repos/NousResearch/hermes-agent/releases/latest`
- Clash: `https://api.github.com/repos/MetaCubeX/mihomo/releases/latest`

### 2. If Already Up to Date

- Confirm with user — no action needed
- Document: "System is current (X vs latest Y)"

### 3. If Updates Available, Handle Constraints

| Constraint | Solution |
|------------|----------|
| No `curl`/`wget` | Use Python `urllib.request` |
| No `sudo`/apt | Use venv or pipx (if available); fallback to `/tmp` downloads |
| Network timeouts | Retry with longer timeout; use hermes `execute_code` for retries |
| No venv support | Try `python3 -m venv` first; if missing, check `python3-venv` package |
| Encrypted subscriptions | Save raw file, let Clash Meta parse it; extract ports from running instance |

### 4. Clash-Specific Tips

- Subscription URLs often return base64-encoded + gzipped + encrypted configs
- Save raw to `/tmp/clash-sub.yaml`, let `clash` binary parse it
- Extract proxy info only if config is plain YAML (rare for commercial subscriptions)

### 5. Verify Installation

After update:
```bash
hermes version
clash -v
hermes status
```

## Common Pitfalls

❌ **Assuming `pip install hermes-agent` works**  
→ System may be externally-managed (PEP 668)

❌ **Assuming all subscriptions are plain YAML**  
→ Many commercial subscriptions are obfuscated

❌ **Assuming latest GitHub version = latest installed**  
→ Check local version first, GitHub API second

✅ **Best practice**: Save subscription file → let Clash parse it → extract ports from `external-controller` or running process

## Example: Verify Hermes Update

```python
# In execute_code
import urllib.request, json
url = "https://api.github.com/repos/NousResearch/hermes-agent/releases/latest"
with urllib.request.urlopen(url) as r:
    data = json.loads(r.read().decode())
print(f"Latest: {data['tag_name']}")
# Compare with `hermes version` output
```

## Files to Remember

| File | Purpose |
|------|---------|
| `/opt/hermes/.venv/` | Hermes virtual environment |
| `/tmp/clash-sub.yaml` | Save Clash subscription raw data |
| `/usr/local/bin/hermes` | System-wide Hermes CLI (shebang to Python) |

## Post-Update Actions

- Run `hermes status` to verify
- If Clash was updated, restart with `hermes gateway restart`
- Confirm proxy ports via `ps aux | grep clash`