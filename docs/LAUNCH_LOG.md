# Launch Log — Agent Readiness Scanner

> Canonical record of public launch events.
> Update this file each time a new post goes live.

---

## v0.1.0 Launch — 2026-05-20

### Hacker News — Show HN

**Status:** LIVE

**Submission thread:** https://news.ycombinator.com/item?id=48213323

**Owner profile / thread page:** https://news.ycombinator.com/threads?id=chevy155

**Title:** Show HN: Agent Readiness Scanner – Check if your repo is ready for AI coding agents

**Body summary:**
> I built Agent Readiness Scanner, a small open-source CLI that answers one question: Is your repo actually ready for AI coding agents? Humans can infer missing context. Agents cannot.

**Next action:** Wait ~24 hours. Paste HN comments into `data/feedback/hackernews.md`. Run `python scripts/ops_agent.py --write`. Read the ops report before making any v0.2 decision.

---

### GitHub

**Status:** LIVE

**Repo:** https://github.com/chevy155/agent-readiness

**Release:** https://github.com/chevy155/agent-readiness/releases/tag/v0.1.0

**CI:** Passing on Python 3.9, 3.10, 3.11, 3.12

---

### Other Channels (pending)

| Channel | Status | URL |
|---|---|---|
| Reddit r/LocalLLaMA | pending | — |
| Reddit r/devops | pending | — |
| X/Twitter | pending | — |
| LinkedIn | pending | — |

---

## Feedback Protocol

Do not build anything in the 24 hours after launch unless a true bug surfaces.

1. Check HN thread: https://news.ycombinator.com/item?id=48213323
2. Copy useful comments manually into `data/feedback/hackernews.md`
3. Run `python scripts/ops_agent.py --write`
4. Read `reports/OPS_REPORT_YYYY_MM_DD.md`
5. Make a conscious v0.2 decision from the ops report — not from emotional response to individual comments

**The first likely v0.2:** Critical Failures Banner. The ops agent will confirm or deny this after real feedback arrives.

---

## Operating Rule

> Treat Hacker News as a feedback source, not command authority.
> Use the ops agent to sort signal before selecting v0.2.
> A single loud comment is not a product direction.
> A repeated pattern across 10+ comments is.
