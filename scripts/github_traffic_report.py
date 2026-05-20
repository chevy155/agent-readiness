"""
github_traffic_report.py

Private traffic reporting script for repo owners.
Fetches GitHub repository traffic metrics using the GitHub CLI (gh).

Usage:
    python scripts/github_traffic_report.py
    python scripts/github_traffic_report.py --write   # also writes reports/GITHUB_TRAFFIC_REPORT.md

Requirements:
    - gh CLI installed and authenticated with repo read access
    - Run manually by repo owner; never runs during agent-scan

This script does NOT:
    - store tokens or credentials
    - write telemetry
    - run during repository scans
    - make network calls unless explicitly invoked
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


REPO = "chevy155/agent-readiness"


# ---------------------------------------------------------------------------
# Pure formatting helpers (testable without network)
# ---------------------------------------------------------------------------


def format_views(data: dict) -> str:
    """Format the /traffic/views API response into a human-readable string."""
    total = data.get("count", 0)
    unique = data.get("uniques", 0)
    return f"Views (14 days):   {total:,} total  |  {unique:,} unique visitors"


def format_clones(data: dict) -> str:
    """Format the /traffic/clones API response into a human-readable string."""
    total = data.get("count", 0)
    unique = data.get("uniques", 0)
    return f"Clones (14 days):  {total:,} total  |  {unique:,} unique cloners"


def format_referrers(data: list[dict]) -> str:
    """Format the /traffic/popular/referrers API response."""
    if not data:
        return "Top referrers:     (none recorded)"
    lines = ["Top referrers:"]
    for item in data[:10]:
        referrer = item.get("referrer", "unknown")
        count = item.get("count", 0)
        unique = item.get("uniques", 0)
        lines.append(f"  {referrer:<40}  {count:>5} views  {unique:>4} unique")
    return "\n".join(lines)


def format_paths(data: list[dict]) -> str:
    """Format the /traffic/popular/paths API response."""
    if not data:
        return "Top paths:         (none recorded)"
    lines = ["Top paths:"]
    for item in data[:10]:
        path = item.get("path", "unknown")
        count = item.get("count", 0)
        unique = item.get("uniques", 0)
        lines.append(f"  {path:<50}  {count:>5} views  {unique:>4} unique")
    return "\n".join(lines)


def format_report(
    views: dict,
    clones: dict,
    referrers: list[dict],
    paths: list[dict],
    repo: str,
    timestamp: str,
) -> str:
    """Compose the full formatted traffic report string."""
    divider = "─" * 60
    lines = [
        divider,
        f"  GitHub Traffic Report — {repo}",
        f"  Generated: {timestamp}",
        divider,
        "",
        format_views(views),
        format_clones(clones),
        "",
        format_referrers(referrers),
        "",
        format_paths(paths),
        "",
        divider,
        "  Note: data covers the past 14 days only (GitHub API limit).",
        "  This report is private. The scanner has no telemetry.",
        divider,
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# GitHub CLI helpers
# ---------------------------------------------------------------------------


def _gh_api(endpoint: str) -> object:
    """Call `gh api <endpoint>` and return parsed JSON. Raises on failure."""
    result = subprocess.run(
        ["gh", "api", endpoint],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"gh api {endpoint} failed (exit {result.returncode}):\n{result.stderr.strip()}"
        )
    return json.loads(result.stdout)


def fetch_traffic(repo: str) -> tuple[dict, dict, list, list]:
    """
    Fetch all four traffic endpoints from the GitHub API.
    Returns (views, clones, referrers, paths).
    Raises RuntimeError if gh is not available or not authenticated.
    """
    base = f"repos/{repo}/traffic"
    views = _gh_api(f"{base}/views")
    clones = _gh_api(f"{base}/clones")
    referrers = _gh_api(f"{base}/popular/referrers")
    paths = _gh_api(f"{base}/popular/paths")
    return views, clones, referrers, paths  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Fetch private GitHub traffic metrics for the agent-readiness repo.",
        epilog=(
            "Requires gh CLI installed and authenticated with repo read access. "
            "Run manually — never runs during agent-scan."
        ),
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write report to reports/GITHUB_TRAFFIC_REPORT.md",
    )
    parser.add_argument(
        "--repo",
        default=REPO,
        help=f"Repository slug (default: {REPO})",
    )
    args = parser.parse_args(argv)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    try:
        views, clones, referrers, paths = fetch_traffic(args.repo)
    except FileNotFoundError:
        print(
            "ERROR: gh CLI not found.\n"
            "Install from https://cli.github.com/ then run: gh auth login",
            file=sys.stderr,
        )
        return 1
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        print(
            "\nMake sure you are authenticated: gh auth login\n"
            "And that your token has the 'repo' scope.",
            file=sys.stderr,
        )
        return 1

    report = format_report(views, clones, referrers, paths, args.repo, timestamp)
    print(report)

    if args.write:
        reports_dir = Path(__file__).parent.parent / "reports"
        reports_dir.mkdir(exist_ok=True)
        output_path = reports_dir / "GITHUB_TRAFFIC_REPORT.md"
        md_content = (
            f"# GitHub Traffic Report — {args.repo}\n\n"
            f"Generated: {timestamp}\n\n"
            "```\n"
            f"{report}\n"
            "```\n"
        )
        output_path.write_text(md_content, encoding="utf-8")
        print(f"\nReport written to: {output_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
