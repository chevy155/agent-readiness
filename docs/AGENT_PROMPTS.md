# Agent Prompts

Ready-to-use prompts for Cursor, Claude Code, GitHub Copilot Chat, Codex, or
local agents after running Agent Readiness Scanner.

Use these prompts to reduce scope creep. Paste the scanner output or
`AGENT_READINESS.md` where indicated.

---

## A. Fix My Agent-Readiness Score

**Input:** Paste `AGENT_READINESS.md`.

```text
You are helping improve this repository's Agent Readiness Scanner score.

Input:
[paste AGENT_READINESS.md here]

Task:
Propose the smallest set of repo changes that would improve the score.

Rules:
- Fix critical failures first.
- Do not add SaaS.
- Do not add telemetry.
- Do not add LLM calls.
- Do not add unnecessary dependencies.
- Do not rewrite unrelated code.
- Prefer docs, CI, tests, and governance files over product features.
- Return a short plan before editing.
```

---

## B. Generate Missing Governance Files

**Input:** Paste terminal scanner output.

```text
You are generating missing repo-governance files for AI coding agents.

Input:
[paste agent-scan output here]

Task:
Create or update only the missing governance files needed for agent readiness:
- AGENTS.md
- .github/copilot-instructions.md
- PR template
- issue templates

Rules:
- Match this repo's existing style.
- Do not overwrite existing content unless asked.
- Include allowed changes, forbidden changes, test commands, and boundaries.
- Do not add SaaS, telemetry, LLM calls, or new dependencies.
```

---

## C. Red-Cell My Readiness Report

**Input:** Paste `AGENT_READINESS.md`.

```text
You are red-celling this Agent Readiness report.

Input:
[paste AGENT_READINESS.md here]

Task:
Identify where the score may be misleading.

Focus on:
- Critical failures that should block agent execution
- Missing tests or weak test signals
- Missing run commands
- Ambiguous agent boundaries
- Security-looking claims that are only heuristic
- Any gap where a human can infer context but an agent cannot

Output:
- Highest-risk gap
- Why it matters for AI coding agents
- Minimal fix
- What not to build
```

---

## D. Prepare Repo for Autonomous Coding Agent

**Input:** Paste `README.md` and `AGENT_READINESS.md`.

```text
You are preparing this repo for a safe first task by an autonomous coding agent.

Input:
[paste README.md]
[paste AGENT_READINESS.md]

Task:
Create a safe first-task plan for an agent.

Rules:
- Do not start with feature work if critical failures exist.
- Prefer verification tasks first.
- Identify required commands before editing.
- Identify protected paths and forbidden changes.
- Keep the first task small and reversible.
- Include rollback and test steps.
```

---

## E. CI Integration Assistant

**Input:** Paste existing workflow files.

```text
You are adding Agent Readiness Scanner to CI.

Input:
[paste existing GitHub Actions workflow files]

Task:
Add a safe CI step that runs:

agent-scan . --fail-under 70

Rules:
- Preserve existing workflow behavior.
- Do not remove existing jobs.
- Do not add secrets.
- Do not add telemetry.
- Use the current pre-PyPI install path unless PyPI is live:
  pip install git+https://github.com/chevy155/agent-readiness.git
- Return the smallest YAML patch possible.
```

