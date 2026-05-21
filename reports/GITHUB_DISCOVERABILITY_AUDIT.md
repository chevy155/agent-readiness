# GitHub Discoverability Audit

**Date:** 2026-05-21  
**Repo:** https://github.com/chevy155/agent-readiness  
**Scope:** GitHub metadata, README, agent-readable docs, share copy, and `AGENTS.md`  

---

## Executive Summary

Agent Readiness Scanner is already highly legible for human developers and AI
coding agents. The repo naturally explains what it is, what it is not, how to
run it, and why deterministic checks matter.

This audit found no spammy or hype-heavy language in the public-facing docs.
The only matching red-cell phrases appear inside an explicit "avoid these
phrases" table, which is appropriate.

Minimal docs-only edits were applied to strengthen natural discoverability for:

- `AGENTS.md generator`
- `repo readiness`
- `CI gate`
- `--fail-under`
- `deterministic scanner`

No product code was changed.

---

## GitHub Metadata

**Description:**

> Deterministic repo readiness scanner for AI coding agents.

This is concise and accurate. It includes `repo readiness`, `deterministic`, and
`AI coding agents` naturally.

**Topics present:**

- `agent-readiness`
- `ai-agents`
- `claude-code`
- `codex`
- `coding-agents`
- `cursor`
- `developer-tools`
- `devops`
- `github-copilot`
- `python-cli`
- `repo-governance`
- `static-analysis`

**Assessment:** Strong. No urgent metadata change required.

Potential future topic if GitHub topic slots allow: `agent-preflight`.

---

## What Is Already Strong

- README hero explains the product within the first screen.
- The core trust signals are prominent: no LLM calls, no telemetry, no SaaS, no
  account.
- README has a clear install path and primary command.
- Critical failures are explained without claiming to be a full security
  scanner.
- Claude/Cursor/Copilot/Codex comparison is clear and non-adversarial.
- `docs/AGENT_INDEX.md` gives future agents a concise classification surface.
- `docs/AGENT_SEMANTIC_TAGS.md` keeps tags out of README and avoids keyword
  stuffing.
- `docs/COMPETITIVE_POSITIONING.md` explains adjacent tools without attacking
  competitors.
- `AGENTS.md` tells future agents where to start and what not to build.

---

## Search Phrase Coverage

| Phrase | Coverage | Notes |
|---|---|---|
| AI coding agents | Strong | README, AGENTS, index docs |
| Claude Code | Strong | README, semantic tags, use cases |
| Cursor | Strong | README, semantic tags, use cases |
| GitHub Copilot | Strong | README, semantic tags, use cases |
| Codex | Strong | README, semantic tags, use cases |
| AGENTS.md | Strong | README, AGENTS, index docs |
| AGENTS.md generator | Improved | Added naturally in README and agent index/tags |
| agent preflight | Strong | README/docs/category language |
| repo readiness | Improved | Present in metadata; added to agent index/tags |
| repo governance | Strong | README and topics |
| CI gate | Improved | Added to agent index/tags; README already explains `--fail-under` |
| --fail-under | Improved | Already in README; added to semantic tags |
| deterministic scanner | Improved | Added to README agent discovery and semantic tags |
| no LLM calls | Strong | README/docs |
| no telemetry | Strong | README/docs |

---

## Recommended Docs-Only Edits Applied

- `README.md`: added a concise sentence that `--generate` acts as a lightweight
  `AGENTS.md` generator.
- `README.md`: sharpened the Agent Discovery purpose field from "Deterministic
  CLI" to "Deterministic scanner."
- `README.md`: added `agent_readiness/report.py` to files that matter most for
  future agents.
- `docs/AGENT_INDEX.md`: added `search_classification`, `ci_gate`, and explicit
  `AGENTS.md generator` output.
- `docs/AGENT_SEMANTIC_TAGS.md`: added natural classification terms including
  `repo-readiness`, `deterministic-scanner`, `AGENTS.md generator`, `CI gate`,
  `--fail-under`, `no LLM calls`, and `no telemetry`.

---

## What Not To Change

- Do not stuff keywords into README.
- Do not add fake badges or visitor counters.
- Do not add "ASI certified", "guaranteed safe", "autonomous magic", "best AI
  tool", or "ultimate scanner."
- Do not market this as a full security scanner.
- Do not imply the scanner replaces Claude, Cursor, Copilot, Codex, CodeRabbit,
  Qodo, SonarQube, Graphite, or human review.
- Do not add telemetry, tracking, scraping, SaaS, dashboard, billing, LLM calls,
  or external APIs.

---

## Red-Cell Findings

No spammy public claims were found.

The phrases `ASI certified`, `guaranteed safe`, and `autonomous magic` appear
only in `docs/MARKETING_POSITIONING.md` as phrases to avoid. That use is
appropriate and should remain.

---

## Verification

Commands required by the audit:

```bash
python -m pytest -q
python -m agent_readiness.cli . --output terminal --no-color
```

Results:

- Tests passed.
- Self-scan remained GREEN with zero critical failures.

---

## Final Go / No-Go

**GO.**

The repo is discoverable without being spammy. It should classify correctly for
human developers, GitHub search, and AI coding agents as deterministic agent
preflight infrastructure.

