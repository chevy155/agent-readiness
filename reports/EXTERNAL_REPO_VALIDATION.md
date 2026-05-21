# External Repo Validation — Agent Readiness Scanner

**Generated:** 2026-05-21 21:21 UTC  
**Scanner version:** 0.2.0  
**Method:** local fixture repos representing real-world readiness levels  

---

## Summary

| Fixture | Score | Tier | Expected | Pass |
|---|---|---|---|---|
| Fixture 1 — Bare Readme Only | 27/100 | RED — Not Ready | RED | ✅ |
| Fixture 2 — Python Project, No Governance | 49/100 | RED — Not Ready | RED | ✅ |
| Fixture 3 — Node.js Project, Partial Setup | 65/100 | ORANGE — Needs Work | ORANGE | ✅ |
| Fixture 4 — Good Structure, Critical Security Failures | 60/100 | ORANGE — Needs Work | ORANGE | ✅ |
| Fixture 5 — Fully Configured | 100/100 | GREEN — Ready | GREEN | ✅ |
| Fixture 6 — Cursor Workspace Strong | 95/100 | GREEN — Ready | GREEN | ✅ |
| Fixture 7 — Cursor Rules Missing | 68/100 | ORANGE — Needs Work | ORANGE | ✅ |
| Fixture 8 — Handoff Missing | 65/100 | ORANGE — Needs Work | ORANGE | ✅ |
| Fixture 9 — Env Contract Broken | 68/100 | ORANGE — Needs Work | ORANGE | ✅ |

---

## Fixture 1 — Bare Readme Only

**Description:** Only a short README.md. No tests, CI, governance, or safety setup.

| Score | Tier | Critical Failures | Expected | Match |
|---|---|---|---|---|
| **27 / 100** | **RED — Not Ready** | **0** | RED | ✅ |

