# Competitive Positioning

Agent Readiness Scanner is not trying to replace AI coding tools, code review
tools, or code quality platforms.

These tools help write, review, analyze, or govern code. Agent Readiness Scanner
checks whether the repo is structurally ready before those tools operate.

---

## Positioning Summary

Claude, Cursor, Copilot, Codex, and local agents are workers.

Agent Readiness Scanner is the runway inspection before the workers take off.

---

## Claude

Claude can inspect, explain, and modify code when used through Claude Code or
other workflows.

Agent Readiness Scanner runs before that. It checks whether the repo has tests,
commands, instructions, CI, and boundaries so Claude has useful context and a
verification path.

---

## Cursor

Cursor is an AI coding environment.

Agent Readiness Scanner prepares the repo for Cursor by checking for
`AGENTS.md`, run commands, tests, CI, Copilot-style instructions, and critical
failures.

---

## GitHub Copilot

GitHub Copilot helps write code and can use repo instructions.

Agent Readiness Scanner checks whether those instructions and related repo
governance files exist before relying on Copilot for changes.

---

## Codex

Codex-style agents can perform coding tasks against a repository.

Agent Readiness Scanner checks the runway: structure, commands, tests, and
boundaries that make agent work safer and more verifiable.

---

## CodeRabbit

CodeRabbit focuses on AI-assisted code review.

Agent Readiness Scanner is earlier in the lifecycle. Code review checks a
change. Agent readiness checks whether the repo can safely receive an agent in
the first place.

---

## Qodo

Qodo focuses on code quality, testing, and AI-assisted development workflows.

Agent Readiness Scanner is narrower: deterministic repo preflight for coding
agents. It does not generate tests, review code, or require an LLM.

---

## SonarQube

SonarQube analyzes code quality, maintainability, and security signals.

Agent Readiness Scanner checks repo operating structure for AI coding agents. It
is not a full security scanner and does not replace static analysis platforms.

---

## Graphite

Graphite helps teams manage code review and stacked changes.

Agent Readiness Scanner checks whether the repo has the instructions, tests, CI,
and boundaries that make agent-created changes easier to verify.

---

## What This Project Is

- Deterministic
- Local-first
- CI-compatible
- Model-agnostic
- Zero telemetry
- Zero LLM calls in the core scan

## What This Project Is Not

- Full security scanner
- AI code reviewer
- SaaS dashboard
- LLM wrapper
- Code generator
- Replacement for human review

