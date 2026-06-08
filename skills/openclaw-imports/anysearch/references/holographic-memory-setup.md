# Holographic Memory Provider Setup

## Why Holographic
- Pure local, no API key required
- Supports `local` mode out of the box
- Unlike honcho/hindsight which require API keys even in "local" mode

## Configuration
```
hermes memory setup holographic
```

This sets:
- `memory.provider: holographic`
- `memory.providers.holographic: { mode: local }`

## Verification
```
hermes memory status
```
Should show: `holographic: available ✓ (mode: local)`

## Session Note (2026-05-29)
User chose holographic after honcho required API key despite claiming local support.
Holographic activated successfully with `available` status.
