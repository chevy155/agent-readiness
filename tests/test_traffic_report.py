"""
Tests for scripts/github_traffic_report.py formatting functions.

All tests use mocked data — no network calls, no gh CLI required.
"""

import sys
from pathlib import Path

import pytest

# Make the scripts/ directory importable
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from github_traffic_report import (
    format_clones,
    format_paths,
    format_referrers,
    format_report,
    format_views,
)


MOCK_VIEWS = {"count": 1234, "uniques": 456, "views": []}
MOCK_CLONES = {"count": 89, "uniques": 67, "clones": []}
MOCK_REFERRERS = [
    {"referrer": "news.ycombinator.com", "count": 500, "uniques": 320},
    {"referrer": "reddit.com", "count": 120, "uniques": 95},
]
MOCK_PATHS = [
    {"path": "/chevy155/agent-readiness", "title": "README", "count": 800, "uniques": 390},
    {"path": "/chevy155/agent-readiness/blob/main/README.md", "title": "README raw", "count": 200, "uniques": 110},
]


class TestFormatViews:
    def test_formats_total_and_unique(self):
        result = format_views(MOCK_VIEWS)
        assert "1,234" in result
        assert "456" in result

    def test_includes_label(self):
        result = format_views(MOCK_VIEWS)
        assert "Views" in result

    def test_zero_values(self):
        result = format_views({"count": 0, "uniques": 0})
        assert "0" in result

    def test_missing_keys_default_zero(self):
        result = format_views({})
        assert "0" in result


class TestFormatClones:
    def test_formats_total_and_unique(self):
        result = format_clones(MOCK_CLONES)
        assert "89" in result
        assert "67" in result

    def test_includes_label(self):
        result = format_clones(MOCK_CLONES)
        assert "Clones" in result

    def test_zero_values(self):
        result = format_clones({"count": 0, "uniques": 0})
        assert "0" in result


class TestFormatReferrers:
    def test_shows_referrer_names(self):
        result = format_referrers(MOCK_REFERRERS)
        assert "news.ycombinator.com" in result
        assert "reddit.com" in result

    def test_shows_counts(self):
        result = format_referrers(MOCK_REFERRERS)
        assert "500" in result
        assert "120" in result

    def test_empty_list_returns_none_message(self):
        result = format_referrers([])
        assert "none" in result.lower()

    def test_limits_to_ten_entries(self):
        many = [{"referrer": f"site{i}.com", "count": i, "uniques": i} for i in range(20)]
        result = format_referrers(many)
        assert "site10.com" not in result
        assert "site9.com" in result


class TestFormatPaths:
    def test_shows_path_names(self):
        result = format_paths(MOCK_PATHS)
        assert "/chevy155/agent-readiness" in result

    def test_shows_counts(self):
        result = format_paths(MOCK_PATHS)
        assert "800" in result
        assert "200" in result

    def test_empty_list_returns_none_message(self):
        result = format_paths([])
        assert "none" in result.lower()

    def test_limits_to_ten_entries(self):
        many = [{"path": f"/path/{i}", "count": i, "uniques": i} for i in range(20)]
        result = format_paths(many)
        assert "/path/10" not in result
        assert "/path/9" in result


class TestFormatReport:
    def test_includes_repo_name(self):
        result = format_report(
            MOCK_VIEWS, MOCK_CLONES, MOCK_REFERRERS, MOCK_PATHS,
            repo="chevy155/agent-readiness",
            timestamp="2026-05-20 12:00 UTC",
        )
        assert "chevy155/agent-readiness" in result

    def test_includes_timestamp(self):
        result = format_report(
            MOCK_VIEWS, MOCK_CLONES, MOCK_REFERRERS, MOCK_PATHS,
            repo="chevy155/agent-readiness",
            timestamp="2026-05-20 12:00 UTC",
        )
        assert "2026-05-20" in result

    def test_includes_views_section(self):
        result = format_report(
            MOCK_VIEWS, MOCK_CLONES, MOCK_REFERRERS, MOCK_PATHS,
            repo="chevy155/agent-readiness",
            timestamp="2026-05-20 12:00 UTC",
        )
        assert "1,234" in result

    def test_includes_clones_section(self):
        result = format_report(
            MOCK_VIEWS, MOCK_CLONES, MOCK_REFERRERS, MOCK_PATHS,
            repo="chevy155/agent-readiness",
            timestamp="2026-05-20 12:00 UTC",
        )
        assert "Clones" in result

    def test_includes_referrer_section(self):
        result = format_report(
            MOCK_VIEWS, MOCK_CLONES, MOCK_REFERRERS, MOCK_PATHS,
            repo="chevy155/agent-readiness",
            timestamp="2026-05-20 12:00 UTC",
        )
        assert "ycombinator" in result

    def test_includes_no_telemetry_note(self):
        result = format_report(
            MOCK_VIEWS, MOCK_CLONES, MOCK_REFERRERS, MOCK_PATHS,
            repo="chevy155/agent-readiness",
            timestamp="2026-05-20 12:00 UTC",
        )
        assert "telemetry" in result
