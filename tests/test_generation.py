"""Tests for templates.py: file generation and overwrite protection.

Uses tmp_path to create isolated test repos. No network. No LLM.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from agent_readiness.templates import (
    generate_agents_md,
    generate_copilot_instructions,
    write_generated_file,
    _detect_language,
    _detect_repo_name,
)


# ---------------------------------------------------------------------------
# _detect_repo_name
# ---------------------------------------------------------------------------

class TestDetectRepoName:
    def test_returns_directory_name(self, tmp_path: Path) -> None:
        subdir = tmp_path / "my-awesome-project"
        subdir.mkdir()
        assert _detect_repo_name(subdir) == "my-awesome-project"


# ---------------------------------------------------------------------------
# _detect_language
# ---------------------------------------------------------------------------

class TestDetectLanguage:
    def test_python_files_detected(self, tmp_path: Path) -> None:
        (tmp_path / "main.py").write_text("print('hello')")
        (tmp_path / "utils.py").write_text("def noop(): pass")
        lang = _detect_language(tmp_path)
        assert lang == "Python"

    def test_js_files_detected(self, tmp_path: Path) -> None:
        (tmp_path / "app.js").write_text("console.log('hi')")
        lang = _detect_language(tmp_path)
        assert lang == "JavaScript"

    def test_no_files_returns_unknown(self, tmp_path: Path) -> None:
        lang = _detect_language(tmp_path)
        assert lang == "Unknown"

    def test_majority_language_wins(self, tmp_path: Path) -> None:
        for i in range(5):
            (tmp_path / f"mod{i}.py").write_text("pass")
        (tmp_path / "app.js").write_text("const x = 1")
        lang = _detect_language(tmp_path)
        assert lang == "Python"


# ---------------------------------------------------------------------------
# write_generated_file
# ---------------------------------------------------------------------------

class TestWriteGeneratedFile:
    def test_writes_new_file(self, tmp_path: Path) -> None:
        target = tmp_path / "newfile.md"
        written, msg = write_generated_file(target, "# Hello")
        assert written is True
        assert target.read_text() == "# Hello"

    def test_does_not_overwrite_existing_by_default(self, tmp_path: Path) -> None:
        target = tmp_path / "existing.md"
        target.write_text("original content")
        written, msg = write_generated_file(target, "new content")
        assert written is False
        assert target.read_text() == "original content"
        assert "Skipped" in msg

    def test_overwrites_when_forced(self, tmp_path: Path) -> None:
        target = tmp_path / "existing.md"
        target.write_text("old")
        written, msg = write_generated_file(target, "new", overwrite=True)
        assert written is True
        assert target.read_text() == "new"

    def test_creates_parent_directories(self, tmp_path: Path) -> None:
        target = tmp_path / "deep" / "nested" / "file.md"
        written, msg = write_generated_file(target, "content")
        assert written is True
        assert target.exists()

    def test_returns_message_with_path(self, tmp_path: Path) -> None:
        target = tmp_path / "file.md"
        written, msg = write_generated_file(target, "content")
        assert str(target) in msg or "Created" in msg


# ---------------------------------------------------------------------------
# generate_agents_md
# ---------------------------------------------------------------------------

class TestGenerateAgentsMd:
    def test_returns_correct_target_path(self, tmp_path: Path) -> None:
        target, content = generate_agents_md(tmp_path)
        assert target == tmp_path / "AGENTS.md"

    def test_content_contains_repo_name(self, tmp_path: Path) -> None:
        # Create a named subdirectory to test name detection
        project_dir = tmp_path / "my-project"
        project_dir.mkdir()
        _, content = generate_agents_md(project_dir)
        assert "my-project" in content

    def test_content_is_non_empty(self, tmp_path: Path) -> None:
        _, content = generate_agents_md(tmp_path)
        assert len(content) > 200

    def test_content_contains_forbidden_section(self, tmp_path: Path) -> None:
        _, content = generate_agents_md(tmp_path)
        assert "Forbidden" in content or "forbidden" in content

    def test_does_not_write_file(self, tmp_path: Path) -> None:
        """generate_agents_md only returns content; it does not write."""
        generate_agents_md(tmp_path)
        assert not (tmp_path / "AGENTS.md").exists()

    def test_write_then_generate_does_not_overwrite(self, tmp_path: Path) -> None:
        (tmp_path / "AGENTS.md").write_text("# Custom AGENTS.md — do not overwrite\n")
        target, content = generate_agents_md(tmp_path)
        written, _ = write_generated_file(target, content)
        assert written is False
        assert "Custom AGENTS.md" in (tmp_path / "AGENTS.md").read_text()


# ---------------------------------------------------------------------------
# generate_copilot_instructions
# ---------------------------------------------------------------------------

class TestGenerateCopilotInstructions:
    def test_returns_correct_target_path(self, tmp_path: Path) -> None:
        target, content = generate_copilot_instructions(tmp_path)
        assert target == tmp_path / ".github" / "copilot-instructions.md"

    def test_content_is_non_empty(self, tmp_path: Path) -> None:
        _, content = generate_copilot_instructions(tmp_path)
        assert len(content) > 100

    def test_content_contains_no_llm_calls(self, tmp_path: Path) -> None:
        _, content = generate_copilot_instructions(tmp_path)
        # The template should warn agents not to add LLM calls
        assert "LLM" in content or "llm" in content.lower() or "network" in content.lower()

    def test_existing_file_not_overwritten(self, tmp_path: Path) -> None:
        ci_path = tmp_path / ".github" / "copilot-instructions.md"
        ci_path.parent.mkdir(parents=True, exist_ok=True)
        ci_path.write_text("# Custom instructions — do not overwrite\n")
        target, content = generate_copilot_instructions(tmp_path)
        written, _ = write_generated_file(target, content)
        assert written is False
        assert "Custom instructions" in ci_path.read_text()


# ---------------------------------------------------------------------------
# Markdown report generation
# ---------------------------------------------------------------------------

class TestMarkdownReportGeneration:
    def test_render_markdown_contains_score(self, tmp_path: Path) -> None:
        from agent_readiness.checks import run_all_checks
        from agent_readiness.report import render_markdown

        results = run_all_checks(tmp_path)
        md = render_markdown(results, str(tmp_path))
        assert "Score" in md
        assert "/ 100" in md

    def test_render_markdown_contains_all_check_names(self, tmp_path: Path) -> None:
        from agent_readiness.checks import run_all_checks
        from agent_readiness.report import render_markdown

        results = run_all_checks(tmp_path)
        md = render_markdown(results, str(tmp_path))
        for r in results:
            assert r["name"] in md

    def test_write_markdown_report_creates_file(self, tmp_path: Path) -> None:
        from agent_readiness.checks import run_all_checks
        from agent_readiness.report import write_markdown_report

        results = run_all_checks(tmp_path)
        output = tmp_path / "AGENT_READINESS.md"
        write_markdown_report(results, str(tmp_path), output)
        assert output.exists()
        content = output.read_text(encoding="utf-8")
        assert "Agent Readiness Report" in content

    def test_render_json_is_valid_json(self, tmp_path: Path) -> None:
        import json
        from agent_readiness.checks import run_all_checks
        from agent_readiness.report import render_json

        results = run_all_checks(tmp_path)
        raw = render_json(results, str(tmp_path))
        data = json.loads(raw)
        assert "score" in data
        assert "tier" in data
        assert "checks" in data
        assert len(data["checks"]) == 12
