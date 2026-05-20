"""Output rendering: terminal (ANSI), JSON, and Markdown.

No I/O except write_markdown_report() which writes to disk.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from . import __version__
from .checks import CheckResult
from .scoring import (
    RESET,
    TIER_COLORS,
    TIER_LABELS,
    compute_score,
    get_critical_failures,
    get_recommendations,
    get_tier,
)

_STATUS_ICON: dict[str, str] = {
    "pass": "✓",
    "fail": "✗",
    "warn": "⚠",
}

_STATUS_COLOR: dict[str, str] = {
    "pass": "\033[92m",
    "fail": "\033[91m",
    "warn": "\033[93m",
}

_STATUS_MD: dict[str, str] = {
    "pass": "✅ PASS",
    "fail": "❌ FAIL",
    "warn": "⚠️ WARN",
}

_SEP = "─" * 62


def _c(text: str, color_code: str, use_color: bool = True) -> str:
    """Apply ANSI color codes only when use_color is True."""
    if use_color:
        return f"{color_code}{text}{RESET}"
    return text


# ---------------------------------------------------------------------------
# Terminal renderer
# ---------------------------------------------------------------------------

def render_terminal(
    results: list[CheckResult],
    scan_path: str,
    verbose: bool = False,
    color: bool = True,
) -> str:
    score = compute_score(results)
    tier = get_tier(score)
    recommendations = get_recommendations(results)
    critical_failures = get_critical_failures(results)

    # Wrap _c with the color preference for this render call
    def c(text: str, code: str) -> str:
        return _c(text, code, color)

    tier_color = TIER_COLORS[tier]
    lines: list[str] = []

    lines += [
        "",
        _SEP,
        f"  Agent Readiness Scanner  v{__version__}",
        _SEP,
        f"  Repo   : {scan_path}",
        f"  Score  : {c(f'{score:.0f} / 100', tier_color)}",
        f"  Status : {c(f'{tier}  —  {TIER_LABELS[tier]}', tier_color)}",
        f"  Critical failures: {len(critical_failures)}",
        _SEP,
        "",
    ]

    if critical_failures:
        lines += [
            c("  CRITICAL FAILURES PRESENT", "\033[91m"),
            "",
            "  This repo has one or more high-severity failures that should be fixed",
            "  before allowing AI coding agents to modify it.",
            "",
        ]
        for r in critical_failures:
            lines.append(f"  - {r['name']}: {r['evidence']}")
            if r["recommendation"]:
                lines.append(f"    Fix: {r['recommendation']}")
        lines += ["", _SEP, ""]

    # Column widths
    W_NAME = 42
    W_STATUS = 6

    header = f"  {'Check':<{W_NAME}} {'Status':<{W_STATUS}}  Wt"
    lines.append(header)
    lines.append("  " + "─" * (W_NAME + W_STATUS + 8))

    for r in results:
        icon = _STATUS_ICON[r["status"]]
        status_color_code = _STATUS_COLOR[r["status"]]
        raw_status = f"{icon} {r['status'].upper()}"
        colored_status = c(raw_status, status_color_code)
        # Pad based on raw length (not colored length)
        pad = W_STATUS - len(raw_status)
        line = f"  {r['name']:<{W_NAME}} {colored_status}{' ' * max(pad, 0)}  {r['weight']}"
        lines.append(line)

        if verbose:
            lines.append(f"     Evidence : {r['evidence']}")
            if r["recommendation"]:
                lines.append(f"     Fix      : {r['recommendation']}")
            lines.append("")

    lines.append("")
    lines.append(_SEP)

    if recommendations:
        lines.append("  Top Fixes:")
        for i, rec in enumerate(recommendations, 1):
            lines.append(f"    {i}. {rec}")
        lines.append("")

    lines.append("  Tip: run with --generate to create missing governance files.")
    lines.append(_SEP)
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# JSON renderer
# ---------------------------------------------------------------------------

def render_json(results: list[CheckResult], scan_path: str) -> str:
    score = compute_score(results)
    tier = get_tier(score)
    recommendations = get_recommendations(results)
    critical_failures = get_critical_failures(results)

    payload = {
        "scan_path": scan_path,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "score": score,
        "tier": tier,
        "tier_label": TIER_LABELS[tier],
        "critical_failures_present": bool(critical_failures),
        "critical_failures": list(critical_failures),
        "checks": list(results),
        "recommendations": recommendations,
    }
    return json.dumps(payload, indent=2)


# ---------------------------------------------------------------------------
# Markdown renderer
# ---------------------------------------------------------------------------

def render_markdown(results: list[CheckResult], scan_path: str) -> str:
    score = compute_score(results)
    tier = get_tier(score)
    recommendations = get_recommendations(results)
    critical_failures = get_critical_failures(results)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines: list[str] = []

    lines += [
        "# Agent Readiness Report",
        "",
        f"| Field | Value |",
        f"|---|---|",
        f"| **Scan Path** | `{scan_path}` |",
        f"| **Timestamp** | {ts} |",
        f"| **Score** | **{score:.0f} / 100** |",
        f"| **Tier** | **{tier} — {TIER_LABELS[tier]}** |",
        f"| **Critical Failures** | **{len(critical_failures)}** |",
        "",
        "---",
        "",
    ]

    if critical_failures:
        lines += [
            "## Critical Failures Present",
            "",
            "This repo has one or more high-severity failures that should be fixed before allowing AI coding agents to modify it.",
            "",
            "| Check | Evidence | Recommendation |",
            "|---|---|---|",
        ]
        for r in critical_failures:
            evidence = r["evidence"].replace("|", "\\|")
            recommendation = r["recommendation"].replace("|", "\\|")
            lines.append(f"| {r['name']} | {evidence} | {recommendation} |")
        lines += ["", "---", ""]

    lines += [
        "## Check Results",
        "",
        "| # | Check | Status | Weight | Evidence |",
        "|---|---|---|---|---|",
    ]

    for i, r in enumerate(results, 1):
        evidence = r["evidence"].replace("|", "\\|")
        lines.append(
            f"| {i} | {r['name']} | {_STATUS_MD[r['status']]} | {r['weight']} | {evidence} |"
        )

    lines += ["", "## Recommendations", ""]

    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            lines.append(f"{i}. {rec}")
    else:
        lines.append("No critical issues found. Repo is well-configured for AI agents.")

    lines += [
        "",
        "## Generated File Suggestions",
        "",
    ]

    missing = [
        r for r in results
        if r["status"] == "fail" and r["id"] in ("agents_md", "copilot_instructions")
    ]
    if missing:
        lines.append("Run `agent-scan . --generate` to create:")
        for r in missing:
            lines.append(f"- `{r['name']}`")
    else:
        lines.append("All key governance files are present.")

    lines += [
        "",
        "---",
        "",
        "_Generated by "
        f"[Agent Readiness Scanner](https://github.com/chevy155/agent-readiness) v{__version__}_",
    ]

    return "\n".join(lines)


def write_markdown_report(
    results: list[CheckResult],
    scan_path: str,
    output_path: Path,
) -> None:
    """Write Markdown report to disk."""
    output_path.write_text(render_markdown(results, scan_path), encoding="utf-8")
