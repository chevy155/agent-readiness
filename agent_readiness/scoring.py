"""Score normalization and risk tier mapping.

Pure functions — no I/O, no side effects.
"""

from __future__ import annotations

from typing import Literal

from .checks import CheckResult

Tier = Literal["GREEN", "YELLOW", "ORANGE", "RED"]

# (min_inclusive, max_inclusive, tier)
_TIER_RANGES: list[tuple[float, float, Tier]] = [
    (85.0, 100.0, "GREEN"),
    (70.0, 84.9, "YELLOW"),
    (50.0, 69.9, "ORANGE"),
    (0.0, 49.9, "RED"),
]

TIER_LABELS: dict[Tier, str] = {
    "GREEN": "Ready",
    "YELLOW": "Mostly Ready",
    "ORANGE": "Needs Work",
    "RED": "Not Ready",
}

TIER_COLORS: dict[Tier, str] = {
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "ORANGE": "\033[33m",
    "RED": "\033[91m",
}

RESET = "\033[0m"

CRITICAL_CHECK_IDS = frozenset({
    "no_env_committed",
    "no_secrets",
})


def compute_score(results: list[CheckResult]) -> float:
    """Normalize weighted check results to a 0–100 score.

    - pass  → full weight credit
    - warn  → half weight credit
    - fail  → zero credit
    """
    if not results:
        return 0.0

    total_weight = sum(r["weight"] for r in results)
    if total_weight == 0:
        return 0.0

    earned = 0.0
    for r in results:
        if r["status"] == "pass":
            earned += r["weight"]
        elif r["status"] == "warn":
            earned += r["weight"] * 0.5

    return round((earned / total_weight) * 100, 1)


def get_tier(score: float) -> Tier:
    """Map a 0–100 score to a risk tier."""
    for low, high, tier in _TIER_RANGES:
        if low <= score <= high:
            return tier
    return "RED"


def get_recommendations(results: list[CheckResult], top_n: int = 3) -> list[str]:
    """Return the top N recommendations from failed/warned checks.

    Ordered by: fail before warn, then by weight (highest first).
    """
    actionable = [
        r for r in results
        if r["status"] in ("fail", "warn") and r["recommendation"]
    ]
    _priority = {"fail": 0, "warn": 1}
    actionable.sort(key=lambda r: (_priority[r["status"]], -r["weight"]))
    return [r["recommendation"] for r in actionable[:top_n]]


def get_critical_failures(results: list[CheckResult]) -> list[CheckResult]:
    """Return failed checks that should block agent modifications.

    Critical failures do not change the score formula. They are surfaced as a
    separate visibility layer so a high overall score cannot hide a committed
    `.env` file or hardcoded secret-pattern finding.
    """
    return [
        r for r in results
        if r["id"] in CRITICAL_CHECK_IDS and r["status"] == "fail"
    ]
