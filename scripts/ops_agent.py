"""
ops_agent.py

Owner-only operations agent for the Agent Readiness Scanner repo.

Sweeps GitHub traffic, repo health, and local pasted feedback files,
then produces a structured Markdown improvement report.

Usage:
    python scripts/ops_agent.py
    python scripts/ops_agent.py --no-gh
    python scripts/ops_agent.py --write
    python scripts/ops_agent.py --write --feedback-dir data/feedback
    python scripts/ops_agent.py --write --output reports/my_report.md

This script:
  - Does NOT add telemetry to the scanner
  - Does NOT run automatically or on a schedule
  - Does NOT track users
  - Does NOT call LLM APIs
  - Does NOT add SaaS, billing, background jobs, or external tracking
  - Is for repo owner use only
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Bootstrap sys.path so sibling scripts are importable
# ---------------------------------------------------------------------------

_SCRIPTS_DIR = Path(__file__).parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from feedback_synthesizer import (
    build_backlog_from_categories,
    categorize_hits,
    count_keyword_frequency,
    extract_keyword_hits,
    render_feedback_section,
)
from github_traffic_report import (
    fetch_traffic,
    format_clones,
    format_paths,
    format_referrers,
    format_views,
)

REPO = "chevy155/agent-readiness"

# ---------------------------------------------------------------------------
# GitHub repo health
# ---------------------------------------------------------------------------


def fetch_repo_health(repo: str) -> dict:
    """
    Fetch stars, forks, open issues, and open PRs via gh CLI.
    Returns a dict with whatever fields succeeded.
    Never raises — partial results are returned on any failure.
    """
    result: dict = {}

    # Basic repo metadata
    r = subprocess.run(
        [
            "gh", "repo", "view", repo,
            "--json", "stargazerCount,forkCount,name,description,openIssuesCount",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if r.returncode == 0:
        try:
            result.update(json.loads(r.stdout))
        except json.JSONDecodeError:
            pass

    # Open issues
    r2 = subprocess.run(
        [
            "gh", "issue", "list", "--repo", repo,
            "--state", "open", "--limit", "20",
            "--json", "number,title,labels",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if r2.returncode == 0:
        try:
            result["open_issues_list"] = json.loads(r2.stdout)
        except json.JSONDecodeError:
            result["open_issues_list"] = []

    # Open PRs
    r3 = subprocess.run(
        [
            "gh", "pr", "list", "--repo", repo,
            "--state", "open", "--limit", "20",
            "--json", "number,title,state",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if r3.returncode == 0:
        try:
            result["open_prs_list"] = json.loads(r3.stdout)
        except json.JSONDecodeError:
            result["open_prs_list"] = []

    return result


def format_repo_health(health: dict) -> str:
    """Render repo health data as a Markdown section string."""
    lines: list[str] = ["## Repo Health Snapshot\n"]
    stars = health.get("stargazerCount", "N/A")
    forks = health.get("forkCount", "N/A")
    open_issues = health.get("openIssuesCount", len(health.get("open_issues_list", [])))
    open_prs = len(health.get("open_prs_list", []))

    lines.append(f"- Stars:       {stars}")
    lines.append(f"- Forks:       {forks}")
    lines.append(f"- Open issues: {open_issues}")
    lines.append(f"- Open PRs:    {open_prs}")
    lines.append("")

    issues = health.get("open_issues_list", [])
    if issues:
        lines.append("**Open issues:**")
        for iss in issues[:10]:
            n = iss.get("number", "?")
            t = iss.get("title", "?")
            lines.append(f"  - #{n}: {t}")
        lines.append("")

    prs = health.get("open_prs_list", [])
    if prs:
        lines.append("**Open PRs:**")
        for pr in prs[:10]:
            n = pr.get("number", "?")
            t = pr.get("title", "?")
            lines.append(f"  - #{n}: {t}")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Feedback loading
# ---------------------------------------------------------------------------


def load_feedback_files(feedback_dir: Path) -> dict[str, str]:
    """
    Read all .md and .txt files from feedback_dir.
    Returns {filename: content}.
    Silently skips empty directories, missing directories, and empty files.
    """
    if not feedback_dir.exists():
        return {}
    result: dict[str, str] = {}
    for p in sorted(feedback_dir.iterdir()):
        if p.suffix in {".md", ".txt"} and p.is_file() and p.stat().st_size > 0:
            try:
                result[p.name] = p.read_text(encoding="utf-8", errors="replace")
            except OSError:
                pass
    return result


# ---------------------------------------------------------------------------
# Report rendering
# ---------------------------------------------------------------------------

_DIVIDER = "─" * 60


def render_full_report(
    traffic: dict | None,
    health: dict | None,
    feedback_files: dict[str, str],
    repo: str,
    timestamp: str,
) -> str:
    """
    Compose the full Markdown ops report.
    All inputs are optional — missing data is noted gracefully.
    Pure function: no I/O, no network.
    """
    parts: list[str] = []

    # Header
    parts.append(f"# Ops Report — {repo}\n\n**Generated:** {timestamp}\n\n")
    parts.append(_DIVIDER + "\n\n")

    # Executive summary
    parts.append("## Executive Summary\n\n")
    summary_lines: list[str] = []

    if traffic:
        v = traffic.get("views", {})
        c = traffic.get("clones", {})
        summary_lines.append(
            f"- **Views (14d):** {v.get('count', 0):,} total, "
            f"{v.get('uniques', 0):,} unique visitors"
        )
        summary_lines.append(
            f"- **Clones (14d):** {c.get('count', 0):,} total, "
            f"{c.get('uniques', 0):,} unique cloners"
        )
    else:
        summary_lines.append("- Traffic: not fetched (`--no-gh` or gh unavailable)")

    if health:
        summary_lines.append(
            f"- **Stars:** {health.get('stargazerCount', 'N/A')} | "
            f"**Forks:** {health.get('forkCount', 'N/A')} | "
            f"**Open issues:** {health.get('openIssuesCount', len(health.get('open_issues_list', [])))}"
        )
    else:
        summary_lines.append("- Repo health: not fetched")

    if feedback_files:
        summary_lines.append(
            f"- **Feedback files:** {len(feedback_files)} "
            f"({', '.join(feedback_files.keys())})"
        )
    else:
        summary_lines.append(
            "- Feedback: none — paste launch comments into `data/feedback/*.md` and re-run"
        )

    parts.append("\n".join(summary_lines) + "\n\n")

    # Traffic section
    if traffic:
        parts.append("## Traffic Snapshot (14 days)\n\n")
        parts.append(format_views(traffic.get("views", {})) + "\n")
        parts.append(format_clones(traffic.get("clones", {})) + "\n\n")
        parts.append(format_referrers(traffic.get("referrers", [])) + "\n\n")
        parts.append(format_paths(traffic.get("paths", [])) + "\n\n")
    else:
        parts.append("## Traffic Snapshot\n\n> Not fetched (`--no-gh` or gh unavailable).\n\n")

    # Repo health section
    if health:
        parts.append(format_repo_health(health) + "\n")
    else:
        parts.append(
            "## Repo Health Snapshot\n\n> Not fetched (`--no-gh` or gh unavailable).\n\n"
        )

    # Feedback section
    if feedback_files:
        combined = "\n\n".join(
            f"=== {fname} ===\n{content}"
            for fname, content in feedback_files.items()
        )
        hits = extract_keyword_hits(combined)
        freq = count_keyword_frequency(hits)
        categories = categorize_hits(hits)
        backlog = build_backlog_from_categories(categories, freq)

        parts.append(render_feedback_section(categories, backlog, freq) + "\n")

        # Recommended v0.2 action
        parts.append("## Recommended v0.2 Action\n\n")
        if backlog:
            top = backlog[0]
            parts.append(f"**{top.title}** — priority score: {top.score}\n\n")
            if top.evidence:
                parts.append("Evidence:\n")
                for e in top.evidence[:3]:
                    parts.append(f"- {e}\n")
        else:
            parts.append(
                "> No clear signal from feedback. Default recommendation: "
                "**Critical Failures Banner** — surface security/secret failures "
                "visually above the score so they cannot hide inside a passing total.\n"
            )
        parts.append("\n")

        # Repeated objections
        parts.append("## Repeated Objections\n\n")
        high_freq = {kw: n for kw, n in freq.items() if n >= 2}
        if high_freq:
            for kw, n in sorted(high_freq.items(), key=lambda x: -x[1]):
                parts.append(f"- `{kw}` — mentioned {n} time(s)\n")
        else:
            parts.append("> No keyword appeared more than once in this feedback batch.\n")
        parts.append("\n")

        # Do-not-build list
        parts.append("## Do-Not-Build List\n\n")
        scope_risks = [i for i in backlog if i.category == "Scope-risk idea"]
        if scope_risks:
            parts.append(
                "The following topics were flagged as scope-risk ideas. "
                "Review carefully before building.\n\n"
            )
            for item in scope_risks:
                ev = "; ".join(item.evidence[:2]) if item.evidence else ""
                parts.append(f"- **{item.title}**{': ' + ev if ev else ''}\n")
        else:
            parts.append("> No scope-risk ideas found in this feedback batch.\n")
        parts.append("\n")

    else:
        parts.append(
            "## Feedback Analysis\n\n"
            "> No feedback files found in `data/feedback/`.\n"
            "> Paste exported HN/Reddit/LinkedIn/X comments into "
            "`data/feedback/*.md` files and re-run.\n\n"
        )
        parts.append(
            "## Recommended v0.2 Action\n\n"
            "> No feedback yet. Default recommendation: **Critical Failures Banner** — "
            "surface security/secret failures visually above the score so they cannot "
            "hide inside a passing total.\n\n"
        )
        parts.append("## Do-Not-Build List\n\n> No feedback to evaluate scope risks.\n\n")

    # Final verdict
    parts.append("## Final Go / No-Go\n\n")
    parts.append(
        "> Re-run this report after pasting launch feedback into `data/feedback/`. "
        "The first clear top-3 backlog items after a real launch batch are the "
        "only valid trigger for a v0.2 build decision.\n\n"
    )
    parts.append(_DIVIDER + "\n\n")
    parts.append("*Generated by `scripts/ops_agent.py` — owner-only, no telemetry.*\n")

    return "".join(parts)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Agent Readiness Ops Agent — sweeps GitHub health, traffic, "
            "and local feedback, then produces an improvement report."
        ),
        epilog="Owner-only tool. No telemetry. Does not run automatically.",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write the report to reports/OPS_REPORT_YYYY_MM_DD.md",
    )
    parser.add_argument(
        "--feedback-dir",
        default="data/feedback",
        metavar="DIR",
        help="Directory containing feedback .md/.txt files (default: data/feedback)",
    )
    parser.add_argument(
        "--no-gh",
        action="store_true",
        help="Skip all GitHub API calls (useful when gh is unavailable)",
    )
    parser.add_argument(
        "--output",
        default=None,
        metavar="PATH",
        help="Override output path when --write is set",
    )
    parser.add_argument(
        "--repo",
        default=REPO,
        help=f"Repository slug (default: {REPO})",
    )
    args = parser.parse_args(argv)

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    now = datetime.now(timezone.utc)
    timestamp = now.strftime("%Y-%m-%d %H:%M UTC")
    date_str = now.strftime("%Y_%m_%d")
    repo_root = Path(__file__).parent.parent
    feedback_dir = repo_root / args.feedback_dir

    # --- GitHub metrics ---
    traffic: dict | None = None
    health: dict | None = None

    if not args.no_gh:
        print("Fetching GitHub traffic...", file=sys.stderr)
        try:
            views, clones, referrers, paths = fetch_traffic(args.repo)
            traffic = {
                "views": views,
                "clones": clones,
                "referrers": referrers,
                "paths": paths,
            }
        except FileNotFoundError:
            print("  gh CLI not found — skipping traffic.", file=sys.stderr)
        except RuntimeError as e:
            print(f"  Traffic fetch failed: {e}", file=sys.stderr)

        print("Fetching repo health...", file=sys.stderr)
        try:
            health = fetch_repo_health(args.repo)
        except Exception as e:
            print(f"  Repo health fetch failed: {e}", file=sys.stderr)
    else:
        print("Skipping GitHub metrics (--no-gh).", file=sys.stderr)

    # --- Feedback ---
    feedback_files = load_feedback_files(feedback_dir)
    if feedback_files:
        print(
            f"Loaded {len(feedback_files)} feedback file(s): "
            f"{', '.join(feedback_files.keys())}",
            file=sys.stderr,
        )
    else:
        print(
            "No feedback files found — paste comments into data/feedback/*.md to enable analysis.",
            file=sys.stderr,
        )

    # --- Render ---
    report = render_full_report(traffic, health, feedback_files, args.repo, timestamp)

    # --- Terminal summary ---
    print()
    print(_DIVIDER)
    print(f"  Agent Readiness Ops Report — {args.repo}")
    print(f"  {timestamp}")
    print(_DIVIDER)
    if traffic:
        v = traffic.get("views", {})
        c = traffic.get("clones", {})
        print(f"  Views (14d):   {v.get('count', 0):,} total  |  {v.get('uniques', 0):,} unique")
        print(f"  Clones (14d):  {c.get('count', 0):,} total  |  {c.get('uniques', 0):,} unique")
    else:
        print("  Traffic:       not fetched")
    if health:
        print(f"  Stars:         {health.get('stargazerCount', 'N/A')}")
        oi = health.get("openIssuesCount", len(health.get("open_issues_list", [])))
        print(f"  Open issues:   {oi}")
    else:
        print("  Repo health:   not fetched")
    if feedback_files:
        print(f"  Feedback files: {len(feedback_files)}")
    else:
        print("  Feedback files: 0  (paste into data/feedback/*.md)")
    print(_DIVIDER)
    print()

    # --- Write ---
    if args.write:
        output_path_str = args.output or f"reports/OPS_REPORT_{date_str}.md"
        output_path = repo_root / output_path_str
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding="utf-8")
        print(f"Report written to: {output_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
