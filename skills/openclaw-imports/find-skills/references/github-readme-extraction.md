# Skill Discovery: Sources & Fallback Patterns

## Skill Sources (in priority order)

1. **Local cache** — Always check first before going online:
   - `C:\Users\Administrator\.workbuddy\skills\`
   - `C:\Users\Administrator\.agents\skills\`
   - `C:\Users\Administrator\AppData\Local\hemes\skills\`
   Copy with `shutil.copytree(src, dst)` (Python, not terminal on Windows).

2. **skillhub** — CN-optimized registry, try first.
3. **clawhub** — Fallback when skillhub unavailable or no match.
4. **GitHub README** — When neither registry yields results, search GitHub directly for the repo and extract the README via AnySearch or curl. This works even for skills not published to any registry (e.g. `Moore-developers/grok-cli`).

## GitHub README Extraction Workflow

When you have a GitHub repo URL and want to get the full skill documentation:

```bash
# Via AnySearch extract (works for rendered HTML pages)
python C:/Users/Administrator/.agents/skills/anysearch/scripts/anysearch_cli.py extract <github-raw-url>

# For raw content (raw.githubusercontent.com) — AnySearch may reject as "text/plain"
# Fall back to curl or fetch if AnySearch fails on raw files
```

**Known limitations:**
- WeChat articles (`mp.weixin.qq.com`) — blocked by login gate, even with AnySearch.
- Empty GitHub Pages subpaths — some demo pages return minimal content.
- `text/plain` rejection — AnySearch only supports `text/html`. If a raw file is rejected, try the rendered GitHub page URL instead.

## grok-cli Case Study

- Repo: `Moore-developers/grok-cli`
- No skill registry entry found → fell back to GitHub README extraction.
- Both English (`README.md`) and Chinese (`README.zh-CN.md`) versions available.
- Chinese README confirms: OAuth login via X Premium+/SuperGrok, no separate API key needed.
- Skill install path: `npx --yes skills add Moore-developers/grok-cli --skill grok-cli --global --yes`
