# Roadmap

Agent Readiness Scanner is the deterministic runway check before AI coding
agents touch a repo.

This roadmap keeps future ideas organized without building them early.

---

## v0.1 — Initial CLI

- Deterministic Python CLI
- 12 repo-readiness checks
- 0–100 score with GREEN / YELLOW / ORANGE / RED tiers
- Terminal, JSON, and Markdown reports
- `--generate` for starter `AGENTS.md` and GitHub Copilot instructions
- `--fail-under` for CI gating
- Fixture validation
- GitHub-ready docs, templates, and CI

---

## v0.2 — Critical Failure Visibility

- Critical failures banner in terminal output
- Critical failures section in Markdown output
- `critical_failures_present` and `critical_failures[]` in JSON output
- Critical checks:
  - `no_env_committed`
  - `no_secrets`
- README positioning upgrade
- Agent preflight doctrine
- Claude / Cursor / Copilot / Codex comparison
- v0.2 build report

The score formula is unchanged. Critical failures are a visibility layer so
serious blockers cannot hide inside a decent numeric score.

---

## Next Likely

- PyPI publish
- GitHub Action polish
- README badge refresh after PyPI publish
- Improved scoring model
- More secret patterns
- Config file support

These are candidate v0.3/v0.4 items. They should be selected from real feedback,
not built speculatively.

---

## Future Only

- Token Burn Firewall
- Repo Red Cell Bot
- Hosted dashboard
- Org-level scan history

These are not built yet. Do not add SaaS, billing, auth, dashboards, background
jobs, telemetry, or external tracking without explicit operator approval.

---

## Operating Rule

Structure before autonomy.

The scanner should stay:

- Deterministic
- Local-first
- CI-ready
- Model-agnostic
- Zero telemetry
- Zero LLM calls in the core scan

