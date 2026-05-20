# Marketing Positioning — Agent Readiness Scanner

> Internal positioning document. Not public marketing copy.
> Use as the source of truth for messaging consistency across all launch channels.

---

## Product Category

**Agent-readiness static analysis**

Not a security scanner. Not a code quality linter. Not a CI framework.
This is a repo governance tool for the AI-agent era: it answers whether a repo has the structural prerequisites for safe and effective AI coding-agent operation.

---

## Primary User

**Developers who are actively adopting AI coding agents** (Cursor, GitHub Copilot, Claude Code, Codex, local agents) and want to know if their repos are ready.

Secondary users:

- Platform engineers standardizing AI tooling across a team
- Dev-tool founders evaluating the governance gap in their own products
- Local-agent users who need repos that work completely offline
- AI-agent workflow builders who need repos with defined operating boundaries

---

## The Problem, Plainly Stated

When you point an AI coding agent at a repo, the agent uses the repo's structure to decide what to do, what to avoid, and how to verify its own work.

Most repos are built for humans. Humans fill in missing context from experience. Agents cannot. They operate on what is present.

Missing:

- `AGENTS.md` → no scope boundaries → agent touches things it shouldn't
- Test suite → no verification loop → agent can't self-check
- Run command → no executable entry point → agent guesses
- `.env` discipline → potential secret exposure
- CI → no pass/fail feedback on changes
- PR template → unstructured output lands in review

The result: wasted tokens, bad changes, and eroded trust in AI-assisted development.

---

## Core Emotional Hook

> **Your repo may be readable by humans but unsafe for agents.**

This is the line that stops a developer mid-scroll.

It reframes a familiar problem (messy repo) through a new lens (agent readiness), and it implies an actionable solution.

---

## Core Rational Hook

- 12 deterministic checks
- 0–100 score
- Results in under 3 seconds
- CI-ready (`--fail-under 70`)
- Zero runtime dependencies
- No LLM calls → free per run, reproducible

---

## Differentiator

**Agent governance before agent execution.**

Other tools check code quality, security vulnerabilities, or test coverage. This tool checks whether the repo is structured to guide an AI agent safely.

The concept is new: repo readiness for AI agents is not yet a recognized category. This tool defines and occupies it.

---

## The Strongest Single Line

> **Humans can infer missing context. Agents cannot.**

Use this line in every launch post. It is the fastest explanation of the product's value.

---

## Messaging Phrases — USE THESE

| Phrase | Context |
|---|---|
| **"agent-ready"** | Describing repos that pass the scan |
| **"deterministic"** | Describing the scan itself; contrast with LLM-based tools |
| **"repo governance"** | The category; use alongside "static analysis" |
| **"AI coding-agent readiness"** | The formal product category |
| **"no LLM calls"** | In every technical description |
| **"no telemetry"** | In every trust-sensitive context |
| **"structure before autonomy"** | The philosophical framing |
| **"agent boundaries"** | Describing what AGENTS.md provides |
| **"0–100 readiness score"** | Always include the score framing |

---

## Messaging Phrases — AVOID THESE

| Phrase | Why |
|---|---|
| **"ASI certified"** | Overclaim; we don't certify anything |
| **"quantum"** | Irrelevant; sounds like nonsense marketing |
| **"guaranteed safe"** | No tool can guarantee this; dangerous overclaim |
| **"security scanner"** | Creates false expectations; we are not a security tool |
| **"replaces code review"** | False and damaging to trust |
| **"fully autonomous"** | Misrepresents what the tool does |
| **"AI-powered"** | The scanner uses no AI; this would be a lie |
| **"enterprise-grade"** | Vague filler |
| **"production-ready"** | Vague filler |
| **"game-changing"** | Hype; kills credibility with developers |

---

## Future Modules (Named, Not Built)

These are named in the roadmap for narrative coherence but do not exist in v0.

**Token Burn Firewall**
Checks whether a repo's structure is likely to cause agents to waste tokens in loops.
Status: not built. Future module.

**Repo Red Cell Bot**
Automated adversarial check: simulates a bad agent PR and assesses whether repo governance would catch it.
Status: not built. Future module.

These modules extend the same category (agent governance) without contradicting the current product's positioning.

---

## Positioning Against Alternatives

| Comparison | Our position |
|---|---|
| vs. linters (ESLint, flake8) | They check code quality. We check repo structure for AI agents. |
| vs. security scanners (truffleHog, gitleaks) | They scan for leaked secrets comprehensively. We flag obvious patterns as one of 12 checks. |
| vs. GitHub Copilot itself | Copilot is the agent. We make repos ready for the agent. |
| vs. OpenAI Codex | Same as Copilot — we're the preparation layer, not the agent. |
| vs. general CI quality tools | They enforce code standards. We enforce agent governance. |

---

## Launch Status

**Hacker News launch is live:**
https://news.ycombinator.com/item?id=48213323

Treat HN as a feedback source, not command authority. Use the ops agent
(`python scripts/ops_agent.py --write`) to sort signal before selecting v0.2.
A single loud comment is not a product direction. A repeated pattern across
10+ comments is.

See [`docs/LAUNCH_LOG.md`](LAUNCH_LOG.md) for the full launch event record.

---

## Launch Positioning Summary

```
Product name:    Agent Readiness Scanner
Version:         v0.1.0
Tagline:         Is your repo ready for AI coding agents?
One-liner:       Deterministic CLI that gives your repo a 0–100 agent readiness score.
Trust signals:   no LLM calls, no telemetry, no SaaS, no account, MIT license
Distribution:    GitHub open-source, pip install, GitHub Actions usage
Target channel:  Hacker News, Reddit r/LocalLLaMA, X developer community, LinkedIn
```
