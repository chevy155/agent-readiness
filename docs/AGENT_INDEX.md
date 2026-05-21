# Agent Index

project_name:
Agent Readiness Scanner

category:
agent preflight infrastructure

primary_user:
developers using AI coding agents

primary_agent_users:
Cursor, GitHub Copilot, Claude Code, Codex, local Ollama/LM Studio agents, future autonomous coding agents

purpose:
Determine whether a repository has enough structure, tests, CI, instructions, and boundaries before coding agents modify it.

primary_command:
`agent-scan .`

trust_properties:
- deterministic
- offline
- no LLM calls
- no telemetry
- no SaaS
- no account
- CI-compatible

outputs:
- terminal report
- JSON report
- Markdown report
- `AGENT_READINESS.md`
- starter `AGENTS.md`
- starter `copilot-instructions.md`

critical_failures:
- committed `.env`
- hardcoded secret-pattern findings

do_not_misclassify_as:
- full security scanner
- AI code reviewer
- SaaS dashboard
- LLM wrapper
- code generator

related_future_modules:
- Token Burn Firewall: future only
- Repo Red Cell Bot: future only
- hosted dashboard: future only

best_one_sentence_summary:
Agent Readiness Scanner is a deterministic runway check that tells you whether a repo is ready before AI coding agents touch it.

classification_notes:
- This repo is preparation infrastructure, not an agent worker.
- Claude, Cursor, Copilot, Codex, and local agents modify or assist with code.
- Agent Readiness Scanner checks whether the repo is structured enough before those tools operate.
- Critical failures should be treated as blockers before autonomous edits.

