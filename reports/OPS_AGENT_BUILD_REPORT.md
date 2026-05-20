# Ops Agent Build Report

**Date:** 2026-05-20
**Phase:** Post-launch radar build
**Trigger:** Launch complete → need a sorting machine for feedback before v0.2 decisions

---

## Files Created

| File | Role |
|---|---|
| `scripts/feedback_synthesizer.py` | Pure functions: keyword extraction, categorization, priority scoring, backlog building, Markdown rendering |
| `scripts/ops_agent.py` | CLI orchestrator: GitHub traffic, repo health, feedback load, report render |
| `tests/test_ops_agent.py` | 56 tests covering all feedback_synthesizer functions + ops_agent formatting |
| `docs/OPS_AGENT.md` | Full documentation: what it does, what it doesn't, how to paste feedback, how to run, how to interpret |
| `reports/OPS_REPORT_TEMPLATE.md` | Blank template showing report structure |
| `data/feedback/.gitkeep` | Holds the feedback directory in git |

**Also fixed:**
- `scripts/github_traffic_report.py` — replaced deprecated `datetime.utcnow()` with `datetime.now(timezone.utc)`
- `scripts/ops_agent.py` — same fix applied on creation

---

## Architecture

```
ops_agent.py
├── imports feedback_synthesizer.py  (pure functions, no I/O)
├── imports github_traffic_report.py (reuses existing fetch_traffic + formatters)
│
├── fetch_repo_health()      → gh repo view + gh issue list + gh pr list
├── format_repo_health()     → pure Markdown formatter
├── load_feedback_files()    → reads data/feedback/*.md and *.txt
└── render_full_report()     → pure composition of all sections

feedback_synthesizer.py
├── extract_keyword_hits()   → {keyword: [matching_lines]}
├── categorize_hits()        → {category: [lines]}
├── count_keyword_frequency() → {keyword: count}
├── priority_score()         → int (freq + sev + adop - srisk - effort)
├── BacklogItem              → dataclass with auto-computed .score
├── build_backlog_from_categories() → [BacklogItem] sorted by score desc
└── render_feedback_section() → Markdown string
```

No external dependencies added. Zero runtime dependencies.

---

## Feedback Keywords Tracked (23)

`install`, `pip`, `pypi`, `windows`, `error`, `github action`, `badge`,
`false positive`, `secret`, `security`, `docker`, `node`, `npm`, `docs`,
`example`, `pricing`, `telemetry`, `llm`, `agent`, `cursor`, `copilot`,
`claude`, `codex`

---

## Category → Priority Heuristics

| Category | Sev | Adop | SRisk | Effort | Notes |
|---|---|---|---|---|---|
| Installation friction | 4 | 5 | 1 | 2 | Highest adoption impact |
| Trust/safety concern | 4 | 4 | 2 | 2 | High — trust is the product's core claim |
| Feature request | 2 | 3 | 3 | 3 | Mid — evaluate scope risk before building |
| Bug report | 5 | 5 | 1 | 3 | Always fix bugs |
| Documentation confusion | 3 | 4 | 1 | 1 | Cheap to fix, high adoption return |
| Distribution signal | 1 | 3 | 1 | 1 | Positive signal, no action needed |
| Scope-risk idea | 2 | 2 | 5 | 5 | Route to Do-Not-Build List |
| Ignore/noise | 1 | 1 | 1 | 1 | True noise |

---

## Commands Run

```bash
python -m pytest -q
# → 185 passed

python scripts/ops_agent.py --no-gh
# → Terminal summary, no file written, exit 0

python scripts/ops_agent.py --no-gh --write
# → Terminal summary + reports/OPS_REPORT_2026_05_20.md written, exit 0
```

---

## Test Results

```
185 passed in 1.13s
```

Test breakdown:
- `tests/test_ops_agent.py` — **56 new tests**
  - `TestExtractKeywordHits` (10 tests)
  - `TestCategorizeHits` (8 tests)
  - `TestCountKeywordFrequency` (3 tests)
  - `TestPriorityScore` (6 tests)
  - `TestBacklogItem` (2 tests)
  - `TestBuildBacklogFromCategories` (5 tests)
  - `TestRenderFeedbackSection` (5 tests)
  - `TestLoadFeedbackFiles` (6 tests)
  - `TestRenderFullReport` (8 tests)
  - `TestFormatRepoHealth` (3 tests)

---

## Example Report Path

```
reports/OPS_REPORT_2026_05_20.md
```

Empty report (no feedback files, --no-gh) generated successfully. Shows:
- "no traffic fetched" placeholders
- "no feedback" placeholders
- Default v0.2 recommendation: **Critical Failures Banner**

---

## Known Limitations

- Feedback synthesis is keyword-based and deterministic, not semantic. A comment like "I love that it works great" that happens to contain "error" anywhere will be included. Operators should sanity-check evidence lines before acting.
- Priority scores are heuristic defaults. The table is a starting point; override manually in the report.
- `--no-gh` skips all GitHub API calls. The feedback-only mode is still useful for post-launch comment analysis.
- `data/feedback/` must be populated manually. No scraping, no API integration.
- The agent does not de-duplicate identical comments pasted across multiple files. If the same comment appears in `hackernews.md` and `manual_notes.md`, it counts twice.

---

## Council Closeout

**CEO verdict:**
Scope protected. The ops agent is a sorting machine, not a builder. It does not add telemetry, does not run automatically, and does not call LLMs. It surfaces signal from real launch feedback and routes scope-risk ideas to a Do-Not-Build List. The product's core trust signals are unchanged.

**CTO verdict:**
Architecture is clean. `feedback_synthesizer.py` is pure functions with no I/O — fully unit-testable. `ops_agent.py` imports from both sibling scripts cleanly. Zero new runtime dependencies. `datetime.utcnow()` deprecation fixed in both scripts. 185 tests pass.

**Ops Agent verdict:**
Ready for use after the Show HN launch. Workflow: launch → wait 24h → paste HN/Reddit comments into `data/feedback/` → run `python scripts/ops_agent.py --write` → read `reports/OPS_REPORT_YYYY_MM_DD.md` → decide on v0.2. The default v0.2 recommendation in the empty report is Critical Failures Banner — which aligns with the pre-launch assessment.

**Verification:**
- `python -m pytest -q` → **185 passed**
- `python scripts/ops_agent.py --no-gh` → terminal summary, exit 0
- `python scripts/ops_agent.py --no-gh --write` → report written, exit 0

**Known limitations:** See above.

**Next move:**
Launch Show HN. Wait 24 hours. Paste comments. Run the ops agent. Let the market tell you what v0.2 should be.

**Final go/no-go: GO.**
