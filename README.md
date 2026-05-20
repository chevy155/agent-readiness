# Agent Readiness Scanner

**Is your repo ready for AI coding agents?**

`agent-scan` runs a fast, deterministic check against your repository and answers:
*"Can Cursor, GitHub Copilot, Claude Code, Codex, or a local agent work safely here?"*

It checks governance files, CI setup, test coverage signals, documentation quality,
and secret safety — then returns a score from 0 to 100 and generates missing files.

**No LLM calls. No network requests. No telemetry. Zero runtime dependencies.**

---

## The Problem

You adopt an AI coding agent. It starts making changes. Then:

- It creates a PR with no test evidence because it doesn't know how to run your tests
- It edits files it should never touch because there are no boundaries defined
- It exposes a secret because `.env` wasn't ignored
- It runs in circles because there's no CI feedback loop

Most repos are not wired for agents. `agent-scan` finds the gaps and fixes them in seconds.

---

## Quick Install

```bash
pip install agent-readiness
```

Or run without installing:

```bash
pipx run agent-readiness
```

---

## Quick Usage

```bash
# Scan current directory
agent-scan .

# Scan a specific repo
agent-scan /path/to/my-project

# Get JSON output (for CI integration)
agent-scan . --output json

# Write AGENT_READINESS.md to the repo
agent-scan . --output markdown

# Generate missing governance files (AGENTS.md, copilot-instructions.md)
agent-scan . --generate

# Fail CI if score is below 70
agent-scan . --fail-under 70

# Show evidence and fix details for every check
agent-scan . --verbose
```

---

## Example Output

```
──────────────────────────────────────────────────────────────
  Agent Readiness Scanner  v0.1.0
──────────────────────────────────────────────────────────────
  Repo   : /Users/dev/my-project
  Score  : 83 / 100
  Status : YELLOW  —  Mostly Ready
──────────────────────────────────────────────────────────────

  Check                                      Status  Wt
  ────────────────────────────────────────── ─────── ──
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

  Tip: run with --generate to create missing governance files.
──────────────────────────────────────────────────────────────
```

Run `agent-scan . --generate` and those two failures disappear.

---

## Score Tiers

| Score | Tier | Meaning |
|---|---|---|
| 85–100 | 🟢 GREEN — Ready | Repo is well-configured for AI agents |
| 70–84 | 🟡 YELLOW — Mostly Ready | Minor governance gaps; fix before heavy agent use |
| 50–69 | 🟠 ORANGE — Needs Work | Agents will struggle; multiple gaps to close |
| 0–49 | 🔴 RED — Not Ready | Do not run autonomous agents until gaps are fixed |

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
| 12 | Agent boundary file | 2 | `CODEOWNERS`, `.agentignore`, or `AGENTS.md` with boundaries section |

Weights sum to 27. Score = (earned weight / 27) × 100.

---

## Using in CI

Add this to your GitHub Actions workflow:

```yaml
- name: Check agent readiness
  run: |
    pip install agent-readiness
    agent-scan . --fail-under 70
```

This will fail the job if your repo score drops below 70.

Or use the included `test.yml` workflow which runs the scan on every push.

---

## --generate: Create Missing Files

Running `agent-scan . --generate` creates:

- `AGENTS.md` — operational guidance for AI agents, populated with your repo name and detected language
- `.github/copilot-instructions.md` — Copilot/Cursor style and scope instructions

**It will never overwrite existing files.**

---

## Why No LLM Calls in v0?

The core scan is pure file-system analysis. This means:

1. **It runs in 1–3 seconds** on any machine, including CI
2. **It costs nothing** per scan — no API keys, no tokens
3. **Results are reproducible** — same repo, same score, every time
4. **It works offline** — no internet connection required

Future versions may add an optional LLM-assisted layer for richer governance file generation.
The core scan will always remain deterministic and free.

---

## Roadmap

| Version | Feature |
|---|---|
| **v0.1 (now)** | CLI scanner, 12 checks, JSON/Markdown output, file generation |
| **v0.2** | GitHub Actions Marketplace listing |
| **v0.3** | Score history (local file-based, no server) |
| **future** | GitHub App with org-level dashboard |
| **future** | Token Burn Firewall module (monitor agent run costs) |
| **future** | Repo Red Cell Bot module (adversarial PR review) |

---

## Important Limitations

> **This is not a security scanner.**
> Check 11 (secret patterns) is a basic heuristic, not a comprehensive secret detection tool.
> Use [truffleHog](https://github.com/trufflesecurity/trufflehog) or [gitleaks](https://github.com/gitleaks/gitleaks) for real secret scanning.

> **This does not replace human review.**
> A passing score means the repo has the structural signals agents need.
> It does not guarantee agent-generated code will be correct or safe.

> **Weights are opinionated.**
> The default weights reflect one operator's view of what matters most.
> They may not match your team's priorities. Adjust via config in a future version.

---

## Development

```bash
git clone https://github.com/yourusername/agent-readiness
cd agent-readiness
pip install -e .
python -m pytest -q
agent-scan . --output terminal
```

See [AGENTS.md](AGENTS.md) for contributor guidelines and scope boundaries.

---

## License

MIT — see [LICENSE](LICENSE).
