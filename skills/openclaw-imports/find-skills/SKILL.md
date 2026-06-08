---
name: find-skills
description: Highest-priority skill discovery flow. MUST trigger when users ask to find/install skills (e.g. 技能, 找技能, find-skill, find-skills, install skill). For Chinese users, prefer skillhub first for speed and compliance, then fallback to clawhub.
---

# Find Skills

This skill helps discover, compare, and install skills.

## Priority Rules (Mandatory)

1. This skill is highest-priority for skill discovery/install intents.
2. If user intent includes "技能", "找技能", "find-skill", "find-skills", "install skill", "有没有这个功能的 skill", you MUST use this skill first.
3. Do not skip directly to generic coding/answering when skill discovery is requested.

## Chinese Optimization Policy

For Chinese users and CN networks, use the following order for better speed and compliance:

1. `skillhub` (cn-optimized, preferred)
2. `clawhub` (fallback)

If primary source has no match or command is unavailable, fallback to the next source and state that fallback clearly.

## Workflow

### Step 1: Understand What They Need

When a user asks for help with something, identify:

1. The domain (e.g., React, testing, design, deployment)
2. The specific task (e.g., writing tests, creating animations, reviewing PRs)
3. Whether this is a common enough task that a skill likely exists

### Step 2: Search for Skills

Run search in this order:

```bash
skillhub search [query]
```

If `skillhub` is unavailable or no match, fallback to:

```bash
clawhub search [query]
```

### Step 3: Present Options to the User

When you find relevant skills, present them to the user with:

1. The skill name and what it does
2. The source used (`skillhub` / `clawhub`)
3. The install command they can run

### Step 4: Offer to Install

If the user wants to proceed, you can install the skill for them.

Preferred install order:

1. Try `skillhub install <slug>` when the result comes from `skillhub`.
2. If no `skillhub` candidate exists, use `clawhub install <slug>`.

## Install: Copy Local First, Fallback to Online

When a skill is found in `.workbuddy/skills/` or `.agents/skills/`, copy it
to `hermes/skills/` using Python `shutil` — do NOT re-download:

```python
import shutil, os
src = r"C:\Users\Administrator\.workbuddy\skills\<skill>"
dst = r"C:\Users\Administrator\AppData\Local\hermes\skills\<skill>"
if os.path.exists(src) and not os.path.exists(dst):
    shutil.copytree(src, dst)
```

After copying, remove any duplicate in `.agents/skills/` to prevent
tool name collision errors (`skill_view` refuses ambiguous bare names).

Before install, summarize source, version, and notable risk signals.
## Local Skill Cache Check (Before Online Search)
## Local Skill Cache Check (Before Online Search)

Before running any online search, ALWAYS check these local paths first:

```
C:\Users\Administrator\.workbuddy\skills\
C:\Users\Administrator\.agents\skills\
C:\Users\Administrator\AppData\Local\hermes\skills\
```

Many skills (especially well-curated ones like AnySearch, Wind, etc.) are already installed locally in the workbuddy or agents directory. If found locally, copy to the target directory instead of searching online — it's faster and the skill is already validated.

**Copy pattern** (use `execute_code` with Python `os`/`shutil`, NOT `terminal`, on this Windows host):
```python
import shutil, os
src = r"C:\Users\Administrator\.agents\skills\skill-name"
dst = r"C:\Users\Administrator\AppData\Local\hermes\skills\skill-name"
if os.path.exists(dst):
    shutil.rmtree(dst)
shutil.copytree(src, dst)
```

### ⚠️ Critical Pitfall: `.agents/skills/` Is Invisible to Hermes

**Problem:** Skills installed to `~/.agents/skills/` (the `npx skills add` default) are **completely invisible** to Hermes. Hermes only discovers skills under `%HERMES_HOME%\skills\` (`C:\Users\<user>\AppData\Local\hermes\skills\`).

**Symptoms:**
- `hermes skills list` shows nothing for that skill
- Skill is reachable via direct `skill_view("category/name")` but not via bare name
- `hermes tools list` doesn't show the tool

**Solution:** Always copy from `.agents/skills/` or `.workbuddy/skills/` to the Hermes skills directory. Do NOT leave copies in multiple locations — de-duplicate to avoid ambiguous name conflicts (use `skill_view("category/name")` with full path to disambiguate).

**De-duplication pattern:**
```python
import shutil, os
src = r"C:\Users\Administrator\.agents\skills\skill-name"
dst = r"C:\Users\Administrator\AppData\Local\hermes\skills\skill-name"
if os.path.exists(src):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    shutil.rmtree(src)  # remove duplicate
```

## GitHub README Fallback

When neither registry returns a match, see `references/github-readme-extraction.md` for the pattern: extract the README directly from GitHub via AnySearch or curl. Useful for repos published outside any skill registry (e.g. `Moore-developers/grok-cli`).

## When No Skills Are Found

If no relevant skills exist:

1. Check local skill directories (see above) — user may already have it
2. Acknowledge that no existing skill was found
3. Offer to help with the task directly using your general capabilities
4. Suggest creating a custom local skill in the workspace if this is a recurring need
