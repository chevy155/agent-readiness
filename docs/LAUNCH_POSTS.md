# Launch Posts — Agent Readiness Scanner

> Ready-to-use copy for launch. Edit to taste. Credible, sharp, no hype.

---

## GitHub Repo Short Description

```
Deterministic repo readiness scanner for AI coding agents.
```

---

## GitHub Topics

```
ai-agents
coding-agents
cursor
github-copilot
claude-code
codex
developer-tools
repo-governance
agent-readiness
python-cli
static-analysis
devops
```

---

## LinkedIn Post

---

I built a small open-source tool called **Agent Readiness Scanner**.

It answers one question: **Is your repo actually ready for AI coding agents?**

Humans can infer missing context. Agents cannot.

Most repos work fine for developers but are under-specified for AI agents. Missing run commands. Weak CI. No AGENTS.md. No Copilot instructions. No PR templates. No agent boundary files.

When you point an agent at a repo like that, it burns tokens, makes bad guesses, and breaks things.

**Agent Readiness Scanner** runs 17 deterministic checks and gives your repo a 0–100 readiness score in under 3 seconds. It can also generate starter AGENTS.md and Copilot instruction files.

No LLM calls.
No telemetry.
No SaaS.
No account.

Just a local scan.

Repo: https://github.com/chevy155/agent-readiness

---

#OpenSource #AIAgents #DeveloperTools #Cursor #GitHubCopilot #ClaudeCode #Python

---

## X / Twitter Post (Short)

---

I built Agent Readiness Scanner.

Humans can infer missing context. Agents cannot.

It gives your repo a 0–100 score: does it have AGENTS.md, CI, tests, run commands, PR templates, and safe .env handling?

```
pip install agent-readiness-cli
agent-scan .
```

No LLM calls. No telemetry. No SaaS.

https://github.com/chevy155/agent-readiness

---

## X / Twitter Thread

---

