"""
feedback_synthesizer.py

Deterministic feedback analysis for the Agent Readiness Scanner ops agent.

Pure functions — no network, no LLM, no file I/O (callers handle I/O).
All functions are fully testable with mocked string input.

Keyword → category mapping covers the signals most relevant to a CLI
dev tool after a public launch:
  - Installation friction  (install, pip, pypi, windows)
  - Trust/safety concern   (secret, security, telemetry, false positive, llm)
  - Feature request        (docker, node, npm, github action, badge)
  - Bug report             (error, false positive)
  - Documentation confusion (docs, example)
  - Distribution signal    (agent, cursor, copilot, claude, codex)
  - Scope-risk idea        (pricing, dashboard, api, saas)
  - Ignore/noise           (anything unmatched)
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Keyword / category configuration
# ---------------------------------------------------------------------------

KEYWORDS: list[str] = [
    "install",
    "pip",
    "pypi",
    "windows",
    "error",
    "github action",
    "badge",
    "false positive",
    "secret",
    "security",
    "docker",
    "node",
    "npm",
    "docs",
    "example",
    "pricing",
    "telemetry",
    "llm",
    "agent",
    "cursor",
    "copilot",
    "claude",
    "codex",
]

# Keywords that require multi-word matching (order matters — check these first)
MULTI_WORD_KEYWORDS: list[str] = ["github action", "false positive"]

KEYWORD_CATEGORY: dict[str, str] = {
    "install": "Installation friction",
    "pip": "Installation friction",
    "pypi": "Installation friction",
    "windows": "Installation friction",
    "error": "Bug report",
    "false positive": "Bug report",
    "github action": "Feature request",
    "badge": "Feature request",
    "docker": "Feature request",
    "node": "Feature request",
    "npm": "Feature request",
    "secret": "Trust/safety concern",
    "security": "Trust/safety concern",
    "telemetry": "Trust/safety concern",
    "llm": "Trust/safety concern",
    "docs": "Documentation confusion",
    "example": "Documentation confusion",
    "pricing": "Scope-risk idea",
    "agent": "Distribution signal",
    "cursor": "Distribution signal",
    "copilot": "Distribution signal",
    "claude": "Distribution signal",
    "codex": "Distribution signal",
}

ALL_CATEGORIES: list[str] = [
    "Installation friction",
    "Trust/safety concern",
    "Feature request",
    "Bug report",
    "Documentation confusion",
    "Distribution signal",
    "Scope-risk idea",
    "Ignore/noise",
]

# Category → (severity, adoption_impact, scope_risk, effort) heuristic defaults
# These are starting values; operator adjusts in the report.
_HEURISTICS: dict[str, tuple[int, int, int, int]] = {
    "Installation friction":    (4, 5, 1, 2),
    "Trust/safety concern":     (4, 4, 2, 2),
    "Feature request":          (2, 3, 3, 3),
    "Bug report":               (5, 5, 1, 3),
    "Documentation confusion":  (3, 4, 1, 1),
    "Distribution signal":      (1, 3, 1, 1),
    "Scope-risk idea":          (2, 2, 5, 5),
    "Ignore/noise":             (1, 1, 1, 1),
}


# ---------------------------------------------------------------------------
# Core analysis functions
# ---------------------------------------------------------------------------


def extract_keyword_hits(
    text: str,
    keywords: list[str] | None = None,
) -> dict[str, list[str]]:
    """
    For each keyword, extract all lines from text that contain it.
    Case-insensitive. Multi-word keywords are matched as substrings.
    Returns {keyword: [matching_lines]}.
    """
    if keywords is None:
        keywords = KEYWORDS

    lines = text.splitlines()
    hits: dict[str, list[str]] = {}

    for kw in keywords:
        pattern = re.compile(re.escape(kw), re.IGNORECASE)
        matched = [line.strip() for line in lines if pattern.search(line) and line.strip()]
        if matched:
            hits[kw] = matched

    return hits


def categorize_hits(
    hits: dict[str, list[str]],
) -> dict[str, list[str]]:
    """
    Group keyword hits by category.
    Returns {category: [all_matching_lines_for_that_category]}.
    Categories with zero hits are still present with empty lists.
    """
    categories: dict[str, list[str]] = {cat: [] for cat in ALL_CATEGORIES}
    for kw, lines in hits.items():
        cat = KEYWORD_CATEGORY.get(kw, "Ignore/noise")
        # Avoid exact duplicates within a category
        existing = set(categories[cat])
        for line in lines:
            if line not in existing:
                categories[cat].append(line)
                existing.add(line)
    return categories


def count_keyword_frequency(hits: dict[str, list[str]]) -> dict[str, int]:
    """Returns {keyword: hit_line_count} for keywords with at least one hit."""
    return {kw: len(lines) for kw, lines in hits.items() if lines}


def _clamp(value: int, lo: int = 1, hi: int = 5) -> int:
    return max(lo, min(hi, value))


def priority_score(
    frequency: int,
    severity: int,
    adoption_impact: int,
    scope_risk: int,
    effort: int,
) -> int:
    """
    Priority score = frequency + severity + adoption_impact - scope_risk - effort.
    All inputs clamped to [1, 5].
    Range: -8 (lowest) to +13 (highest).
    Higher score = higher priority to address.
    """
    return (
        _clamp(frequency)
        + _clamp(severity)
        + _clamp(adoption_impact)
        - _clamp(scope_risk)
        - _clamp(effort)
    )


@dataclass
class BacklogItem:
    title: str
    category: str
    frequency: int
    severity: int
    adoption_impact: int
    scope_risk: int
    effort: int
    evidence: list[str] = field(default_factory=list)
    score: int = field(init=False)

    def __post_init__(self) -> None:
        self.score = priority_score(
            self.frequency,
            self.severity,
            self.adoption_impact,
            self.scope_risk,
            self.effort,
        )


def build_backlog_from_categories(
    categories: dict[str, list[str]],
    freq: dict[str, int],
) -> list[BacklogItem]:
    """
    Auto-generate a ranked backlog from category hit counts.
    One item per non-empty category.
    Scores are heuristic defaults; operator adjusts in the report.
    Items are sorted by score descending.
    """
    items: list[BacklogItem] = []
    for cat in ALL_CATEGORIES:
        lines = categories.get(cat, [])
        if not lines:
            continue
        hit_count = len(lines)
        sev, adop, srisk, effort = _HEURISTICS.get(cat, (2, 2, 2, 3))
        freq_score = _clamp(hit_count)
        item = BacklogItem(
            title=f"Address: {cat}",
            category=cat,
            frequency=freq_score,
            severity=sev,
            adoption_impact=adop,
            scope_risk=srisk,
            effort=effort,
            evidence=lines[:5],
        )
        items.append(item)

    items.sort(key=lambda x: x.score, reverse=True)
    return items


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------


def render_feedback_section(
    categories: dict[str, list[str]],
    backlog: list[BacklogItem],
    keyword_freq: dict[str, int],
) -> str:
    """
    Render the full feedback analysis block as Markdown.
    Returns a multi-line string starting with '## Feedback Analysis'.
    """
    parts: list[str] = []

    parts.append("## Feedback Analysis\n")

    # --- Keyword frequency table ---
    if keyword_freq:
        parts.append("### Keyword Frequency\n")
        parts.append("| Keyword | Hits |\n|---|---|\n")
        for kw, count in sorted(keyword_freq.items(), key=lambda x: -x[1]):
            parts.append(f"| `{kw}` | {count} |\n")
        parts.append("\n")

    # --- Category detail ---
    parts.append("### Categories\n")
    active_cats = [c for c in ALL_CATEGORIES if categories.get(c)]
    if not active_cats:
        parts.append("> No keyword hits found across all categories.\n\n")
    else:
        for cat in ALL_CATEGORIES:
            lines = categories.get(cat, [])
            if not lines:
                continue
            parts.append(f"**{cat}** ({len(lines)} hits)\n\n")
            for line in lines[:5]:
                parts.append(f"- {line}\n")
            if len(lines) > 5:
                parts.append(f"- *(+{len(lines) - 5} more)*\n")
            parts.append("\n")

    # --- Backlog table ---
    if backlog:
        parts.append("### Improvement Backlog (Top 5)\n\n")
        parts.append(
            "| # | Title | Category | Score | Freq | Sev | Adop | SRisk | Effort |\n"
            "|---|---|---|---|---|---|---|---|---|\n"
        )
        for i, item in enumerate(backlog[:5], 1):
            parts.append(
                f"| {i} | {item.title} | {item.category} | **{item.score}** | "
                f"{item.frequency} | {item.severity} | {item.adoption_impact} | "
                f"{item.scope_risk} | {item.effort} |\n"
            )
        parts.append("\n")

    return "".join(parts)
