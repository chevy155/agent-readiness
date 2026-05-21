# Changelog

All notable changes to Agent Readiness Scanner are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.3.0] — 2026-05-21

### Added

- **Agent Workspace Readiness expansion** while preserving deterministic local scanning.
- **17 checks total** (up from 12).
- **Cursor rules detection** via `.cursorrules` or `.cursor/rules/*`.
- **Workspace continuity checks** for handoff/current-state docs and substantive handoff content.
- **Explicit test command detection** across Makefile/justfile/package.json/pyproject signals.
- **Env contract pairing check** with stronger safety semantics:
  - fail when `.env`-like files exist and `.gitignore` lacks `.env` protection
  - warn when ignore is correct but no env example/template exists
  - pass when both ignore + example/template are present
- **New fixture repos 06–09** for workspace-strong, cursor-rules-missing, handoff-missing, and env-contract-broken scenarios.

### Changed

- Version bumped to `0.3.0`.
- Total scoring weight increased to **36** with existing weighted normalization preserved.
- Fixture validation and docs updated to reflect workspace-readiness semantics.
- Test suite expanded to **218 passing tests**.

### Unchanged

- No runtime dependencies.
- No LLM calls.
- No network calls in scanner core.
- No telemetry.
- Critical-failure set remains unchanged (`no_env_committed`, `no_secrets`).

---

## [0.2.0] — 2026-05-20

### Added

- **Critical failures banner** in terminal output for committed `.env` files and hardcoded secret-pattern findings.
- **Critical failures section** in Markdown reports.
- **JSON critical fields**:
  - `critical_failures_present`
  - `critical_failures`
- **Agent preflight positioning** in README and marketing docs.
- **Claude / Cursor / Copilot / Codex comparison** explaining that the scanner is a deterministic preflight layer before agents modify a repo.
- **Roadmap** at `docs/ROADMAP.md`.
- **v0.2 build report** at `reports/V0_2_BUILD_REPORT.md`.

### Changed

- Version bumped to `0.2.0`.
- Secret-pattern detection now catches modern `sk-...` variants with underscores/hyphens.
- Fixture validation now reports critical failures separately from score/tier.
- README now links the Python badge to `pyproject.toml` until PyPI is live.

### Unchanged

- Score formula remains `(earned weight / 27) × 100`.
- No runtime dependencies.
- No network calls in the scanner.
- No LLM calls.
- No telemetry.

---

## [0.1.0] — 2026-05-20

### Added

- **12-check scanner** covering: AGENTS.md, copilot instructions, PR template, issue templates,
  CI workflow, test directory, run command, .env.example, no .env committed, README quality,
  no hardcoded secrets, and agent boundary file
- **CLI entry point** `agent-scan [path]` — install from source with `pip install -e .` (PyPI publish pending)
- **Three output modes**: `--output terminal` (default), `--output json`, `--output markdown`
- **File generation**: `--generate` flag creates missing `AGENTS.md` and
  `.github/copilot-instructions.md` from static templates; never overwrites existing files
- **CI gate**: `--fail-under N` exits with code 1 if score is below threshold
- **`--verbose` flag**: shows evidence and fix recommendation for every check
- **`--no-color` flag**: disables ANSI terminal colors
- **`NO_COLOR` env var**: respects [no-color.org](https://no-color.org) standard
- **`--version` flag**: prints the package version
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

- Secret detection is heuristic. Not a replacement for truffleHog or gitleaks.
  See [SECURITY.md](SECURITY.md).
- No score history persistence.
- No `--config` file for custom check weights (planned for v0.3).

---

## Roadmap

| Version | Target |
|---|---|
| v0.2 | Critical failures banner, positioning upgrade, agent preflight doctrine |
| next likely | PyPI publish, GitHub Action polish, improved scoring model, more secret patterns |
| future | Config file support |
| future | GitHub App with org-level dashboard |
| future | Token Burn Firewall module |
| future | Repo Red Cell Bot module |
