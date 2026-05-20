# Copilot Instructions — agent-readiness

> Instructions for GitHub Copilot, Cursor, Claude Code, and all AI coding agents in this repo.

---

## Project

`agent-readiness` is the Agent Readiness Scanner — a deterministic Python CLI that checks whether
a repository is ready for AI coding agents. It has **zero runtime dependencies** and makes **no
network or LLM calls**.

---

## Hard Constraints

**Keep v0 deterministic.** The core scanner (`checks.py`) must remain pure file-system analysis.
Do not add LLM calls, network requests, or probabilistic logic to the check functions.

**Keep zero runtime dependencies.** `agent_readiness/` must import from the standard library only.
Dev dependencies (pytest) are fine. Production dependencies are not.

**Tests first.** Before adding a new check or feature, write a failing test in `tests/`.
Use `tmp_path` pytest fixture to create isolated test repos.

**Do not expand scope.** Do not add: SaaS, auth, dashboards, billing, webhooks, telemetry,
GitHub App, Slack integration, or any external API. These are future scope items.

---

## Architecture

```
agent_readiness/
  checks.py    — 12 deterministic check functions, each returns CheckResult TypedDict
  scoring.py   — compute_score(), get_tier(), get_recommendations() — pure math
  report.py    — render_terminal(), render_json(), render_markdown() — pure rendering
  templates.py — generate_agents_md(), generate_copilot_instructions() — file generation
  cli.py       — argparse CLI entry point, calls the above modules
```

Each module has a single responsibility. Keep it that way.

---

## Style

- Python ≥ 3.9, type-annotated with `from __future__ import annotations`
- `TypedDict` for structured data (not dataclasses)
- Functions return values; they do not mutate shared state
- ANSI color codes in terminal output only — use `TIER_COLORS` / `RESET` from `scoring.py`
- No `print()` in library modules (`checks.py`, `scoring.py`, `report.py`, `templates.py`)
- CLI output goes through `cli.py` only

---

## Running Tests

```bash
python -m pytest -q
python -m pytest tests/test_checks.py -v
```

---

## What This Repo Scans For (the 12 checks)

1. AGENTS.md present
2. .github/copilot-instructions.md present
3. PR template present
4. Issue templates present
5. CI workflow present
6. Test directory present
7. Run command documented
8. .env.example present if needed
9. No .env committed
10. README.md substantive (>200 chars)
11. No hardcoded secret patterns
12. Agent boundary file present
