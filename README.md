# Agent Readiness Scanner

**The deterministic runway check before AI coding agents touch your repo.**

[![CI](https://github.com/chevy155/agent-readiness/actions/workflows/test.yml/badge.svg)](https://github.com/chevy155/agent-readiness/actions/workflows/test.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://github.com/chevy155/agent-readiness/blob/main/pyproject.toml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/chevy155/agent-readiness/blob/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/agent-readiness-cli.svg)](https://pypi.org/project/agent-readiness-cli/)

Claude, Cursor, Copilot, Codex, and local agents can help modify a repo.
Agent Readiness Scanner tells you whether the repo is structured enough before
those agents touch it.

It runs locally, checks 17 repo-governance signals, returns a **0–100 readiness
score**, and now surfaces **critical failures** separately so serious issues
cannot hide inside a decent score.

Output: terminal, JSON, or Markdown. Trust signal: deterministic checks, no LLM
calls, no telemetry, no SaaS, no account.

```bash
pip install agent-readiness-cli
agent-scan .
```

Or install from source:

```bash
git clone https://github.com/chevy155/agent-readiness.git
cd agent-readiness
pip install -e .
agent-scan .
```

---

## Why This Exists

**Humans can infer missing context. Agents cannot.**

**Agents are powerful, but they need a runway. This tool checks the runway.**

Most repos work fine for human developers. But AI coding agents operate differently. They need:

- A test suite they can run to verify changes
- Run commands documented somewhere they can find
- CI that gives them pass/fail feedback
- `AGENTS.md` telling them what is in-scope and what is forbidden
- Copilot instructions explaining style and conventions
- `.env` patterns handled safely so they don't expose secrets
- PR and issue templates so their outputs are structured
- An agent boundary file so they know what paths are off-limits

Without this structure, agents burn tokens, make bad changes, and erode trust.

`agent-scan` gives your repo a **0–100 readiness score** in under 3 seconds — then generates the missing files.

**No LLM calls. No telemetry. No SaaS. No account. Just a local scan.**

---

## Why Not Just Ask Claude, Cursor, Copilot, or Codex?

Claude, Cursor, Copilot, Codex, and local agents can help inspect or improve a
repo. Agent Readiness Scanner is different: it is a deterministic preflight
check before those agents touch the repo.

**Code review checks the change. Agent Readiness checks whether the repo can
safely receive an agent in the first place.**

This is not a replacement for AI coding tools. It is the runway inspection
before using them:

- Repeatable: same repo, same score, every run
- CI-compatible: use `--fail-under` to gate agent readiness
- Model-agnostic: works before Claude, Cursor, Copilot, Codex, or local agents
- Zero LLM calls: no tokens, no API keys, no inference
- Zero telemetry: the scanner does not phone home

---

## Built For

- Developers adopting **Cursor, GitHub Copilot, Claude Code, or Codex**
- AI-agent workflow builders who need repos with clear operating boundaries
- Engineering teams running autonomous coding experiments
- Dev-tool founders and platform engineers who want governance before autonomy
- Local-agent users (LM Studio, Ollama, llama.cpp) who need repo structure that works offline
- Anyone who has had an agent make a mess and wants to prevent the next one

---

## Quick Install

```bash
pip install agent-readiness-cli
```

For development (clone and install with test dependencies):

```bash
git clone https://github.com/chevy155/agent-readiness.git
cd agent-readiness
pip install -e ".[dev]"
```

---

## Quick Usage

```bash
# Scan current directory
agent-scan .

# Scan a specific path
agent-scan /path/to/my-project

# JSON output (for CI or scripting)
agent-scan . --output json

# Write AGENT_READINESS.md to the repo
agent-scan . --output markdown

# Generate missing governance files (never overwrites)
agent-scan . --generate

# Fail CI if score drops below 70
agent-scan . --fail-under 70

# Clean output for pipes and logs
agent-scan . --no-color

# Show version
agent-scan --version
```

---

## Example Output

```
──────────────────────────────────────────────────────────────
  Agent Readiness Scanner  v0.3.0
──────────────────────────────────────────────────────────────
  Repo   : /my-project
  Score  : 83 / 100
  Status : YELLOW  —  Mostly Ready
  Critical failures: 0
──────────────────────────────────────────────────────────────

  Check                                      Status  Wt
  ─────────────────────────────────────────────────────
  AGENTS.md present                          ✗ FAIL  3
  .github/copilot-instructions.md present    ✗ FAIL  2
  PR template present                        ✓ PASS  2
  Issue templates present                    ✓ PASS  1
  CI workflow present                        ✓ PASS  3
  Test directory present                     ✓ PASS  3
  Run command documented                     ✓ PASS  2
  .env.example present (if needed)           ✓ PASS  2
  No .env file committed                     ✓ PASS  3
  README.md present and substantive          ✓ PASS  2
  No hardcoded secret patterns               ✓ PASS  3
  Agent boundary file present                ✓ PASS  2

──────────────────────────────────────────────────────────────
  Top Fixes:
    1. Run `agent-scan . --generate` to create a starter AGENTS.md.
    2. Run `agent-scan . --generate` to create a starter copilot-instructions.md.
──────────────────────────────────────────────────────────────
```

Run `agent-scan . --generate` → both failures disappear in seconds.

---

## Critical Failures

The score still uses the same weight formula, but v0.2 adds a separate
critical-failure layer. If a repo has a committed `.env` file or hardcoded
secret-pattern finding, the scanner shows a blocker near the top of terminal,
Markdown, and JSON output.

Example:

```text
Score  : 82 / 100
Status : YELLOW — Mostly Ready
Critical failures: 2

CRITICAL FAILURES PRESENT

  This repo has one or more high-severity failures that should be fixed
  before allowing AI coding agents to modify it.

- No .env file committed: .env file found in repo root — may contain real secrets
- No hardcoded secret patterns: Potential secrets in 1 file(s): src/config.py: OpenAI/Anthropic API key (sk-)
```

Critical failures are blockers for agent execution even when the numeric score
is YELLOW or GREEN.

---

## Score Tiers

| Score | Tier | Meaning |
|---|---|---|
| 85–100 | 🟢 **GREEN — Ready** | Repo is well-configured for AI agents |
| 70–84 | 🟡 **YELLOW — Mostly Ready** | Minor governance gaps; fix before heavy agent use |
| 50–69 | 🟠 **ORANGE — Needs Work** | Agents will struggle; multiple gaps to close |
| 0–49 | 🔴 **RED — Not Ready** | Do not run autonomous agents until gaps are fixed |

---

## The 17 Checks

| # | Check | Weight | What it looks for |
|---|---|---|---|
| 1 | AGENTS.md present | 3 | `AGENTS.md` in repo root with meaningful content |
| 2 | Copilot instructions present | 2 | `.github/copilot-instructions.md` |
| 3 | PR template present | 2 | `.github/pull_request_template.md` |
| 4 | Issue templates present | 1 | `.github/ISSUE_TEMPLATE/*.md` |
| 5 | CI workflow present | 3 | `.github/workflows/*.yml` or `.yaml` |
| 6 | Test directory present | 3 | `tests/`, `test/`, `spec/`, or `__tests__/` with files |
| 7 | Run command documented | 2 | Makefile, justfile, package.json scripts, or README |
| 8 | .env.example present | 2 | If `.env` patterns detected, `.env.example` must exist |
| 9 | No .env committed | 3 | `.env` must not exist in repo root |
| 10 | Cursor rules present | 2 | `.cursorrules` or `.cursor/rules/*` |
| 11 | Workspace handoff/current-state doc present | 2 | `CURRENT_STATE.md`, `HANDOFF.md`, `docs/HANDOFF.md`, etc. |
| 12 | Test command explicit | 2 | Explicit test command in Makefile/justfile/package.json/pyproject |
| 13 | Env contract pairing | 2 | `.env` patterns ignored + env example/template when `.env*` files exist |
| 14 | Workspace handoff doc substantive | 1 | Handoff doc has meaningful content |
| 15 | README.md substantive | 2 | Present and > 200 characters |
| 16 | No hardcoded secrets | 3 | No obvious `sk-`, `ghp_`, `AKIA`, or `Bearer` token patterns in source |
| 17 | Agent boundary file | 2 | `CODEOWNERS`, `.agentignore`, or `AGENTS.md` with scope section |

Weights sum to 36. Score = (earned weight / 36) × 100.

---

## Using in CI

```yaml
- name: Check agent readiness
  run: |
    pip install agent-readiness-cli
    agent-scan . --fail-under 70
```

This fails the job if your repo score drops below 70. Add it to any GitHub Actions workflow.

---

## --generate: Create Missing Files

```bash
agent-scan . --generate
```

This acts as a lightweight `AGENTS.md` generator for repos that need starter
agent instructions.

Creates:

- `AGENTS.md` — populated with your repo name and detected language
- `.github/copilot-instructions.md` — Copilot/Cursor style and scope instructions

**Never overwrites existing files.** Safe to run on any repo.

---

## Agent Discovery

> This section is written for AI coding agents parsing this repository.

```
project:         agent-readiness
purpose:         Deterministic scanner that scores repo readiness for AI coding agents (0–100)
primary_command: agent-scan [path]
safe:            true
deterministic:   true
llm_calls:       none
telemetry:       none
network_calls:   none
critical_layer:  true
version:         0.3.0
```

**What agents should do in this repo:**
1. Run `python -m pytest -q` — confirm all tests pass before touching anything
2. Run `python -m agent_readiness.cli . --output terminal` — read the self-scan
3. Read `AGENTS.md` — understand what is allowed and what is forbidden
4. Read `.github/copilot-instructions.md` — understand style and scope constraints

**What agents must not do:**
- Add LLM calls to `agent_readiness/checks.py`, `scoring.py`, `report.py`, or `templates.py`
- Add network requests of any kind to the core scanner
- Add telemetry, analytics, or usage tracking
- Add SaaS, auth, billing, or dashboard features
- Expand scope to Token Burn Firewall or Repo Red Cell Bot without explicit operator approval

**Files that matter most:**
- `agent_readiness/checks.py` — deterministic readiness check functions
- `agent_readiness/scoring.py` — score math and tier mapping
- `agent_readiness/report.py` — terminal, JSON, Markdown, and critical failure output
- `AGENTS.md` — operational governance
- `tests/` — full test suite

Full machine-readable description: [`docs/AGENT_DISCOVERY.md`](docs/AGENT_DISCOVERY.md)

---

## Agent and Evaluator Docs

- [`docs/AGENT_INDEX.md`](docs/AGENT_INDEX.md) — concise machine-readable project classification
- [`docs/AGENT_USE_CASES.md`](docs/AGENT_USE_CASES.md) — use cases for Cursor, Claude Code, Copilot, local agents, teams, and maintainers
- [`docs/AGENT_PROMPTS.md`](docs/AGENT_PROMPTS.md) — prompts to use after running the scanner
- [`docs/WHY_DETERMINISTIC.md`](docs/WHY_DETERMINISTIC.md) — why the core scan avoids LLM calls
- [`docs/COMPETITIVE_POSITIONING.md`](docs/COMPETITIVE_POSITIONING.md) — how this differs from Claude, Cursor, Copilot, Codex, CodeRabbit, Qodo, SonarQube, and Graphite

---

## Why No LLM Calls

The core scan is pure file-system analysis:

1. **Runs in under 3 seconds** on any machine, including CI
2. **Costs nothing per scan** — no API keys, no tokens, no usage fees
3. **Results are reproducible** — same repo, same score, every time
4. **Works completely offline** — no internet required

The scanner already scans itself and scores **100/100 GREEN**.

The core scan will stay deterministic and free. Optional future assistants must
not weaken this trust boundary.

---

## Roadmap

| Version | Feature |
|---|---|
| **v0.1** | CLI scanner, foundational readiness checks, all output modes, file generation |
| **v0.2** | Critical failures banner, positioning upgrade, agent preflight doctrine |
| **v0.3 (current)** | Agent workspace readiness checks: Cursor rules, handoff continuity, explicit test command, env contract pairing |
| **next likely** | GitHub Action polish, improved scoring model, more secret patterns, config file support |
| **future only** | GitHub App with org-level dashboard |
| **future** | Token Burn Firewall module |
| **future** | Repo Red Cell Bot module |

Full roadmap: [`docs/ROADMAP.md`](docs/ROADMAP.md)

---

## Important Limitations

> **This is not a security scanner.**
> Check 11 detects common obvious patterns (`sk-`, `ghp_`, `AKIA`, `Bearer`). Use [truffleHog](https://github.com/trufflesecurity/trufflehog) or [gitleaks](https://github.com/gitleaks/gitleaks) for real secret scanning. See [SECURITY.md](SECURITY.md).

> **This does not replace human review.**
> A passing score means the repo has the structural signals agents need. It does not guarantee agent-generated code will be correct or safe.

> **This is not a substitute for writing tests.**
> Check 6 detects whether a test directory exists. It does not measure test quality or coverage.

---

## Development

```bash
git clone https://github.com/chevy155/agent-readiness
cd agent-readiness
pip install -e ".[dev]"
python -m pytest -q
agent-scan . --output terminal
```

See [AGENTS.md](AGENTS.md) for contributor guidelines and [CONTRIBUTING.md](CONTRIBUTING.md) for the full contribution guide.

---

## License

MIT — see [LICENSE](LICENSE).
