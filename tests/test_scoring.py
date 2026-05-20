"""Tests for scoring.py: compute_score, get_tier, get_recommendations."""

from __future__ import annotations

import pytest

from agent_readiness.checks import CheckResult
from agent_readiness.scoring import (
    compute_score,
    get_recommendations,
    get_tier,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_result(
    status: str,
    weight: int,
    recommendation: str = "",
    check_id: str = "test_check",
) -> CheckResult:
    return CheckResult(
        id=check_id,
        name=f"Check {check_id}",
        description="Test check",
        weight=weight,
        status=status,  # type: ignore[arg-type]
        evidence="test evidence",
        recommendation=recommendation,
    )


# ---------------------------------------------------------------------------
# compute_score
# ---------------------------------------------------------------------------

class TestComputeScore:
    def test_all_pass_returns_100(self) -> None:
        results = [_make_result("pass", 3), _make_result("pass", 2), _make_result("pass", 1)]
        assert compute_score(results) == 100.0

    def test_all_fail_returns_0(self) -> None:
        results = [_make_result("fail", 3), _make_result("fail", 2)]
        assert compute_score(results) == 0.0

    def test_all_warn_returns_50(self) -> None:
        results = [_make_result("warn", 4)]
        assert compute_score(results) == 50.0

    def test_empty_list_returns_0(self) -> None:
        assert compute_score([]) == 0.0

    def test_mixed_results_normalized_correctly(self) -> None:
        # weight 3 pass + weight 1 fail = 3/4 earned = 75.0
        results = [_make_result("pass", 3), _make_result("fail", 1)]
        assert compute_score(results) == 75.0

    def test_warn_counts_as_half_weight(self) -> None:
        # weight 2 warn + weight 2 pass = 1 + 2 = 3 / 4 = 75.0
        results = [_make_result("warn", 2), _make_result("pass", 2)]
        assert compute_score(results) == 75.0

    def test_single_pass_weight_1_returns_100(self) -> None:
        results = [_make_result("pass", 1)]
        assert compute_score(results) == 100.0

    def test_score_rounds_to_one_decimal(self) -> None:
        # 2 pass, 1 fail — weights all 1 → 2/3 = 66.6...7
        results = [
            _make_result("pass", 1),
            _make_result("pass", 1),
            _make_result("fail", 1),
        ]
        score = compute_score(results)
        assert score == round(200 / 3, 1)


# ---------------------------------------------------------------------------
# get_tier
# ---------------------------------------------------------------------------

class TestGetTier:
    def test_100_is_green(self) -> None:
        assert get_tier(100.0) == "GREEN"

    def test_85_is_green(self) -> None:
        assert get_tier(85.0) == "GREEN"

    def test_84_is_yellow(self) -> None:
        assert get_tier(84.0) == "YELLOW"

    def test_70_is_yellow(self) -> None:
        assert get_tier(70.0) == "YELLOW"

    def test_69_is_orange(self) -> None:
        assert get_tier(69.0) == "ORANGE"

    def test_50_is_orange(self) -> None:
        assert get_tier(50.0) == "ORANGE"

    def test_49_is_red(self) -> None:
        assert get_tier(49.0) == "RED"

    def test_0_is_red(self) -> None:
        assert get_tier(0.0) == "RED"

    def test_boundary_84_point_9_is_yellow(self) -> None:
        assert get_tier(84.9) == "YELLOW"

    def test_boundary_85_0_is_green(self) -> None:
        assert get_tier(85.0) == "GREEN"


# ---------------------------------------------------------------------------
# get_recommendations
# ---------------------------------------------------------------------------

class TestGetRecommendations:
    def test_returns_empty_for_all_pass(self) -> None:
        results = [_make_result("pass", 3, recommendation="")]
        assert get_recommendations(results) == []

    def test_returns_fail_recommendations(self) -> None:
        results = [_make_result("fail", 3, recommendation="Fix this.")]
        recs = get_recommendations(results)
        assert "Fix this." in recs

    def test_limits_to_top_n(self) -> None:
        results = [
            _make_result("fail", 3, recommendation=f"Fix {i}.", check_id=f"c{i}")
            for i in range(10)
        ]
        recs = get_recommendations(results, top_n=3)
        assert len(recs) == 3

    def test_fail_prioritized_over_warn(self) -> None:
        results = [
            _make_result("warn", 3, recommendation="Warn rec."),
            _make_result("fail", 1, recommendation="Fail rec."),
        ]
        recs = get_recommendations(results, top_n=1)
        assert recs == ["Fail rec."]

    def test_higher_weight_fail_first(self) -> None:
        results = [
            _make_result("fail", 1, recommendation="Low weight.", check_id="c1"),
            _make_result("fail", 3, recommendation="High weight.", check_id="c2"),
        ]
        recs = get_recommendations(results, top_n=1)
        assert recs == ["High weight."]

    def test_ignores_results_with_no_recommendation(self) -> None:
        results = [
            _make_result("fail", 3, recommendation=""),
            _make_result("fail", 2, recommendation="Fix this."),
        ]
        recs = get_recommendations(results)
        assert recs == ["Fix this."]


# ---------------------------------------------------------------------------
# Integration: full 12-check score against known scenario
# ---------------------------------------------------------------------------

class TestScoreIntegration:
    def test_all_27_weight_pass_yields_100(self) -> None:
        """Total weight across all 12 checks is 27. All pass → 100."""
        from agent_readiness.checks import run_all_checks
        from pathlib import Path
        import tempfile, os

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            # Build a near-perfect repo
            (root / "AGENTS.md").write_text("# AGENTS\nForbidden: never.\nScope: src/\n" * 5)
            gh = root / ".github"
            (gh / "workflows").mkdir(parents=True)
            (gh / "ISSUE_TEMPLATE").mkdir(parents=True)
            (gh / "workflows" / "ci.yml").write_text("name: CI\non: push")
            (gh / "copilot-instructions.md").write_text("Keep deterministic.\n" * 5)
            (gh / "pull_request_template.md").write_text("## Summary\n")
            (gh / "ISSUE_TEMPLATE" / "bug.md").write_text("# Bug\n")
            (root / "tests").mkdir()
            (root / "tests" / "test_main.py").write_text("def test_ok(): pass")
            (root / "README.md").write_text("# Project\n\n" + "Details. " * 60)
            (root / "Makefile").write_text("test:\n\tpytest -q\n")
            (root / ".gitignore").write_text(".env\n.venv\n")
            (root / "CODEOWNERS").write_text("* @owner\n")

            results = run_all_checks(root)
            score = compute_score(results)
            assert score == 100.0, f"Expected 100.0, got {score}. Failures: {[r for r in results if r['status'] != 'pass']}"
