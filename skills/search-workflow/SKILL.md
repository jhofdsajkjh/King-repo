---
name: search-workflow
description: Consolidated search utilities and frameworks.
---

# Search Workflow Umbrella

## anysearch
Description: Real-time search engine supporting web search, vertical domains, and content extraction.

**Important (2026-05-29):** AnySearch works purely as a Hermes skill (installed under `openclaw-imports` category). There is NO separate Hermes plugin for AnySearch. The skill includes CLI scripts (`scripts/anysearch_cli.py`) and a pre-configured API key. When user asks "is the plugin installed?", clarify that AnySearch is skill-only — `hermes plugins list` will show nothing, but that's expected and does not affect functionality.

**User preference:** AnySearch is the user's default search tool. All search tasks should prioritize AnySearch unless user specifies otherwise.

## search-skill-system
Description: Standardized search enhancement framework using SkillBank, Select-Read-Act paradigm.
