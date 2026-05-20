# Changelog

All notable changes to Agent Readiness Scanner are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] — 2026-05-20

### Added

- **12-check scanner** covering: AGENTS.md, copilot instructions, PR template, issue templates,
  CI workflow, test directory, run command, .env.example, no .env committed, README quality,
  no hardcoded secrets, and agent boundary file
- **CLI entry point** `agent-scan [path]` via `pip install agent-readiness`
- **Three output modes**: `--output terminal` (default), `--output json`, `--output markdown`
- **File generation**: `--generate` flag creates missing `AGENTS.md` and
  `.github/copilot-instructions.md` from static templates; never overwrites existing files
- **CI gate**: `--fail-under N` exits with code 1 if score is below threshold
- **`--verbose` flag**: shows evidence and fix recommendation for every check
- **`--no-color` flag**: disables ANSI terminal colors
- **`NO_COLOR` env var**: respects [no-color.org](https://no-color.org) standard
- **`--version` flag**: prints `agent-scan 0.1.0`
- **`python -m agent_readiness`** module entry point
- **GitHub Action** `.github/workflows/test.yml` covering Python 3.9–3.12
- **AGENTS.md** and **`.github/copilot-instructions.md`** operational governance for this repo
- **99 unit tests** covering all checks, scoring math, template generation, and CLI behavior
- **Self-scan score**: 100/100 GREEN on own repo

### Scoring

- Total weight: 27 across 12 checks
- Pass = full weight, warn = half weight, fail = zero weight
- Score = (earned / 27) × 100
- Tiers: GREEN ≥ 85, YELLOW 70–84, ORANGE 50–69, RED < 50

### Known Limitations

- Secret detection is heuristic (4 patterns). Not a replacement for truffleHog or gitleaks.
  See [SECURITY.md](SECURITY.md).
- No score history persistence (planned for v0.2).
- No `--config` file for custom check weights (planned for v0.3).

---

## Roadmap

| Version | Target |
|---|---|
| v0.2 | Score history (local file), `--no-color` improvement, PyPI listing |
| v0.3 | GitHub Actions Marketplace listing |
| v0.4 | `--config` for custom check weights |
| future | GitHub App with org-level dashboard |
| future | Token Burn Firewall module |
| future | Repo Red Cell Bot module |
