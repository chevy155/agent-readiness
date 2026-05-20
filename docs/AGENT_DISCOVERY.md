# Agent Discovery — agent-readiness

> Machine-readable / agent-readable description of this repository.
> Written so that AI coding agents can understand the project quickly and operate safely.

---

## Identity

```
repository:      agent-readiness
owner:           chevy155
url:             https://github.com/chevy155/agent-readiness
version:         0.2.0
language:        Python
license:         MIT
```

---

## Purpose

```
one_sentence:    Deterministic CLI that answers "Is your repo ready for AI coding agents?"
score_range:     0–100
output_formats:  terminal, json, markdown
checks:          12 deterministic file-system checks
critical_layer:  true
llm_calls:       none
network_calls:   none
telemetry:       none
runtime_deps:    none (stdlib only)
```

---

## Primary Command

```bash
agent-scan [path]

# Common invocations:
agent-scan .                          # scan current directory
agent-scan . --output json            # machine-readable output
agent-scan . --output markdown        # write AGENT_READINESS.md
agent-scan . --generate               # create missing governance files
agent-scan . --fail-under 70          # CI gate: exit 1 if score < 70
agent-scan . --no-color               # clean output for pipes/logs
agent-scan --version                  # print version
```

---

## Inputs

```
input_type:      local filesystem path (directory)
required:        false (defaults to current directory)
network_access:  none required
api_keys:        none required
auth:            none required
```

---

## Outputs

| Mode | Output |
|---|---|
| `terminal` | Colored score report + check table + top 3 fixes |
| `json` | Structured JSON: score, tier, critical_failures_present, critical_failures[], checks[], recommendations[] |
| `markdown` | `AGENT_READINESS.md` written to scanned repo root |
| `--generate` | Creates `AGENTS.md` and `.github/copilot-instructions.md` if missing |

---

## Safety Properties

```
deterministic:   true — same repo always produces same score
side_effects:    none unless --generate flag is passed
file_writes:     only when --generate is passed; never overwrites existing files
process_spawn:   none
network:         none
secrets_stored:  none
telemetry:       none
```

---

## Critical Failures

Critical failures are surfaced separately from the overall score.

```
critical_check_ids:
  - no_env_committed
  - no_secrets

json_fields:
  - critical_failures_present: true | false
  - critical_failures: [CheckResult]
```

Agents must treat critical failures as blockers before modifying a repo. If
critical failures are present, fix those first before optional governance
improvements like PR templates, issue templates, or README polish.

The score formula is unchanged. Critical failures are a visibility layer so a
YELLOW or GREEN score cannot hide a committed `.env` file or a hardcoded
secret-pattern finding.

---

## Architecture

```
agent_readiness/
  checks.py    → 12 check functions, each returns CheckResult TypedDict
  scoring.py   → compute_score(), get_tier(), get_recommendations(), get_critical_failures()
  report.py    → render_terminal(), render_json(), render_markdown() with critical failure sections
  templates.py → generate_agents_md(), generate_copilot_instructions()
  cli.py       → argparse CLI entry point

templates/
  AGENTS.md.template
  copilot-instructions.md.template

tests/          → pytest suite (no network, no LLM calls)
```

---

## Ideal First Action for an Agent Entering This Repo

1. `python -m pytest -q` — verify tests pass
2. `python -m agent_readiness.cli . --output terminal --no-color` — read self-scan
3. If critical failures are present, fix those before any optional work
4. Read `AGENTS.md` — understand allowed/forbidden changes
5. Read `.github/copilot-instructions.md` — understand style constraints

Do not make any changes until step 4 is complete.

---

## Allowed Changes

An AI agent working in this repo may:

- Fix bugs in existing check functions when a failing test proves the issue
- Add new tests to `tests/` using `tmp_path` pytest fixture
- Improve docstrings and inline comments
- Refactor within a single module without changing public function signatures
- Fix linter warnings without changing behavior

---

## Forbidden Expansions

An AI agent working in this repo must NOT:

```
forbidden:
  - add LLM calls to any core module (checks.py, scoring.py, report.py, templates.py)
  - add network requests of any kind
  - add telemetry, analytics, or usage tracking
  - add runtime dependencies (package must remain zero-dependency)
  - add SaaS, auth, dashboard, billing, or GitHub App features
  - modify .github/workflows/test.yml without operator approval
  - expand scope to Token Burn Firewall or Repo Red Cell Bot
```

---

## Future Modules (Not Present in v0)

These are named in the roadmap but do not exist in this repository:

```
future_modules:
  - name:    Token Burn Firewall
    status:  not built
    scope:   separate product / future module

  - name:    Repo Red Cell Bot
    status:  not built
    scope:   separate product / future module
```

Do not implement these modules in this repository without explicit operator approval.

---

## Test Command

```bash
python -m pytest -q
```

---

## Score Invariants

```
all_pass:   100.0
all_fail:   0.0
all_warn:   50.0
total_weight: 27
critical_score_effect: none (visibility layer only)
tiers:
  GREEN:   85–100
  YELLOW:  70–84
  ORANGE:  50–69
  RED:     0–49
```

---

## Critical Constraint

> **Do not add LLM calls to the core scan.**
> The scanner's core value is determinism and zero cost per run.
> Any LLM dependency in `checks.py`, `scoring.py`, or `report.py` breaks this guarantee.

> **Do not add telemetry.**
> The scanner's secondary value is user trust.
> No usage tracking, no beacon pings, no analytics.

---

*This file is updated with each significant version change.*
*Last updated: 2026-05-20 — v0.2.0*
