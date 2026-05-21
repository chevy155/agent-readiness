# Repo Map

Fast orientation for future coding agents and human contributors.

---

## Where Agents Should Start

1. Read `docs/AGENT_INDEX.md`
2. Read this file
3. Run `python -m pytest -q`
4. Run `python -m agent_readiness.cli . --output terminal --no-color`
5. Read `AGENTS.md`
6. Only then propose changes

---

## Core Modules

| Path | Role |
|---|---|
| `agent_readiness/checks.py` | 12 deterministic file-system checks |
| `agent_readiness/scoring.py` | Score math, tier mapping, recommendations, critical failure helper |
| `agent_readiness/report.py` | Terminal, JSON, and Markdown rendering |
| `agent_readiness/templates.py` | Starter `AGENTS.md` and Copilot instruction generation |
| `agent_readiness/cli.py` | CLI orchestration and argument parsing |
| `agent_readiness/__init__.py` | Package version and public exports |

---

## Test Modules

| Path | Role |
|---|---|
| `tests/test_checks.py` | Individual check behavior |
| `tests/test_scoring.py` | Score, tier, recommendations, critical failure helper |
| `tests/test_generation.py` | Rendering, CLI behavior, version/no-color, critical failure output |
| `tests/test_ops_agent.py` | Owner-only ops agent and feedback synthesis |
| `tests/test_traffic_report.py` | GitHub traffic report formatting |
| `tests/fixtures/` | Five local fixture repos for validation |

---

## Scripts

| Path | Role |
|---|---|
| `scripts/validate_fixtures.py` | Scans local fixture repos and writes validation report |
| `scripts/github_traffic_report.py` | Owner-only GitHub traffic report via `gh api` |
| `scripts/ops_agent.py` | Owner-only post-launch feedback radar |
| `scripts/feedback_synthesizer.py` | Pure keyword/category/backlog helpers |

---

## Docs

| Path | Role |
|---|---|
| `README.md` | Primary human entry point |
| `AGENTS.md` | Operating contract for future coding agents |
| `docs/AGENT_DISCOVERY.md` | Machine-readable repo description |
| `docs/AGENT_INDEX.md` | Concise classification index |
| `docs/AGENT_USE_CASES.md` | Human and agent workflow scenarios |
| `docs/AGENT_PROMPTS.md` | Prompts to use after scanning a repo |
| `docs/WHY_DETERMINISTIC.md` | Why the core scan avoids LLM calls |
| `docs/COMPETITIVE_POSITIONING.md` | Comparison against adjacent tools |
| `docs/ROADMAP.md` | Built, next likely, and future-only modules |

---

## Reports

| Path | Role |
|---|---|
| `AGENT_READINESS.md` | Generated self-scan report |
| `reports/EXTERNAL_REPO_VALIDATION.md` | Fixture validation output |
| `reports/V0_2_BUILD_REPORT.md` | v0.2 implementation report |
| `reports/OPS_REPORT_*.md` | Owner-only launch/feedback reports |

---

## Files Not to Modify Casually

- `.github/workflows/test.yml` - CI is operator-controlled
- `pyproject.toml` - package metadata and entry point
- `agent_readiness/checks.py` - changes affect score behavior
- `agent_readiness/scoring.py` - changes affect score/tier/critical semantics
- `tests/fixtures/` - fixture changes must preserve documented expected tiers
- `reports/BUILD_REPORT.md` - historical Day 1 artifact
- `reports/MARKETING_AGENT_DISCOVERY_REPORT.md` - historical launch artifact

---

## Commands to Verify Changes

```bash
python -m pytest -q
python -m agent_readiness.cli . --output terminal --no-color
python -m agent_readiness.cli . --output json
python -m agent_readiness.cli . --output markdown
python scripts/validate_fixtures.py
python scripts/ops_agent.py --no-gh
```

If the installed `agent-scan` entry point is available:

```bash
agent-scan . --output terminal --no-color
```

