# Share Copy

Calm, technical copy for explaining Agent Readiness Scanner without hype.

---

## HN Follow-Up: What Makes This Different From Claude?

Claude, Cursor, Copilot, and Codex can help inspect or modify a repo.

This tool is the preflight check before using them. It does not ask an LLM to
judge the repo. It runs deterministic file-system checks for things agents need:
tests, CI, run commands, repo instructions, PR/issue templates, `.env` hygiene,
and boundaries.

The goal is repeatability. Same repo, same score, no tokens, no telemetry.

---

## GitHub Repo Social Preview Text

Deterministic agent preflight infrastructure. Check whether a repo is ready
before Claude, Cursor, Copilot, Codex, or local agents modify it.

---

## LinkedIn Technical Post

I built Agent Readiness Scanner as a deterministic preflight check for AI coding
agents.

Humans can infer missing context. Agents cannot.

Most repos are readable by humans but under-specified for agents: missing run
commands, weak CI, no `AGENTS.md`, unclear test paths, no PR template, and no
agent boundaries.

Agent Readiness Scanner gives a 0-100 score and now surfaces critical failures
like committed `.env` files separately from the overall score.

No LLM calls. No telemetry. No SaaS. No account.

Repo: https://github.com/chevy155/agent-readiness

---

## X Short Post

Agents are powerful, but they need a runway.

Agent Readiness Scanner checks the runway: tests, CI, run commands, repo
instructions, `.env` hygiene, and agent boundaries.

Deterministic. No LLM calls. No telemetry.

https://github.com/chevy155/agent-readiness

---

## Reddit Technical Post

I built a small Python CLI that checks whether a repo is ready before AI coding
agents modify it.

It runs deterministic checks for `AGENTS.md`, Copilot instructions, CI, tests,
run commands, PR templates, issue templates, `.env` handling, and critical
secret-pattern findings.

It is not a security scanner or an AI code reviewer. It is a preflight gate for
repo structure.

No LLM calls, no telemetry, no SaaS, no account.

Repo: https://github.com/chevy155/agent-readiness

---

## Direct Message to a Developer Friend

I launched a small repo tool you might find useful if you are using Cursor,
Copilot, Claude Code, Codex, or local coding agents.

It checks whether a repo has enough structure before an agent edits it: tests,
CI, run commands, repo instructions, `.env` hygiene, and boundaries.

Repo: https://github.com/chevy155/agent-readiness

---

## Issue Response Template: Feature Requests

Thanks for the suggestion. The core constraint for this project is that the
scanner remains deterministic, local-first, zero telemetry, and no LLM calls.

Can you share:

- The repo scenario this would help
- The current scanner output
- Whether this is a preflight check or a post-edit/code-review feature
- The smallest deterministic signal we could inspect

If it expands into SaaS, dashboards, billing, telemetry, or LLM-required
behavior, it is likely future-only or out of scope.

---

## Issue Response Template: Bug Reports

Thanks for reporting this. Please include:

- OS and Python version
- Command run
- Full terminal output
- Whether `python -m agent_readiness.cli . --output terminal --no-color` works
- Minimal repo/file structure that reproduces the issue
- Expected vs. actual score or critical-failure behavior

The scanner should remain deterministic and should not make network calls.