**1/**
I built a small open-source CLI called Agent Readiness Scanner.

It answers: "Is your repo actually ready for AI coding agents?"

Most repos are readable by humans but under-specified for agents. Here's what that means 🧵

**2/**
When you hand a repo to an AI coding agent (Cursor, Copilot, Claude Code, Codex), it needs:

- A test suite it can run
- Documented run commands
- CI that gives pass/fail feedback
- AGENTS.md explaining what it can/can't touch
- .env handled safely

Without this: token waste, bad changes.

**3/**
Agent Readiness Scanner runs 17 checks and produces a 0–100 score:

```
Score  : 83 / 100
Status : YELLOW — Mostly Ready
```

Run `--generate` to auto-create AGENTS.md and Copilot instructions for any repo.

**4/**
No LLM calls.
No telemetry.
No SaaS.
No account.

```
pip install agent-readiness-cli
agent-scan .
```

Repo: https://github.com/chevy155/agent-readiness

Works on any Python, macOS, Linux, Windows.

---

## Hacker News / Show HN Post

**Title:**
```
Show HN: Agent Readiness Scanner – Check if your repo is ready for AI coding agents
```

**Body:**
```
I built Agent Readiness Scanner, a small open-source CLI that answers one question:

Is your repo actually ready for AI coding agents?

Humans can infer missing context. Agents cannot.

Most repos may be readable by humans but are under-specified for agents: missing run
commands, weak CI, no AGENTS.md, no Copilot instructions, unclear test paths, no PR
templates, and no agent boundaries.

This tool gives a repo a 0–100 readiness score using deterministic checks.

No LLM calls. No telemetry. No SaaS. No account required.

Current v0.3 checks 17 signals: AGENTS.md, Copilot instructions, CI workflows,
tests, run commands, README quality, PR templates, issue templates, basic
secret-pattern hygiene, .env handling, Cursor rules, workspace handoff continuity,
explicit test command signals, env contract pairing, and agent boundaries.

It can also generate starter AGENTS.md and GitHub Copilot instruction files.

Repo:
https://github.com/chevy155/agent-readiness

I built it because before letting agents modify a repo, I wanted a simple
deterministic way to know whether the repo gives them enough structure to work safely.
```

---

## Reddit — r/LocalLLaMA

---

**[Tool] Agent Readiness Scanner — check if your repo is structured enough for AI coding agents**

Built a small open-source CLI that runs 17 static checks on a repo and tells you whether it's ready for local AI coding agents (Cursor, Claude Code, local Codex, anything using your repo as context).

The focus: repos that work for local agents specifically — AGENTS.md, .env hygiene, documented test commands, CI, PR templates.

```bash
pip install agent-readiness-cli
agent-scan .
```

Zero runtime dependencies. No LLM calls in the scanner itself. No telemetry.

If you're running local agents against your own repos and want to make sure the repo won't blow up in their hands, this might help.

Repo: https://github.com/chevy155/agent-readiness

---

## Reddit — r/devops

---

**[Tool] Agent Readiness Scanner — static analysis for AI agent governance, works in CI**

If your team is experimenting with AI coding agents (Cursor, Copilot, Claude Code), you've probably noticed that repos without strong structure cause agents to make bad decisions.

Built a CLI that checks:

- AGENTS.md present
- Copilot instructions present
- CI workflow configured
- Tests exist
- Run command documented
- No .env committed
- No hardcoded secrets
- PR/issue templates present
- Agent boundary file

Score is 0–100. Add to CI:

```yaml
- name: Check agent readiness
  run: |
    pip install agent-readiness-cli
    agent-scan . --fail-under 70
```

Open source, MIT, no network calls, no telemetry.

https://github.com/chevy155/agent-readiness

---

## Founder-Style Post

---

Two months ago I was watching a coding agent make a mess of a perfectly reasonable repo.

It wasn't the agent's fault. The repo was fine for a human developer. It had a README, some code, a rough idea of a test suite.

But for an agent: no AGENTS.md, no run command documented, a half-committed .env, no PR template, no CI. The agent had no idea where to start, what to avoid, or how to verify its own work.

So I built Agent Readiness Scanner.

It runs 17 deterministic checks. No LLM. No telemetry. Under 3 seconds. Gives a 0–100 score. Can generate the missing files automatically.

The result is a repo your agents can actually work in.

https://github.com/chevy155/agent-readiness

---

## Technical Post

---

**Agent Readiness Scanner: implementation notes**

The scanner runs 17 file-system checks implemented in pure Python stdlib — no external dependencies. Each check returns a `TypedDict` with `status` (pass/warn/fail), `weight`, and `recommendation`. Score is `sum(earned_weight) / 36 * 100`.

The 17 checks were chosen because they are:

1. **Binary** — either present or not, deterministic every run
2. **Actionable** — each miss maps to a specific fix
3. **Agent-relevant** — specifically what coding agents need, not general repo quality

The `--generate` flag creates `AGENTS.md` and `.github/copilot-instructions.md` from templates, substituting repo name and detected language. It never overwrites existing files.

CI integration is one line:

```yaml
agent-scan . --fail-under 70
```

The scanner scans itself and scores 100/100 GREEN.

Zero runtime deps. Works on Python 3.9+.

https://github.com/chevy155/agent-readiness

---

## Agent-Native / Futuristic Post

---

Humans can infer missing context. Agents cannot.

A developer can look at a messy repo and build a mental model of what runs, what to avoid, how to verify changes. They fill in the blanks from experience.

An AI coding agent cannot. It operates on what is present. Missing AGENTS.md means no scope boundaries. Missing test suite means no feedback loop. Missing run commands means no way to verify. Missing .env hygiene means potential secret exposure. The agent does its best with incomplete information, and that best is often wrong.

**Agent Readiness Scanner** checks whether a repo gives agents the structure they need to act safely. 17 deterministic checks. 0–100 score. No LLM calls. No telemetry.

Structure before autonomy.

https://github.com/chevy155/agent-readiness
