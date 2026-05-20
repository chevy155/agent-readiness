# Launch Checklist — Agent Readiness Scanner

> Step-by-step checklist to maximize GitHub visibility after the initial push.
> Complete in order. Most steps take less than 5 minutes.

---

## 1. Set Repo Description and Homepage

Run this with the GitHub CLI:

```bash
gh repo edit chevy155/agent-readiness \
  --description "Deterministic repo readiness scanner for AI coding agents." \
  --homepage "https://github.com/chevy155/agent-readiness"
```

Verify it applied:

```bash
gh repo view chevy155/agent-readiness --json description,homepageUrl
```

---

## 2. Add Topics

The GitHub CLI supports topic editing. Run:

```bash
gh repo edit chevy155/agent-readiness --add-topic ai-agents
gh repo edit chevy155/agent-readiness --add-topic coding-agents
gh repo edit chevy155/agent-readiness --add-topic cursor
gh repo edit chevy155/agent-readiness --add-topic github-copilot
gh repo edit chevy155/agent-readiness --add-topic claude-code
gh repo edit chevy155/agent-readiness --add-topic codex
gh repo edit chevy155/agent-readiness --add-topic developer-tools
gh repo edit chevy155/agent-readiness --add-topic repo-governance
gh repo edit chevy155/agent-readiness --add-topic agent-readiness
gh repo edit chevy155/agent-readiness --add-topic python-cli
gh repo edit chevy155/agent-readiness --add-topic static-analysis
gh repo edit chevy155/agent-readiness --add-topic devops
```

Or all at once using the REST API:

```bash
gh api --method PUT repos/chevy155/agent-readiness/topics \
  --field "names[]=ai-agents" \
  --field "names[]=coding-agents" \
  --field "names[]=cursor" \
  --field "names[]=github-copilot" \
  --field "names[]=claude-code" \
  --field "names[]=codex" \
  --field "names[]=developer-tools" \
  --field "names[]=repo-governance" \
  --field "names[]=agent-readiness" \
  --field "names[]=python-cli" \
  --field "names[]=static-analysis" \
  --field "names[]=devops"
```

**Manual alternative:**
Go to https://github.com/chevy155/agent-readiness → About section → gear icon → Topics → add each topic above.

---

## 3. Confirm CI Is Passing

```bash
gh run list --repo chevy155/agent-readiness --limit 5
```

All 4 matrix jobs (Python 3.9, 3.10, 3.11, 3.12) should show ✓.

If any are failing:

```bash
gh run view --repo chevy155/agent-readiness --log-failed
```

---

## 4. Confirm Tag Exists

```bash
gh release list --repo chevy155/agent-readiness
```

If `v0.1.0` is not listed as a release (just a tag), create a GitHub Release:

```bash
gh release create v0.1.0 \
  --repo chevy155/agent-readiness \
  --title "v0.1.0 — Initial Release" \
  --notes "First public release of Agent Readiness Scanner.

## What's included
- 12 deterministic checks
- 0–100 readiness score
- GREEN / YELLOW / ORANGE / RED tiers
- Terminal, JSON, and Markdown output modes
- \`--generate\` to create AGENTS.md and copilot-instructions.md
- \`--fail-under\` for CI gating
- \`--no-color\` and NO_COLOR env var support
- 108 tests passing, Python 3.9–3.12

## Install
\`\`\`
pip install agent-readiness
agent-scan .
\`\`\`"
```

---

## 5. Self-Scan and Update Repo

```bash
cd /path/to/agent-readiness
agent-scan . --output terminal
```

Expected: 100/100 GREEN. If not, fix before launching.

Generate the latest `AGENT_READINESS.md` and commit it:

```bash
agent-scan . --output markdown
git add AGENT_READINESS.md
git commit -m "docs: add AGENT_READINESS.md from self-scan"
git push
```

---

## 6. Launch Posts

See [`docs/LAUNCH_POSTS.md`](LAUNCH_POSTS.md) for ready-to-use copy for:

- LinkedIn
- X/Twitter (short post + thread)
- Hacker News / Show HN
- Reddit r/LocalLLaMA
- Reddit r/devops
- Agent-native post

**Recommended launch order:**
1. Post Show HN first (weekday morning)
2. Reddit r/LocalLLaMA same day
3. X/Twitter thread after HN is live
4. LinkedIn 1-2 days later (different audience)
5. Reddit r/devops after initial traction data

---

## 7. Check Traffic After Launch

After each launch post, run the private traffic report:

```bash
python scripts/github_traffic_report.py
```

Or write a snapshot to disk:

```bash
python scripts/github_traffic_report.py --write
```

See [`docs/TRAFFIC_METRICS.md`](TRAFFIC_METRICS.md) for what the numbers mean.

---

## 8. Post-Launch Repo Health

After each traffic spike, re-run the self-scan to confirm nothing drifted:

```bash
agent-scan . --fail-under 85
python -m pytest -q
```

---

## Status Tracker

| Step | Task | Done |
|---|---|---|
| 1 | Set description and homepage via `gh repo edit` | ☐ |
| 2 | Add 12 topics via `gh api` or GitHub UI | ☐ |
| 3 | Confirm CI passing on all 4 Python versions | ☐ |
| 4 | Create GitHub Release for v0.1.0 | ☐ |
| 5 | Self-scan, commit AGENT_READINESS.md | ☐ |
| 6 | Post Show HN | ☐ |
| 7 | Post Reddit r/LocalLLaMA | ☐ |
| 8 | Post X/Twitter thread | ☐ |
| 9 | Post LinkedIn | ☐ |
| 10 | Check traffic report 24h after HN post | ☐ |
