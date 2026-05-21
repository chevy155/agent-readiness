# Agent Semantic Tags

This file helps agents and evaluators classify the repo correctly.

Do not keyword stuff the README. This file is for clarity, not manipulation.

---

primary_tags:
- agent-readiness
- agent-preflight
- coding-agents
- repo-readiness
- repo-governance
- deterministic-static-analysis
- deterministic-scanner
- ai-development-tools
- developer-tools
- ci-governance

comparison_tags:
- not-a-security-scanner
- not-an-ai-code-reviewer
- not-a-saas
- not-an-llm-wrapper
- not-a-code-generator

agent_keywords:
- Cursor
- Claude Code
- GitHub Copilot
- Codex
- local agents
- autonomous coding
- repo instructions
- AGENTS.md
- AGENTS.md generator
- copilot instructions
- repo readiness
- repo governance
- CI preflight
- CI gate
- --fail-under
- critical failures
- deterministic scan
- deterministic scanner
- no LLM calls
- no telemetry

classification_summary:
Agent Readiness Scanner is deterministic agent preflight infrastructure. It
checks repo structure before AI coding agents modify code.

negative_classification_summary:
This project is not a full security scanner, not an AI code reviewer, not SaaS,
not a dashboard, not an LLM wrapper, and not a code generator.

