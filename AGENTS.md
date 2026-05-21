# AGENTS.md — agent-readiness

> Operational guidance for AI coding agents working in this repository.
> Applies to: Cursor, Claude Code, GitHub Copilot, Codex, and local agents.

---

## Project Purpose

`agent-readiness` is the Agent Readiness Scanner — a deterministic Python CLI that checks whether
a repository is ready for AI coding agents. It scans for governance files, CI configuration,
test coverage signals, documentation, and safety patterns.

The product goal is a self-serve, hands-off tool. It must require no consulting, no manual
intervention, and no external services to reach first value.

**Current version: v0.2.0 — CLI only.**

v0.2 priority is bounded: critical-failure visibility and positioning clarity
only. Do not expand the product while working this release.

---

## Allowed Changes

Agents are explicitly permitted to:

- Fix bugs in existing check functions when a test identifies a clear failure
- Add new tests to `tests/` using the `tmp_path` pytest fixture
- Improve docstrings, type annotations, and inline comments
- Refactor within a single module without changing public function signatures
- Fix linter warnings (ruff, pyright) without changing behavior
- Update the README if user-facing behavior changes
- Add new check functions to `checks.py` if they follow the `CheckResult` TypedDict contract

---

## Forbidden Changes

Agents **must not** make the following changes without explicit operator approval:

- Add any runtime dependency to `pyproject.toml`
- Add network calls, HTTP requests, or socket operations of any kind
- Add LLM API calls, model loading, or AI inference
- Add telemetry, analytics, crash reporting, or usage tracking
- Modify `.github/workflows/test.yml` (CI is operator-controlled)
- Remove or rename the `agent-scan` CLI entry point
- Change the `CheckResult` TypedDict structure in a breaking way
- Add SaaS, auth, dashboard, billing, or GitHub App features
- Expand scope to include Token Burn Firewall or Repo Red Cell Bot

Before adding any new feature, check `docs/LAUNCH_LOG.md` and the latest
`reports/OPS_REPORT_*.md`. If launch feedback does not support the feature,
do not build it without explicit operator approval.

Future agents should read `docs/AGENT_INDEX.md` and `docs/REPO_MAP.md` before
modifying this repo. Those files explain how to classify the project and where
to make safe changes.

---

## Test Commands

```bash
# Run the full test suite (required before any commit)
python -m pytest -q

# Run tests with verbose output
python -m pytest -v

# Run a specific test file
python -m pytest tests/test_checks.py -v

# Scan this repo (smoke test the CLI)
python -m agent_readiness.cli . --output terminal
python -m agent_readiness.cli . --output terminal --no-color
python -m agent_readiness.cli . --output json
python -m agent_readiness.cli . --output markdown
python -m agent_readiness.cli . --generate

# If the entry point is installed:
agent-scan . --output terminal
```

---

## Style Rules

- Python ≥ 3.9 with `from __future__ import annotations`
- `TypedDict` for structured return values — not dataclasses
- No `print()` in library modules; only in `cli.py`
- No global mutable state
- Keep functions under 50 lines where possible; split if longer
- All public functions require docstrings
- ANSI color output: use `TIER_COLORS` and `RESET` from `scoring.py`

---

## Scope Boundaries

**In scope for v0:**

- `agent_readiness/` Python package (checks, scoring, report, templates, cli)
- `tests/` test suite
- `templates/` static template files
- README, AGENTS.md, `.github/` governance files

**In scope for v0.2 only:**

- Critical-failure visibility for committed `.env` and hardcoded secret-pattern findings
- README positioning as an agent preflight / runway check
- Agent-facing doctrine updates
- Roadmap and build report documentation

**Out of scope (do not build):**

- SaaS dashboard or web UI
- GitHub App or OAuth integration
- Billing or Stripe integration
- External database or persistent storage
- Token Burn Firewall module
- Repo Red Cell Bot module
- Slack, Discord, or email integrations
- Multi-language non-Python implementations

---

## Guardrails

1. If you are unsure whether a change is in scope, **do not make it**. Open an issue instead.
2. If a test fails after your change, fix the code — do not weaken or delete the test.
3. If you add a new check, it must return a `CheckResult` TypedDict with all required fields.
4. Do not add `# type: ignore` or `# noqa` without a comment explaining why.
5. Do not commit `AGENT_READINESS.md` — it is a generated artifact.
6. Do not commit `.env`, API keys, tokens, or any credentials.
7. The scanner must be runnable offline and cost nothing per invocation.
8. Before modifying this repo, run tests first if practical; if not practical,
   explain why before editing.
9. Do not expand into SaaS, dashboard, auth, billing, LLM, or hosted paths
   without explicit operator approval.

---

## Architecture Reference

```
agent_readiness/
  __init__.py      — package exports and version
  checks.py        — 12 deterministic check functions → CheckResult
  scoring.py       — compute_score(), get_tier(), get_recommendations(), get_critical_failures()
  report.py        — render_terminal(), render_json(), render_markdown()
  templates.py     — generate_agents_md(), generate_copilot_instructions()
  cli.py           — argparse CLI, orchestrates the above
  __main__.py      — python -m agent_readiness entry point

templates/
  AGENTS.md.template
  copilot-instructions.md.template

tests/
  test_checks.py
  test_scoring.py
  test_generation.py
```

Data flow: `cli.py` → `checks.py` → `scoring.py` → `report.py` → stdout/disk

---

*This file was written by the project operator. Do not modify it without approval.*