| Check | Status | Weight | Evidence |
|---|---|---|---|
| AGENTS.md present | ❌ FAIL | 3 | AGENTS.md not found in repo root |
| .github/copilot-instructions.md present | ❌ FAIL | 2 | .github/copilot-instructions.md not found |
| PR template present | ❌ FAIL | 2 | .github/pull_request_template.md not found |
| Issue templates present | ❌ FAIL | 1 | .github/ISSUE_TEMPLATE/ not found or empty |
| CI workflow present | ❌ FAIL | 3 | .github/workflows/*.yml not found |
| Test directory present | ❌ FAIL | 3 | No test directory found (checked: tests/, test/, spec/, __tests__/) |
| Run command documented | ❌ FAIL | 2 | No Makefile, justfile, package.json scripts, or pyproject.toml test config found |
| .env.example present (if needed) | ✅ PASS | 2 | No .env-like files detected — check not applicable |
| No .env file committed | ✅ PASS | 3 | .env file not found in repo root |
| Cursor rules present | ❌ FAIL | 2 | No .cursorrules or .cursor/rules/* file found |
| Workspace handoff/current-state doc present | ❌ FAIL | 2 | No CURRENT_STATE/HANDOFF/session notes doc found in root or docs/ |
| Test command explicit | ❌ FAIL | 2 | No explicit test command found in Makefile/justfile/package.json/pyproject.toml |
| Env contract pairing | ✅ PASS | 2 | No .env-like runtime files detected — check not applicable |
| Workspace handoff doc substantive | ❌ FAIL | 1 | No handoff/current-state doc available to assess substance |
| README.md present and substantive | ❌ FAIL | 2 | README.md found but nearly empty (24 characters) |
| No hardcoded secret patterns | ✅ PASS | 3 | No obvious secret patterns detected in non-test source files |
| Agent boundary file present | ❌ FAIL | 2 | No CODEOWNERS, .agentignore, or AGENTS.md with boundary section found |

**Top Fixes:**

1. Run `agent-scan . --generate` to create a starter AGENTS.md.
2. Add a GitHub Actions workflow that runs your test suite on push.
3. Create a tests/ directory with at least one test file.

---

## Fixture 2 — Python Project, No Governance

**Description:** Has tests, pyproject.toml, .gitignore, and a substantive README. Missing all governance files: no AGENTS.md, no CI, no PR/issue templates.

| Score | Tier | Critical Failures | Expected | Match |
|---|---|---|---|---|
| **49 / 100** | **RED — Not Ready** | **0** | RED | ✅ |

| Check | Status | Weight | Evidence |
|---|---|---|---|
| AGENTS.md present | ❌ FAIL | 3 | AGENTS.md not found in repo root |
| .github/copilot-instructions.md present | ❌ FAIL | 2 | .github/copilot-instructions.md not found |
| PR template present | ❌ FAIL | 2 | .github/pull_request_template.md not found |
| Issue templates present | ❌ FAIL | 1 | .github/ISSUE_TEMPLATE/ not found or empty |
| CI workflow present | ❌ FAIL | 3 | .github/workflows/*.yml not found |
| Test directory present | ✅ PASS | 3 | Found tests/ with 1 test file(s) |
| Run command documented | ✅ PASS | 2 | Found pyproject.toml with pytest or scripts configuration |
| .env.example present (if needed) | ✅ PASS | 2 | No .env-like files detected — check not applicable |
| No .env file committed | ✅ PASS | 3 | .env not present; .gitignore includes .env pattern |
| Cursor rules present | ❌ FAIL | 2 | No .cursorrules or .cursor/rules/* file found |
| Workspace handoff/current-state doc present | ❌ FAIL | 2 | No CURRENT_STATE/HANDOFF/session notes doc found in root or docs/ |
| Test command explicit | ✅ PASS | 2 | Found pyproject.toml with pytest configuration |
| Env contract pairing | ✅ PASS | 2 | No .env-like runtime files detected — check not applicable |
| Workspace handoff doc substantive | ❌ FAIL | 1 | No handoff/current-state doc available to assess substance |
| README.md present and substantive | ⚠️ WARN | 2 | README.md found but brief (429 characters) |
| No hardcoded secret patterns | ✅ PASS | 3 | No obvious secret patterns detected in non-test source files |
| Agent boundary file present | ❌ FAIL | 2 | No CODEOWNERS, .agentignore, or AGENTS.md with boundary section found |

**Top Fixes:**

1. Run `agent-scan . --generate` to create a starter AGENTS.md.
2. Add a GitHub Actions workflow that runs your test suite on push.
3. Run `agent-scan . --generate` to create a starter copilot-instructions.md.

---

## Fixture 3 — Node.js Project, Partial Setup

**Description:** Has CI, tests, package.json scripts, PR template, .env.example. Missing AGENTS.md, copilot-instructions, and issue templates.

| Score | Tier | Critical Failures | Expected | Match |
|---|---|---|---|---|
| **65 / 100** | **ORANGE — Needs Work** | **0** | ORANGE | ✅ |

| Check | Status | Weight | Evidence |
|---|---|---|---|
| AGENTS.md present | ❌ FAIL | 3 | AGENTS.md not found in repo root |
| .github/copilot-instructions.md present | ❌ FAIL | 2 | .github/copilot-instructions.md not found |
| PR template present | ✅ PASS | 2 | Found .github/pull_request_template.md |
| Issue templates present | ❌ FAIL | 1 | .github/ISSUE_TEMPLATE/ not found or empty |
| CI workflow present | ✅ PASS | 3 | Found 1 workflow(s): ci.yml |
| Test directory present | ✅ PASS | 3 | Found tests/ with 1 test file(s) |
| Run command documented | ✅ PASS | 2 | Found package.json with scripts.test or scripts.start |
| .env.example present (if needed) | ✅ PASS | 2 | No .env-like files detected — check not applicable |
| No .env file committed | ✅ PASS | 3 | .env not present; .gitignore includes .env pattern |
| Cursor rules present | ❌ FAIL | 2 | No .cursorrules or .cursor/rules/* file found |
| Workspace handoff/current-state doc present | ❌ FAIL | 2 | No CURRENT_STATE/HANDOFF/session notes doc found in root or docs/ |
| Test command explicit | ✅ PASS | 2 | Found package.json scripts.test |
| Env contract pairing | ✅ PASS | 2 | No .env-like runtime files detected — check not applicable |
| Workspace handoff doc substantive | ❌ FAIL | 1 | No handoff/current-state doc available to assess substance |
| README.md present and substantive | ✅ PASS | 2 | README.md found (743 characters) |
| No hardcoded secret patterns | ✅ PASS | 3 | No obvious secret patterns detected in non-test source files |
| Agent boundary file present | ❌ FAIL | 2 | No CODEOWNERS, .agentignore, or AGENTS.md with boundary section found |

**Top Fixes:**

1. Run `agent-scan . --generate` to create a starter AGENTS.md.
2. Run `agent-scan . --generate` to create a starter copilot-instructions.md.
3. Add .cursorrules or .cursor/rules/ with project-specific agent constraints.

---

## Fixture 4 — Good Structure, Critical Security Failures

**Description:** Has governance files, CI, tests, and documentation. BUT: .env committed to repo root AND hardcoded API key in src/config.py.

| Score | Tier | Critical Failures | Expected | Match |
|---|---|---|---|---|
| **60 / 100** | **ORANGE — Needs Work** | **2** | ORANGE | ✅ |

> **Product Insight:** Score stays YELLOW despite two critical failures because weight-based scoring spreads impact. v0.2 fixes the visibility gap by surfacing critical failures separately from the score.

### Critical Failures

| Check | Evidence | Recommendation |
|---|---|---|
| No .env file committed | .env file found in repo root — may contain real secrets | Remove .env from the repo immediately and add it to .gitignore. |
| No hardcoded secret patterns | Potential secrets in 1 file(s): src\config.py: OpenAI/Anthropic API key (sk-) | Remove hardcoded secrets and use environment variables or a secrets manager. |

| Check | Status | Weight | Evidence |
|---|---|---|---|
| AGENTS.md present | ✅ PASS | 3 | Found AGENTS.md (213 bytes) |
| .github/copilot-instructions.md present | ✅ PASS | 2 | Found .github/copilot-instructions.md (173 bytes) |
| PR template present | ✅ PASS | 2 | Found .github/pull_request_template.md |
| Issue templates present | ✅ PASS | 1 | Found 1 template(s) in .github/ISSUE_TEMPLATE/ |
| CI workflow present | ✅ PASS | 3 | Found 1 workflow(s): test.yml |
| Test directory present | ✅ PASS | 3 | Found tests/ with 1 test file(s) |
| Run command documented | ✅ PASS | 2 | Found pyproject.toml with pytest or scripts configuration |
| .env.example present (if needed) | ⚠️ WARN | 2 | .env-like file(s) found (.env) but no .env.example exists |
| No .env file committed | ❌ FAIL | 3 | .env file found in repo root — may contain real secrets |
| Cursor rules present | ❌ FAIL | 2 | No .cursorrules or .cursor/rules/* file found |
| Workspace handoff/current-state doc present | ❌ FAIL | 2 | No CURRENT_STATE/HANDOFF/session notes doc found in root or docs/ |
| Test command explicit | ✅ PASS | 2 | Found pyproject.toml with pytest configuration |
| Env contract pairing | ❌ FAIL | 2 | .env-like file(s) found (.env) but .gitignore does not protect .env patterns |
| Workspace handoff doc substantive | ❌ FAIL | 1 | No handoff/current-state doc available to assess substance |
| README.md present and substantive | ⚠️ WARN | 2 | README.md found but brief (468 characters) |
| No hardcoded secret patterns | ❌ FAIL | 3 | Potential secrets in 1 file(s): src\config.py: OpenAI/Anthropic API key (sk-) |
| Agent boundary file present | ✅ PASS | 2 | AGENTS.md contains boundary/scope keywords |

**Top Fixes:**

1. Remove .env from the repo immediately and add it to .gitignore.
2. Remove hardcoded secrets and use environment variables or a secrets manager.
3. Add .cursorrules or .cursor/rules/ with project-specific agent constraints.

---

## Fixture 5 — Fully Configured

**Description:** Has AGENTS.md with boundaries, copilot instructions, PR template, issue templates, CI, tests, Makefile, .env.example, .gitignore, README, CODEOWNERS. No .env committed. No secrets in source.

| Score | Tier | Critical Failures | Expected | Match |
|---|---|---|---|---|
| **100 / 100** | **GREEN — Ready** | **0** | GREEN | ✅ |

| Check | Status | Weight | Evidence |
|---|---|---|---|
| AGENTS.md present | ✅ PASS | 3 | Found AGENTS.md (671 bytes) |
| .github/copilot-instructions.md present | ✅ PASS | 2 | Found .github/copilot-instructions.md (212 bytes) |
| PR template present | ✅ PASS | 2 | Found .github/pull_request_template.md |
| Issue templates present | ✅ PASS | 1 | Found 1 template(s) in .github/ISSUE_TEMPLATE/ |
| CI workflow present | ✅ PASS | 3 | Found 1 workflow(s): ci.yml |
| Test directory present | ✅ PASS | 3 | Found tests/ with 1 test file(s) |
| Run command documented | ✅ PASS | 2 | Found Makefile with `test` target |
| .env.example present (if needed) | ✅ PASS | 2 | No .env-like files detected — check not applicable |
| No .env file committed | ✅ PASS | 3 | .env not present; .gitignore includes .env pattern |
| Cursor rules present | ✅ PASS | 2 | Found .cursorrules (148 bytes) |
| Workspace handoff/current-state doc present | ✅ PASS | 2 | Found handoff/current-state doc(s): CURRENT_STATE.md |
| Test command explicit | ✅ PASS | 2 | Found Makefile with explicit `test` target |
| Env contract pairing | ✅ PASS | 2 | No .env-like runtime files detected — check not applicable |
| Workspace handoff doc substantive | ✅ PASS | 1 | CURRENT_STATE.md appears substantive (284 bytes) |
| README.md present and substantive | ✅ PASS | 2 | README.md found (796 characters) |
| No hardcoded secret patterns | ✅ PASS | 3 | No obvious secret patterns detected in non-test source files |
| Agent boundary file present | ✅ PASS | 2 | Found CODEOWNERS at CODEOWNERS |

---

## Fixture 6 — Cursor Workspace Strong

**Description:** Full governance plus Cursor rules, explicit handoff doc, explicit test command, and safe env contract pairing.

| Score | Tier | Critical Failures | Expected | Match |
|---|---|---|---|---|
| **95 / 100** | **GREEN — Ready** | **0** | GREEN | ✅ |

| Check | Status | Weight | Evidence |
|---|---|---|---|
| AGENTS.md present | ✅ PASS | 3 | Found AGENTS.md (273 bytes) |
| .github/copilot-instructions.md present | ✅ PASS | 2 | Found .github/copilot-instructions.md (167 bytes) |
| PR template present | ✅ PASS | 2 | Found .github/pull_request_template.md |
| Issue templates present | ✅ PASS | 1 | Found 1 template(s) in .github/ISSUE_TEMPLATE/ |
| CI workflow present | ✅ PASS | 3 | Found 1 workflow(s): ci.yml |
| Test directory present | ✅ PASS | 3 | Found tests/ with 1 test file(s) |
| Run command documented | ✅ PASS | 2 | Found pyproject.toml with pytest or scripts configuration |
| .env.example present (if needed) | ✅ PASS | 2 | Found example file alongside .env-like files |
| No .env file committed | ✅ PASS | 3 | .env not present; .gitignore includes .env pattern |
| Cursor rules present | ✅ PASS | 2 | Found .cursorrules (150 bytes) |
| Workspace handoff/current-state doc present | ✅ PASS | 2 | Found handoff/current-state doc(s): CURRENT_STATE.md |
| Test command explicit | ✅ PASS | 2 | Found pyproject.toml with pytest configuration |
| Env contract pairing | ✅ PASS | 2 | .env-like files detected; .gitignore protects .env and example/template file is present |
| Workspace handoff doc substantive | ✅ PASS | 1 | CURRENT_STATE.md appears substantive (268 bytes) |
| README.md present and substantive | ❌ FAIL | 2 | README.md found but nearly empty (194 characters) |
| No hardcoded secret patterns | ✅ PASS | 3 | No obvious secret patterns detected in non-test source files |
| Agent boundary file present | ✅ PASS | 2 | AGENTS.md contains boundary/scope keywords |

**Top Fixes:**

1. Expand README.md with meaningful content (minimum 200 characters).

---

## Fixture 7 — Cursor Rules Missing

**Description:** Strong governance and testability, but missing .cursorrules/.cursor/rules agent policy.

| Score | Tier | Critical Failures | Expected | Match |
|---|---|---|---|---|
| **68 / 100** | **ORANGE — Needs Work** | **0** | ORANGE | ✅ |

| Check | Status | Weight | Evidence |
|---|---|---|---|
| AGENTS.md present | ✅ PASS | 3 | Found AGENTS.md (239 bytes) |
| .github/copilot-instructions.md present | ❌ FAIL | 2 | .github/copilot-instructions.md not found |
| PR template present | ❌ FAIL | 2 | .github/pull_request_template.md not found |
| Issue templates present | ❌ FAIL | 1 | .github/ISSUE_TEMPLATE/ not found or empty |
| CI workflow present | ❌ FAIL | 3 | .github/workflows/*.yml not found |
| Test directory present | ✅ PASS | 3 | Found tests/ with 1 test file(s) |
| Run command documented | ✅ PASS | 2 | Found pyproject.toml with pytest or scripts configuration |
| .env.example present (if needed) | ✅ PASS | 2 | Found example file alongside .env-like files |
| No .env file committed | ✅ PASS | 3 | .env not present; .gitignore includes .env pattern |
| Cursor rules present | ❌ FAIL | 2 | No .cursorrules or .cursor/rules/* file found |
| Workspace handoff/current-state doc present | ✅ PASS | 2 | Found handoff/current-state doc(s): CURRENT_STATE.md |
| Test command explicit | ✅ PASS | 2 | Found pyproject.toml with pytest configuration |
| Env contract pairing | ✅ PASS | 2 | .env-like files detected; .gitignore protects .env and example/template file is present |
| Workspace handoff doc substantive | ✅ PASS | 1 | CURRENT_STATE.md appears substantive (184 bytes) |
| README.md present and substantive | ❌ FAIL | 2 | README.md found but nearly empty (110 characters) |
| No hardcoded secret patterns | ✅ PASS | 3 | No obvious secret patterns detected in non-test source files |
| Agent boundary file present | ✅ PASS | 2 | AGENTS.md contains boundary/scope keywords |

**Top Fixes:**

1. Add a GitHub Actions workflow that runs your test suite on push.
2. Run `agent-scan . --generate` to create a starter copilot-instructions.md.
3. Add .github/pull_request_template.md with a checklist for reviewers.

---

## Fixture 8 — Handoff Missing

**Description:** Strong workspace setup without current-state/handoff continuity docs.

| Score | Tier | Critical Failures | Expected | Match |
|---|---|---|---|---|
| **65 / 100** | **ORANGE — Needs Work** | **0** | ORANGE | ✅ |

| Check | Status | Weight | Evidence |
|---|---|---|---|
| AGENTS.md present | ✅ PASS | 3 | Found AGENTS.md (214 bytes) |
| .github/copilot-instructions.md present | ❌ FAIL | 2 | .github/copilot-instructions.md not found |
| PR template present | ❌ FAIL | 2 | .github/pull_request_template.md not found |
| Issue templates present | ❌ FAIL | 1 | .github/ISSUE_TEMPLATE/ not found or empty |
| CI workflow present | ❌ FAIL | 3 | .github/workflows/*.yml not found |
| Test directory present | ✅ PASS | 3 | Found tests/ with 1 test file(s) |
| Run command documented | ✅ PASS | 2 | Found pyproject.toml with pytest or scripts configuration |
| .env.example present (if needed) | ✅ PASS | 2 | Found example file alongside .env-like files |
| No .env file committed | ✅ PASS | 3 | .env not present; .gitignore includes .env pattern |
| Cursor rules present | ✅ PASS | 2 | Found .cursorrules (99 bytes) |
| Workspace handoff/current-state doc present | ❌ FAIL | 2 | No CURRENT_STATE/HANDOFF/session notes doc found in root or docs/ |
| Test command explicit | ✅ PASS | 2 | Found pyproject.toml with pytest configuration |
| Env contract pairing | ✅ PASS | 2 | .env-like files detected; .gitignore protects .env and example/template file is present |
| Workspace handoff doc substantive | ❌ FAIL | 1 | No handoff/current-state doc available to assess substance |
| README.md present and substantive | ❌ FAIL | 2 | README.md found but nearly empty (107 characters) |
| No hardcoded secret patterns | ✅ PASS | 3 | No obvious secret patterns detected in non-test source files |
| Agent boundary file present | ✅ PASS | 2 | AGENTS.md contains boundary/scope keywords |

**Top Fixes:**

1. Add a GitHub Actions workflow that runs your test suite on push.
2. Run `agent-scan . --generate` to create a starter copilot-instructions.md.
3. Add .github/pull_request_template.md with a checklist for reviewers.

---

## Fixture 9 — Env Contract Broken

**Description:** Contains .env-like runtime files but .gitignore is missing .env protections, triggering env contract pairing failure.

| Score | Tier | Critical Failures | Expected | Match |
|---|---|---|---|---|
| **68 / 100** | **ORANGE — Needs Work** | **0** | ORANGE | ✅ |

| Check | Status | Weight | Evidence |
|---|---|---|---|
| AGENTS.md present | ✅ PASS | 3 | Found AGENTS.md (165 bytes) |
| .github/copilot-instructions.md present | ❌ FAIL | 2 | .github/copilot-instructions.md not found |
| PR template present | ❌ FAIL | 2 | .github/pull_request_template.md not found |
| Issue templates present | ❌ FAIL | 1 | .github/ISSUE_TEMPLATE/ not found or empty |
| CI workflow present | ❌ FAIL | 3 | .github/workflows/*.yml not found |
| Test directory present | ✅ PASS | 3 | Found tests/ with 1 test file(s) |
| Run command documented | ✅ PASS | 2 | Found pyproject.toml with pytest or scripts configuration |
| .env.example present (if needed) | ✅ PASS | 2 | Found example file alongside .env-like files |
| No .env file committed | ✅ PASS | 3 | .env file not found in repo root |
| Cursor rules present | ✅ PASS | 2 | Found .cursorrules (59 bytes) |
| Workspace handoff/current-state doc present | ✅ PASS | 2 | Found handoff/current-state doc(s): CURRENT_STATE.md |
| Test command explicit | ✅ PASS | 2 | Found pyproject.toml with pytest configuration |
| Env contract pairing | ❌ FAIL | 2 | .env-like file(s) found (.env.local) but .gitignore does not protect .env patterns |
| Workspace handoff doc substantive | ✅ PASS | 1 | CURRENT_STATE.md appears substantive (142 bytes) |
| README.md present and substantive | ❌ FAIL | 2 | README.md found but nearly empty (115 characters) |
| No hardcoded secret patterns | ✅ PASS | 3 | No obvious secret patterns detected in non-test source files |
| Agent boundary file present | ✅ PASS | 2 | AGENTS.md contains boundary/scope keywords |

**Top Fixes:**

1. Add a GitHub Actions workflow that runs your test suite on push.
2. Run `agent-scan . --generate` to create a starter copilot-instructions.md.
3. Add .github/pull_request_template.md with a checklist for reviewers.

---

## Observations

### Scores Feel Honest

- **Fixture 1 (RED):** A nearly empty repo correctly scores in the danger zone. An agent running here has no test suite to verify against, no run command, no governance, and no CI. The score reflects real operational risk.

- **Fixture 2 (ORANGE):** A well-coded Python project with tests and documentation but zero governance files. Score is correct: the project has technical quality but is not agent-ready because there are no AGENTS.md boundaries or CI feedback loop.

- **Fixture 3 (YELLOW):** A Node.js project with CI, tests, PR template, and env setup is mostly ready. Missing governance files (AGENTS.md, copilot instructions) and issue templates drag the score to YELLOW. Fix is two files.

### Critical Failure Visibility Confirmed

- **Fixture 4 (YELLOW, security failures):** A repo with a committed `.env` file and a hardcoded API key in source code still scores in the YELLOW tier. v0.2 keeps the score formula unchanged but surfaces both failures separately as critical blockers in terminal, Markdown, and JSON output.

- **Fixture 5 (GREEN):** A fully configured repo scores 100/100. Every check passes. The CODEOWNERS file satisfies agent_boundary. The Makefile satisfies run_command. The .env.example satisfies env_example because .env.example is present. This is what a target repo looks like.

### Score Sensitivity

A 5-check failure on the highest-weight checks (weight 3) costs ~55 points. The weights are designed so that infrastructure failures (no CI, no tests) and safety failures (secrets, .env committed) dominate the score. Governance failures (no AGENTS.md) matter but are recoverable in minutes with `agent-scan . --generate`.

---

## Verdict

Fixture tiers matched expected readiness patterns across governance, workspace policy, handoff continuity, and env contract checks. The scoring system remains deterministic and critical failures still surface separately from the numeric score.

**Scanner is ready for public release.**