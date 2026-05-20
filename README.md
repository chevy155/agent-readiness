# Agent Readiness Scanner

**Is your repo actually ready for AI coding agents?**

[![CI](https://github.com/chevy155/agent-readiness/actions/workflows/test.yml/badge.svg)](https://github.com/chevy155/agent-readiness/actions/workflows/test.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://pypi.org/project/agent-readiness/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A deterministic readiness scanner for Cursor, GitHub Copilot, Claude Code, Codex, and local agents.

```bash
git clone https://github.com/chevy155/agent-readiness.git
cd agent-readiness
pip install -e .
agent-scan .
```

---

## Why This Exists

**Humans can infer missing context. Agents cannot.**

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
git clone https://github.com/chevy155/agent-readiness.git
cd agent-readiness
pip install -e .
```

For development (includes pytest):

```bash
pip install -e ".[dev]"
```

> **PyPI:** `pip install agent-readiness` will work once the package is published to PyPI.

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
  Agent Readiness Scanner  v0.1.0
──────────────────────────────────────────────────────────────
  Repo   : /my-project
  Score  : 83 / 100
  Status : YELLOW  —  Mostly Ready
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

## Score Tiers

| Score | Tier | Meaning |
|---|---|---|
| 85–100 | 🟢 **GREEN — Ready** | Repo is well-configured for AI agents |
| 70–84 | 🟡 **YELLOW — Mostly Ready** | Minor governance gaps; fix before heavy agent use |
| 50–69 | 🟠 **ORANGE — Needs Work** | Agents will struggle; multiple gaps to close |
| 0–49 | 🔴 **RED — Not Ready** | Do not run autonomous agents until gaps are fixed |

---

## The 12 Checks

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
| 10 | README.md substantive | 2 | Present and > 200 characters |
| 11 | No hardcoded secrets | 3 | No `sk-`, `ghp_`, `AKIA`, or `Bearer` tokens in source |
| 12 | Agent boundary file | 2 | `CODEOWNERS`, `.agentignore`, or `AGENTS.md` with scope section |

Weights sum to 27. Score = (earned weight / 27) × 100.

---

## Using in CI

```yaml
- name: Check agent readiness
  run: |
    pip install git+https://github.com/chevy155/agent-readiness.git
    agent-scan . --fail-under 70
```

This fails the job if your repo score drops below 70. Add it to any GitHub Actions workflow.

> Once published to PyPI, replace with `pip install agent-readiness`.

---

## --generate: Create Missing Files

```bash
agent-scan . --generate
```

Creates:

- `AGENTS.md` — populated with your repo name and detected language
- `.github/copilot-instructions.md` — Copilot/Cursor style and scope instructions

**Never overwrites existing files.** Safe to run on any repo.

---

## Agent Discovery

> This section is written for AI coding agents parsing this repository.

```
project:         agent-readiness
purpose:         Deterministic CLI that scores repo readiness for AI coding agents (0–100)
primary_command: agent-scan [path]
safe:            true
deterministic:   true
llm_calls:       none
telemetry:       none
network_calls:   none
version:         0.1.0
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
- `agent_readiness/checks.py` — the 12 check functions
- `agent_readiness/scoring.py` — score math and tier mapping
- `AGENTS.md` — operational governance
- `tests/` — full test suite (108 tests)

Full machine-readable description: [`docs/AGENT_DISCOVERY.md`](docs/AGENT_DISCOVERY.md)

---

## Why No LLM Calls in v0

The core scan is pure file-system analysis:

1. **Runs in under 3 seconds** on any machine, including CI
2. **Costs nothing per scan** — no API keys, no tokens, no usage fees
3. **Results are reproducible** — same repo, same score, every time
4. **Works completely offline** — no internet required

The scanner already scans itself and scores **100/100 GREEN**.

Future versions may add an optional LLM-assisted generation layer. The core scan will always remain deterministic and free.

---

## Roadmap

| Version | Feature |
|---|---|
| **v0.1 (current)** | CLI scanner, 12 checks, all output modes, file generation |
| **v0.2** | Critical-failures banner, score history (local), `--no-color` polish |
| **v0.3** | GitHub Actions Marketplace listing |
| **future** | GitHub App with org-level dashboard |
| **future** | Token Burn Firewall module |
| **future** | Repo Red Cell Bot module |

---

## Important Limitations

> **This is not a security scanner.**
> Check 11 detects four common patterns. Use [truffleHog](https://github.com/trufflesecurity/trufflehog) or [gitleaks](https://github.com/gitleaks/gitleaks) for real secret scanning. See [SECURITY.md](SECURITY.md).

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
