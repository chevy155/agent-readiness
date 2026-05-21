# Agent Use Cases

Agent Readiness Scanner is deterministic agent preflight infrastructure. Use it
before Claude, Cursor, Copilot, Codex, or local agents modify a repo.

---

## Cursor User Preparing a Repo

**Problem:** You want Cursor to make changes, but the repo has unclear commands,
weak tests, or missing repo instructions.

**Command to run:**

```bash
agent-scan .
```

**Expected output:** A terminal score, readiness tier, critical failure count,
and top fixes.

**Next action:** Fix critical failures first, then run `agent-scan . --generate`
if `AGENTS.md` or Copilot instructions are missing.

---

## Claude Code User Before Autonomous Edits

**Problem:** Claude Code can modify a repo, but it needs boundaries, tests, and
safe operating context.

**Command to run:**

```bash
agent-scan . --output markdown
```

**Expected output:** `AGENT_READINESS.md` with score, check table, critical
failures, and recommendations.

**Next action:** Paste `AGENT_READINESS.md` into Claude and ask for a minimal
repair plan before giving it edit authority.

---

## GitHub Copilot User Adding Repo Instructions

**Problem:** Copilot lacks project-specific instructions and may infer style or
scope incorrectly.

**Command to run:**

```bash
agent-scan . --generate
```

**Expected output:** Starter `AGENTS.md` and `.github/copilot-instructions.md`
if missing. Existing files are not overwritten.

**Next action:** Review and customize the generated instructions for the repo's
real commands, style, and forbidden paths.

---

## Local Ollama / LM Studio User Working Offline

**Problem:** You are using a local coding model and need the repo to be
self-describing without cloud APIs.

**Command to run:**

```bash
agent-scan . --no-color
```

**Expected output:** Offline terminal output with deterministic score and no
network calls.

**Next action:** Fix missing tests, run commands, or agent instructions before
letting the local agent edit files.

---

## Engineering Team Gating Agent Readiness in CI

**Problem:** A team wants a repeatable gate before agents work on production
repos.

**Command to run:**

```bash
agent-scan . --fail-under 70
```

**Expected output:** Exit code `0` if the repo meets the threshold, `1` if it
does not.

**Next action:** Add the command to CI and treat critical failures as blockers,
even if the score is above threshold.

---

## Open-Source Maintainer Improving Contributor Guidance

**Problem:** Contributors and agents both need clearer contribution paths.

**Command to run:**

```bash
agent-scan . --output markdown
```

**Expected output:** `AGENT_READINESS.md` showing missing templates,
instructions, or boundaries.

**Next action:** Add `AGENTS.md`, PR templates, issue templates, and documented
test commands.

---

## Startup CTO Preparing Repos for AI-Assisted Development

**Problem:** Multiple repos may be readable by humans but under-specified for
agent workflows.

**Command to run:**

```bash
agent-scan /path/to/repo --output json
```

**Expected output:** Structured JSON with score, tier, checks,
`critical_failures_present`, and recommendations.

**Next action:** Use JSON output to inventory repos, fix critical failures first,
then standardize governance files across the highest-value repos.

