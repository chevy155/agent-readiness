"""
Tests for feedback_synthesizer and ops_agent formatting/logic.

All tests use local mocked input only.
No network calls. No gh CLI invocations. No file system side effects
beyond tmp_path fixtures.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Make scripts/ importable
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from feedback_synthesizer import (
    ALL_CATEGORIES,
    BacklogItem,
    build_backlog_from_categories,
    categorize_hits,
    count_keyword_frequency,
    extract_keyword_hits,
    priority_score,
    render_feedback_section,
)
from ops_agent import (
    format_repo_health,
    load_feedback_files,
    render_full_report,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SAMPLE_FEEDBACK = """\
I tried to install it but pip install agent-readiness fails because it's not on pypi yet.
The windows terminal shows a weird error with encoding.
I got a false positive on the secret check — my README has a Bearer example.
Would be great to have a docker image for CI.
The docs need a better example for the github action integration.
Does it support node or npm projects?
Great tool — using it with cursor and copilot already.
No telemetry is a huge plus, I was worried about llm calls.
"""


# ---------------------------------------------------------------------------
# extract_keyword_hits
# ---------------------------------------------------------------------------


class TestExtractKeywordHits:
    def test_basic_hit(self):
        hits = extract_keyword_hits("I tried pip install and got an error.")
        assert "pip" in hits
        assert "install" in hits
        assert "error" in hits

    def test_case_insensitive(self):
        hits = extract_keyword_hits("Use PIP to install.")
        assert "pip" in hits

    def test_multi_word_keyword(self):
        hits = extract_keyword_hits("The github action workflow failed.")
        assert "github action" in hits

    def test_no_hits_returns_empty(self):
        hits = extract_keyword_hits("Everything is working perfectly.")
        assert hits == {}

    def test_returns_matching_lines(self):
        text = "pip is great\nno match here\ninstall via pip"
        hits = extract_keyword_hits(text)
        assert len(hits["pip"]) == 2
        assert "pip is great" in hits["pip"]
        assert "install via pip" in hits["pip"]

    def test_custom_keyword_list(self):
        hits = extract_keyword_hits("foo bar baz", keywords=["foo", "baz"])
        assert "foo" in hits
        assert "baz" in hits
        assert "bar" not in hits

    def test_empty_text(self):
        assert extract_keyword_hits("") == {}

    def test_blank_lines_not_included(self):
        hits = extract_keyword_hits("pip\n\n\ninstall")
        for lines in hits.values():
            assert all(line != "" for line in lines)

    def test_false_positive_multiword(self):
        hits = extract_keyword_hits("Got a false positive on the secret check.")
        assert "false positive" in hits
        assert "secret" in hits

    def test_full_sample(self):
        hits = extract_keyword_hits(SAMPLE_FEEDBACK)
        assert "pip" in hits
        assert "error" in hits
        assert "cursor" in hits
        assert "telemetry" in hits


# ---------------------------------------------------------------------------
# categorize_hits
# ---------------------------------------------------------------------------


class TestCategorizeHits:
    def test_returns_all_categories(self):
        hits = extract_keyword_hits("pip install error")
        cats = categorize_hits(hits)
        assert set(cats.keys()) == set(ALL_CATEGORIES)

    def test_pip_maps_to_installation(self):
        hits = {"pip": ["pip install failed"]}
        cats = categorize_hits(hits)
        assert "pip install failed" in cats["Installation friction"]

    def test_security_maps_to_trust(self):
        hits = {"security": ["I worry about security"]}
        cats = categorize_hits(hits)
        assert "I worry about security" in cats["Trust/safety concern"]

    def test_docker_maps_to_feature_request(self):
        hits = {"docker": ["add a docker image"]}
        cats = categorize_hits(hits)
        assert "add a docker image" in cats["Feature request"]

    def test_docs_maps_to_documentation(self):
        hits = {"docs": ["the docs need improvement"]}
        cats = categorize_hits(hits)
        assert "the docs need improvement" in cats["Documentation confusion"]

    def test_cursor_maps_to_distribution_signal(self):
        hits = {"cursor": ["using it with cursor"]}
        cats = categorize_hits(hits)
        assert "using it with cursor" in cats["Distribution signal"]

    def test_no_duplicates_within_category(self):
        # "error" and "false positive" both map to Bug report;
        # if a line matches both, it should appear once only
        line = "I got a false positive error in the secret check."
        hits = extract_keyword_hits(line)
        cats = categorize_hits(hits)
        bug_lines = cats.get("Bug report", [])
        assert len(bug_lines) == len(set(bug_lines))

    def test_full_sample_categorization(self):
        hits = extract_keyword_hits(SAMPLE_FEEDBACK)
        cats = categorize_hits(hits)
        assert len(cats["Installation friction"]) > 0
        assert len(cats["Distribution signal"]) > 0


# ---------------------------------------------------------------------------
# count_keyword_frequency
# ---------------------------------------------------------------------------


class TestCountKeywordFrequency:
    def test_counts_correctly(self):
        hits = {"pip": ["line1", "line2"], "error": ["line3"]}
        freq = count_keyword_frequency(hits)
        assert freq["pip"] == 2
        assert freq["error"] == 1

    def test_empty_hits_excluded(self):
        hits = {"pip": ["line1"], "install": []}
        freq = count_keyword_frequency(hits)
        assert "pip" in freq
        assert "install" not in freq

    def test_empty_input(self):
        assert count_keyword_frequency({}) == {}


# ---------------------------------------------------------------------------
# priority_score
# ---------------------------------------------------------------------------


class TestPriorityScore:
    def test_basic_calculation(self):
        # 3 + 4 + 5 - 2 - 2 = 8
        assert priority_score(3, 4, 5, 2, 2) == 8

    def test_all_ones(self):
        # 1 + 1 + 1 - 1 - 1 = 1
        assert priority_score(1, 1, 1, 1, 1) == 1

    def test_all_fives(self):
        # 5 + 5 + 5 - 5 - 5 = 5
        assert priority_score(5, 5, 5, 5, 5) == 5

    def test_max_positive(self):
        # 5 + 5 + 5 - 1 - 1 = 13
        assert priority_score(5, 5, 5, 1, 1) == 13

    def test_min_value(self):
        # 1 + 1 + 1 - 5 - 5 = -7
        assert priority_score(1, 1, 1, 5, 5) == -7

    def test_clamps_high_inputs(self):
        # values > 5 are clamped to 5
        assert priority_score(10, 10, 10, 1, 1) == priority_score(5, 5, 5, 1, 1)

    def test_clamps_low_inputs(self):
        # values < 1 are clamped to 1
        assert priority_score(0, 0, 0, 0, 0) == priority_score(1, 1, 1, 1, 1)


# ---------------------------------------------------------------------------
# BacklogItem
# ---------------------------------------------------------------------------


class TestBacklogItem:
    def test_score_computed_on_init(self):
        item = BacklogItem(
            title="Fix install",
            category="Installation friction",
            frequency=4,
            severity=4,
            adoption_impact=5,
            scope_risk=1,
            effort=2,
        )
        assert item.score == priority_score(4, 4, 5, 1, 2)

    def test_evidence_defaults_to_empty(self):
        item = BacklogItem(
            title="Test",
            category="Bug report",
            frequency=1,
            severity=1,
            adoption_impact=1,
            scope_risk=1,
            effort=1,
        )
        assert item.evidence == []


# ---------------------------------------------------------------------------
# build_backlog_from_categories
# ---------------------------------------------------------------------------


class TestBuildBacklogFromCategories:
    def test_returns_sorted_by_score(self):
        cats = {c: [] for c in ALL_CATEGORIES}
        cats["Bug report"] = ["critical crash", "another crash"]
        cats["Scope-risk idea"] = ["add saas"]
        freq: dict[str, int] = {}
        backlog = build_backlog_from_categories(cats, freq)
        assert len(backlog) == 2
        assert backlog[0].score >= backlog[1].score

    def test_empty_categories_returns_empty(self):
        cats = {c: [] for c in ALL_CATEGORIES}
        assert build_backlog_from_categories(cats, {}) == []

    def test_one_item_per_non_empty_category(self):
        cats = {c: [] for c in ALL_CATEGORIES}
        cats["Installation friction"] = ["bad install"]
        cats["Bug report"] = ["crash"]
        backlog = build_backlog_from_categories(cats, {})
        assert len(backlog) == 2

    def test_frequency_capped_at_5(self):
        cats = {c: [] for c in ALL_CATEGORIES}
        cats["Installation friction"] = [f"line {i}" for i in range(20)]
        backlog = build_backlog_from_categories(cats, {})
        assert backlog[0].frequency == 5

    def test_evidence_capped_at_5(self):
        cats = {c: [] for c in ALL_CATEGORIES}
        cats["Documentation confusion"] = [f"line {i}" for i in range(10)]
        backlog = build_backlog_from_categories(cats, {})
        assert len(backlog[0].evidence) <= 5


# ---------------------------------------------------------------------------
# render_feedback_section
# ---------------------------------------------------------------------------


class TestRenderFeedbackSection:
    def test_contains_header(self):
        cats = {c: [] for c in ALL_CATEGORIES}
        result = render_feedback_section(cats, [], {})
        assert "## Feedback Analysis" in result

    def test_empty_feedback_shows_no_hits_message(self):
        cats = {c: [] for c in ALL_CATEGORIES}
        result = render_feedback_section(cats, [], {})
        assert "No keyword hits" in result

    def test_backlog_table_rendered(self):
        cats = {c: [] for c in ALL_CATEGORIES}
        cats["Bug report"] = ["crash on startup"]
        freq = {"error": 1}
        backlog = build_backlog_from_categories(cats, freq)
        result = render_feedback_section(cats, backlog, freq)
        assert "Improvement Backlog" in result
        assert "Bug report" in result

    def test_keyword_frequency_table_rendered(self):
        cats = {c: [] for c in ALL_CATEGORIES}
        freq = {"pip": 3, "error": 1}
        result = render_feedback_section(cats, [], freq)
        assert "Keyword Frequency" in result
        assert "pip" in result
        assert "3" in result

    def test_returns_string(self):
        cats = {c: [] for c in ALL_CATEGORIES}
        result = render_feedback_section(cats, [], {})
        assert isinstance(result, str)


# ---------------------------------------------------------------------------
# load_feedback_files
# ---------------------------------------------------------------------------


class TestLoadFeedbackFiles:
    def test_missing_directory_returns_empty(self, tmp_path):
        missing = tmp_path / "nonexistent"
        assert load_feedback_files(missing) == {}

    def test_empty_directory_returns_empty(self, tmp_path):
        empty = tmp_path / "feedback"
        empty.mkdir()
        assert load_feedback_files(empty) == {}

    def test_gitkeep_not_loaded(self, tmp_path):
        d = tmp_path / "feedback"
        d.mkdir()
        (d / ".gitkeep").write_bytes(b"")
        result = load_feedback_files(d)
        assert ".gitkeep" not in result

    def test_markdown_files_loaded(self, tmp_path):
        d = tmp_path / "feedback"
        d.mkdir()
        (d / "hackernews.md").write_text("pip install failed", encoding="utf-8")
        (d / "reddit.md").write_text("no pypi package yet", encoding="utf-8")
        result = load_feedback_files(d)
        assert "hackernews.md" in result
        assert "reddit.md" in result
        assert "pip install failed" in result["hackernews.md"]

    def test_txt_files_loaded(self, tmp_path):
        d = tmp_path / "feedback"
        d.mkdir()
        (d / "notes.txt").write_text("manual notes", encoding="utf-8")
        result = load_feedback_files(d)
        assert "notes.txt" in result

    def test_empty_files_skipped(self, tmp_path):
        d = tmp_path / "feedback"
        d.mkdir()
        (d / "empty.md").write_bytes(b"")
        result = load_feedback_files(d)
        assert "empty.md" not in result


# ---------------------------------------------------------------------------
# render_full_report
# ---------------------------------------------------------------------------


class TestRenderFullReport:
    def test_no_data_renders_gracefully(self):
        result = render_full_report(
            traffic=None,
            health=None,
            feedback_files={},
            repo="owner/repo",
            timestamp="2026-05-20 12:00 UTC",
        )
        assert "Ops Report" in result
        assert "owner/repo" in result
        assert "no telemetry" in result.lower()

    def test_includes_timestamp(self):
        result = render_full_report(
            traffic=None,
            health=None,
            feedback_files={},
            repo="owner/repo",
            timestamp="2026-05-20 12:00 UTC",
        )
        assert "2026-05-20" in result

    def test_traffic_section_when_present(self):
        traffic = {
            "views": {"count": 500, "uniques": 200, "views": []},
            "clones": {"count": 30, "uniques": 25, "clones": []},
            "referrers": [{"referrer": "news.ycombinator.com", "count": 400, "uniques": 160}],
            "paths": [{"path": "/owner/repo", "count": 450, "uniques": 180}],
        }
        result = render_full_report(
            traffic=traffic,
            health=None,
            feedback_files={},
            repo="owner/repo",
            timestamp="2026-05-20 12:00 UTC",
        )
        assert "500" in result
        assert "ycombinator" in result

    def test_health_section_when_present(self):
        health = {
            "stargazerCount": 42,
            "forkCount": 3,
            "openIssuesCount": 1,
            "open_issues_list": [{"number": 1, "title": "Install fails"}],
            "open_prs_list": [],
        }
        result = render_full_report(
            traffic=None,
            health=health,
            feedback_files={},
            repo="owner/repo",
            timestamp="2026-05-20 12:00 UTC",
        )
        assert "42" in result
        assert "Install fails" in result

    def test_feedback_section_when_present(self):
        result = render_full_report(
            traffic=None,
            health=None,
            feedback_files={"hackernews.md": SAMPLE_FEEDBACK},
            repo="owner/repo",
            timestamp="2026-05-20 12:00 UTC",
        )
        assert "Feedback Analysis" in result
        assert "Recommended v0.2 Action" in result

    def test_default_v02_recommendation_without_feedback(self):
        result = render_full_report(
            traffic=None,
            health=None,
            feedback_files={},
            repo="owner/repo",
            timestamp="2026-05-20 12:00 UTC",
        )
        assert "Critical Failures Banner" in result

    def test_returns_string(self):
        result = render_full_report(None, None, {}, "r", "t")
        assert isinstance(result, str)


# ---------------------------------------------------------------------------
# format_repo_health
# ---------------------------------------------------------------------------


class TestFormatRepoHealth:
    def test_shows_stars_and_forks(self):
        health = {
            "stargazerCount": 99,
            "forkCount": 5,
            "openIssuesCount": 2,
            "open_issues_list": [],
            "open_prs_list": [],
        }
        result = format_repo_health(health)
        assert "99" in result
        assert "5" in result

    def test_shows_open_issues_list(self):
        health = {
            "stargazerCount": 0,
            "forkCount": 0,
            "openIssuesCount": 1,
            "open_issues_list": [{"number": 7, "title": "Windows crash"}],
            "open_prs_list": [],
        }
        result = format_repo_health(health)
        assert "Windows crash" in result
        assert "#7" in result

    def test_empty_health_does_not_crash(self):
        result = format_repo_health({})
        assert isinstance(result, str)
