# Ops Agent — Agent Readiness Scanner

> Owner-only post-launch radar. Sweeps GitHub traffic, repo health, and
> pasted launch feedback, then produces a structured improvement report.

---

## What It Does

`scripts/ops_agent.py` is a manual-run operations tool for the repo owner.
After a launch post (Show HN, Reddit, LinkedIn, X), you paste the comments
into `data/feedback/` and run the agent. It tells you:

- What people looked at (GitHub traffic: views, clones, top referrers, top paths)
- What they complained about (keyword-matched feedback categories)
- What confused them (Documentation confusion category)
- What feature requests repeated (Feature request category + frequency count)
- What would increase adoption (ranked backlog by priority score)
- What to ignore (low-signal feedback and scope-risk ideas)
- What the next smallest v0.2 improvement is (top backlog item)

---

## What It Does NOT Do

- Does not add telemetry to the scanner
- Does not run automatically or on a schedule
- Does not track users
- Does not call any LLM API
- Does not scrape social media websites
- Does not add SaaS, billing, background jobs, or external tracking
- Does not write to GitHub or modify repo files (except the report, when `--write` is passed)

---

## How to Paste Feedback

After your launch post, copy comments from the platform and paste them into a
Markdown file in `data/feedback/`. One file per source:

```
data/feedback/
  hackernews.md     ← paste HN thread comments here
  reddit_localllama.md
  reddit_devops.md
  linkedin.md
  x.md
  github_issues.md  ← copy open issue titles and bodies
  manual_notes.md   ← your own observations
```

**Format:** plain text or Markdown. The agent reads every line.
No structure required — paste raw comments, it will find the signal.

**Example — data/feedback/hackernews.md:**

```
would be great to have this on pypi
does it support node / npm repos?
false positive on my README — it has a Bearer token in a curl example
love that there's no telemetry, most tools phone home
error on windows when running with emoji in paths
```

---

## How to Run It

```bash
# Terminal summary only (no file written)
python scripts/ops_agent.py

# Skip GitHub API calls (when gh is not available)
python scripts/ops_agent.py --no-gh

# Write report to reports/OPS_REPORT_YYYY_MM_DD.md
python scripts/ops_agent.py --write

# Full run with specific feedback directory
python scripts/ops_agent.py --write --feedback-dir data/feedback

# Override output path
python scripts/ops_agent.py --write --output reports/my_custom_report.md
```

Requires `gh` CLI installed and authenticated with repo read access
for GitHub metrics. If `gh` is unavailable, use `--no-gh` and the
agent skips GitHub calls gracefully.

---

## How to Interpret the Report

```
reports/OPS_REPORT_YYYY_MM_DD.md
```

### Executive Summary
Quick snapshot of views, clones, stars, and feedback file count.

### Traffic Snapshot (14 days)
GitHub traffic: total views, unique visitors, total clones, unique cloners,
top referrers, and top paths. Covers the past 14 days only (GitHub API limit).

### Repo Health Snapshot
Stars, forks, open issues, open PRs.

### Feedback Analysis — Keyword Frequency
Table of all keywords found in feedback, sorted by frequency.
High-frequency keywords are the strongest signal.

### Feedback Analysis — Categories
Lines from feedback grouped into:

| Category | Meaning |
|---|---|
| **Installation friction** | Problems installing or running the tool |
| **Trust/safety concern** | Worries about telemetry, secrets, LLMs |
| **Feature request** | Things people want added |
| **Bug report** | Something broke |
| **Documentation confusion** | What wasn't clear |
| **Distribution signal** | Mentions of target tools (Cursor, Copilot, etc.) |
| **Scope-risk idea** | Things that sound good but could break scope |
| **Ignore/noise** | Unmatched or low-value lines |

### Improvement Backlog (Top 5)
Ranked table of categories with hits.

Priority score = `frequency + severity + adoption_impact - scope_risk - effort`

Higher score = higher priority. Scores are heuristic starting points;
adjust manually in the report before acting.

### Recommended v0.2 Action
The top-scoring backlog item. This is the one thing to build next.

### Repeated Objections
Keywords that appeared more than once. These are the strongest signals.

### Do-Not-Build List
Scope-risk ideas from feedback — things that sound appealing but could
expand scope beyond the product's core. Review carefully before building.

---

## Why It Does Not Scrape Social Sites

Scraping requires third-party APIs or browser automation:
- Adds external dependencies
- Requires API keys (Hacker News, Reddit, LinkedIn, X all have rate limits)
- Creates privacy and ToS risks
- Is fragile and breaks silently

Pasting feedback manually is slower but:
- Requires no credentials
- Has no rate limits
- Is deterministic
- Forces the operator to actually read the comments (which prevents reactive over-building)

---

## Why It Does Not Auto-Build Features

The ops agent is a **sorting machine**, not a builder.

Automated feature suggestion from feedback → automated building is the
fastest way to expand scope in the wrong direction. The correct loop is:

1. Launch
2. Wait 24–48 hours for feedback
3. Paste feedback into `data/feedback/`
4. Run ops agent
5. Read the report — especially the **Do-Not-Build List**
6. Make a conscious decision about v0.2
7. Build only the single highest-signal item

The agent tells you what to build. You decide whether to build it.

---

## Running Tests

```bash
python -m pytest tests/test_ops_agent.py -q
```

All tests use mocked input. No network calls. No gh CLI required.

---

## Files

| File | Role |
|---|---|
| `scripts/ops_agent.py` | Main CLI — orchestrates GitHub fetch, feedback load, report render |
| `scripts/feedback_synthesizer.py` | Pure functions — keyword extraction, categorization, backlog scoring |
| `scripts/github_traffic_report.py` | Traffic fetcher — reused for views/clones/referrers/paths |
| `data/feedback/` | Drop feedback files here before running |
| `reports/OPS_REPORT_YYYY_MM_DD.md` | Generated report (created with `--write`) |
| `reports/OPS_REPORT_TEMPLATE.md` | Blank template showing report structure |
| `tests/test_ops_agent.py` | Test suite — feedback_synthesizer + ops_agent formatting |
