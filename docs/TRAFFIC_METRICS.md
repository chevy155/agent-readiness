# Traffic Metrics — Agent Readiness Scanner

> How to understand GitHub repository traffic data after launch.
> This repo does not track users. The scanner has no telemetry.

---

## What GitHub Traffic Tells You

GitHub provides repository-level traffic data to users with write access. It covers:

| Metric | What it means |
|---|---|
| **Views (total)** | Total page impressions on the repo in the past 14 days |
| **Views (unique visitors)** | Number of distinct GitHub accounts or IP-based anonymous visitors |
| **Clones (total)** | Total `git clone` operations in the past 14 days |
| **Clones (unique cloners)** | Number of distinct accounts or IPs that cloned |
| **Top referrers** | Sites/sources that sent traffic (e.g., news.ycombinator.com, reddit.com) |
| **Top paths** | Which pages or files were most viewed within the repo |

---

## Important Limits

- **Window is 14 days only.** GitHub does not store all-time view history through the traffic API.
- **Data is owner-private.** Only users with write access to the repo can see it.
- **Anonymous traffic is estimated.** GitHub groups unauthenticated visitors by IP and may not count all bots.
- **Clones vs. pip installs are different.** PyPI has separate download stats (installable via `pypistats`).

---

## How to Access Traffic

**Option 1 — Private script (recommended):**

```bash
python scripts/github_traffic_report.py
```

Prints views, clones, top referrers, and top paths. Requires `gh` CLI with repo read access.

**Option 2 — GitHub UI:**

Go to https://github.com/chevy155/agent-readiness/graphs/traffic

**Option 3 — GitHub CLI directly:**

```bash
gh api repos/chevy155/agent-readiness/traffic/views
gh api repos/chevy155/agent-readiness/traffic/clones
gh api repos/chevy155/agent-readiness/traffic/popular/referrers
gh api repos/chevy155/agent-readiness/traffic/popular/paths
```

---

## What Good Numbers Look Like After a Show HN Post

| Day | Expected range | Notes |
|---|---|---|
| Day 1 (HN post day) | 200–2000 views | Varies by HN ranking |
| Day 2 | 50–300 views | Tail traffic from HN |
| Day 3–7 | 20–100 views/day | Reddit + referral tail |
| Week 2+ | 5–30 views/day | Organic search, referrals |

These are rough benchmarks. A dev-tool CLI with no demo video typically converts 1–5% of viewers to cloners.

---

## What This Repo Does NOT Do

- **No visitor tracking inside the scanner.** `agent-scan` does not make any network calls. It scans local files only.
- **No telemetry.** There is no beacon, analytics endpoint, or usage tracking anywhere in the codebase.
- **No public view counter badge.** A public "visitors" badge requires a third-party tracking service (e.g., hits.seeyoufarm.com), which conflicts with the scanner's trust signal. Do not add this in v0.1 or v0.2.
- **No third-party pixel or CDN tracking.** The README loads only GitHub-hosted badges (GitHub Actions, shields.io).

---

## When to Add a Download Count Badge

PyPI publishes download statistics. After the package has real installs, you can add a truthful badge:

```markdown
[![PyPI Downloads](https://img.shields.io/pypi/dm/agent-readiness.svg)](https://pypi.org/project/agent-readiness/)
```

Do not add this until the package is on PyPI and has at least a few hundred downloads. An empty counter weakens the impression.

---

## Future: PyPI Download Tracking

If the package is published to PyPI, install `pypistats`:

```bash
pip install pypistats
pypistats recent agent-readiness
```

Or check https://pypistats.org/packages/agent-readiness.

---

## Cadence for Monitoring After Launch

| When | Action |
|---|---|
| 2 hours after HN post | Run `github_traffic_report.py`, note top referrers |
| 24 hours after HN post | Re-run, check clone count, identify top paths |
| 48 hours after each launch post | Run again, compare to prior snapshot |
| Weekly after first month | Run weekly to track organic baseline |

Write snapshots to disk with `--write` to compare over time.
