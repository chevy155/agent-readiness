"""Tests for individual check functions in checks.py.

Uses tmp_path (pytest fixture) to create isolated fake repos.
No network calls. No LLM calls.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from agent_readiness.checks import (
    check_agent_boundary,
    check_agents_md,
    check_ci_workflow,
    check_copilot_instructions,
    check_env_example,
    check_issue_templates,
    check_no_env_committed,
    check_no_secrets,
    check_pr_template,
    check_readme_quality,
    check_run_command,
    check_test_directory,
    run_all_checks,
)


# ---------------------------------------------------------------------------
# check_agents_md
# ---------------------------------------------------------------------------

class TestAgentsMd:
    def test_missing_returns_fail(self, tmp_path: Path) -> None:
        result = check_agents_md(tmp_path)
        assert result["status"] == "fail"
        assert result["id"] == "agents_md"

    def test_empty_returns_warn(self, tmp_path: Path) -> None:
        (tmp_path / "AGENTS.md").write_text("# tiny")
        result = check_agents_md(tmp_path)
        assert result["status"] == "warn"

    def test_substantive_returns_pass(self, tmp_path: Path) -> None:
        (tmp_path / "AGENTS.md").write_text(
            "# AGENTS.md\n\nForbidden: do not touch production.\n"
            "Allowed: fix bugs.\nScope: src/ only.\n" * 3
        )
        result = check_agents_md(tmp_path)
        assert result["status"] == "pass"

    def test_weight_is_3(self, tmp_path: Path) -> None:
        result = check_agents_md(tmp_path)
        assert result["weight"] == 3

    def test_generate_recommendation_present_on_fail(self, tmp_path: Path) -> None:
        result = check_agents_md(tmp_path)
        assert "--generate" in result["recommendation"]


# ---------------------------------------------------------------------------
# check_readme_quality
# ---------------------------------------------------------------------------

class TestReadmeQuality:
    def test_missing_returns_fail(self, tmp_path: Path) -> None:
        result = check_readme_quality(tmp_path)
        assert result["status"] == "fail"

    def test_too_short_returns_fail(self, tmp_path: Path) -> None:
        (tmp_path / "README.md").write_text("Hello.")
        result = check_readme_quality(tmp_path)
        assert result["status"] == "fail"

    def test_between_200_and_500_returns_warn(self, tmp_path: Path) -> None:
        (tmp_path / "README.md").write_text("x" * 300)
        result = check_readme_quality(tmp_path)
        assert result["status"] == "warn"

    def test_over_500_returns_pass(self, tmp_path: Path) -> None:
        (tmp_path / "README.md").write_text("# My Project\n\n" + "Details. " * 60)
        result = check_readme_quality(tmp_path)
        assert result["status"] == "pass"

    def test_exactly_200_returns_warn(self, tmp_path: Path) -> None:
        (tmp_path / "README.md").write_text("a" * 200)
        result = check_readme_quality(tmp_path)
        assert result["status"] == "warn"


# ---------------------------------------------------------------------------
# check_ci_workflow
# ---------------------------------------------------------------------------

class TestCiWorkflow:
    def test_missing_returns_fail(self, tmp_path: Path) -> None:
        result = check_ci_workflow(tmp_path)
        assert result["status"] == "fail"

    def test_workflow_yml_returns_pass(self, tmp_path: Path) -> None:
        wf_dir = tmp_path / ".github" / "workflows"
        wf_dir.mkdir(parents=True)
        (wf_dir / "test.yml").write_text("name: CI\non: push\njobs: {}")
        result = check_ci_workflow(tmp_path)
        assert result["status"] == "pass"

    def test_workflow_yaml_extension_returns_pass(self, tmp_path: Path) -> None:
        wf_dir = tmp_path / ".github" / "workflows"
        wf_dir.mkdir(parents=True)
        (wf_dir / "ci.yaml").write_text("name: CI")
        result = check_ci_workflow(tmp_path)
        assert result["status"] == "pass"

    def test_empty_workflows_dir_returns_fail(self, tmp_path: Path) -> None:
        wf_dir = tmp_path / ".github" / "workflows"
        wf_dir.mkdir(parents=True)
        result = check_ci_workflow(tmp_path)
        assert result["status"] == "fail"

    def test_weight_is_3(self, tmp_path: Path) -> None:
        result = check_ci_workflow(tmp_path)
        assert result["weight"] == 3


# ---------------------------------------------------------------------------
# check_test_directory
# ---------------------------------------------------------------------------

class TestTestDirectory:
    def test_no_test_dir_returns_fail(self, tmp_path: Path) -> None:
        result = check_test_directory(tmp_path)
        assert result["status"] == "fail"

    def test_tests_dir_with_py_files_returns_pass(self, tmp_path: Path) -> None:
        test_dir = tmp_path / "tests"
        test_dir.mkdir()
        (test_dir / "test_foo.py").write_text("def test_nothing(): pass")
        result = check_test_directory(tmp_path)
        assert result["status"] == "pass"

    def test_empty_tests_dir_returns_warn(self, tmp_path: Path) -> None:
        (tmp_path / "tests").mkdir()
        result = check_test_directory(tmp_path)
        assert result["status"] == "warn"

    def test_spec_dir_accepted(self, tmp_path: Path) -> None:
        spec = tmp_path / "spec"
        spec.mkdir()
        (spec / "app_spec.rb").write_text('describe "App" do; end')
        result = check_test_directory(tmp_path)
        assert result["status"] == "pass"


# ---------------------------------------------------------------------------
# check_no_secrets
# ---------------------------------------------------------------------------

class TestNoSecrets:
    def test_clean_repo_returns_pass(self, tmp_path: Path) -> None:
        (tmp_path / "main.py").write_text("print('hello')\n")
        result = check_no_secrets(tmp_path)
        assert result["status"] == "pass"

    def test_openai_key_returns_fail(self, tmp_path: Path) -> None:
        (tmp_path / "config.py").write_text("API_KEY = 'sk-abcdefghijklmnopqrstuvwx'\n")
        result = check_no_secrets(tmp_path)
        assert result["status"] == "fail"

    def test_github_token_returns_fail(self, tmp_path: Path) -> None:
        (tmp_path / "deploy.sh").write_text(
            "TOKEN=ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghij\n"
        )
        result = check_no_secrets(tmp_path)
        assert result["status"] == "fail"

    def test_aws_key_returns_fail(self, tmp_path: Path) -> None:
        (tmp_path / "infra.py").write_text("access_key = 'AKIAIOSFODNN7EXAMPLE'\n")
        result = check_no_secrets(tmp_path)
        assert result["status"] == "fail"

    def test_secret_in_test_file_is_ignored(self, tmp_path: Path) -> None:
        test_dir = tmp_path / "tests"
        test_dir.mkdir()
        (test_dir / "test_auth.py").write_text(
            "MOCK_KEY = 'sk-abcdefghijklmnopqrstuvwx'  # fixture only\n"
        )
        result = check_no_secrets(tmp_path)
        assert result["status"] == "pass"

    def test_weight_is_3(self, tmp_path: Path) -> None:
        result = check_no_secrets(tmp_path)
        assert result["weight"] == 3


# ---------------------------------------------------------------------------
# check_no_env_committed
# ---------------------------------------------------------------------------

class TestNoEnvCommitted:
    def test_no_env_file_returns_pass(self, tmp_path: Path) -> None:
        result = check_no_env_committed(tmp_path)
        assert result["status"] == "pass"

    def test_env_file_present_returns_fail(self, tmp_path: Path) -> None:
        (tmp_path / ".env").write_text("SECRET_KEY=abc123\n")
        result = check_no_env_committed(tmp_path)
        assert result["status"] == "fail"

    def test_gitignore_with_env_returns_pass(self, tmp_path: Path) -> None:
        (tmp_path / ".gitignore").write_text(".venv\n.env\n*.pyc\n")
        result = check_no_env_committed(tmp_path)
        assert result["status"] == "pass"


# ---------------------------------------------------------------------------
# check_copilot_instructions
# ---------------------------------------------------------------------------

class TestCopilotInstructions:
    def test_missing_returns_fail(self, tmp_path: Path) -> None:
        result = check_copilot_instructions(tmp_path)
        assert result["status"] == "fail"

    def test_present_and_substantive_returns_pass(self, tmp_path: Path) -> None:
        ci_path = tmp_path / ".github" / "copilot-instructions.md"
        ci_path.parent.mkdir(parents=True, exist_ok=True)
        ci_path.write_text("Keep v0 deterministic. No LLM calls. No network.\n" * 5)
        result = check_copilot_instructions(tmp_path)
        assert result["status"] == "pass"


# ---------------------------------------------------------------------------
# check_pr_template
# ---------------------------------------------------------------------------

class TestPrTemplate:
    def test_missing_returns_fail(self, tmp_path: Path) -> None:
        result = check_pr_template(tmp_path)
        assert result["status"] == "fail"

    def test_present_returns_pass(self, tmp_path: Path) -> None:
        pt = tmp_path / ".github" / "pull_request_template.md"
        pt.parent.mkdir(parents=True, exist_ok=True)
        pt.write_text("## Summary\n\n## Checklist\n- [ ] Tests pass\n")
        result = check_pr_template(tmp_path)
        assert result["status"] == "pass"


# ---------------------------------------------------------------------------
# check_issue_templates
# ---------------------------------------------------------------------------

class TestIssueTemplates:
    def test_missing_returns_fail(self, tmp_path: Path) -> None:
        result = check_issue_templates(tmp_path)
        assert result["status"] == "fail"

    def test_with_template_returns_pass(self, tmp_path: Path) -> None:
        it_dir = tmp_path / ".github" / "ISSUE_TEMPLATE"
        it_dir.mkdir(parents=True)
        (it_dir / "bug_report.md").write_text("# Bug\n\n## Steps\n")
        result = check_issue_templates(tmp_path)
        assert result["status"] == "pass"


# ---------------------------------------------------------------------------
# check_env_example
# ---------------------------------------------------------------------------

class TestEnvExample:
    def test_no_env_files_returns_pass(self, tmp_path: Path) -> None:
        result = check_env_example(tmp_path)
        assert result["status"] == "pass"

    def test_env_without_example_returns_warn(self, tmp_path: Path) -> None:
        (tmp_path / ".env.production").write_text("DB_URL=postgres://...\n")
        result = check_env_example(tmp_path)
        assert result["status"] == "warn"

    def test_env_with_example_returns_pass(self, tmp_path: Path) -> None:
        (tmp_path / ".env.production").write_text("DB_URL=postgres://...\n")
        (tmp_path / ".env.example").write_text("DB_URL=postgres://localhost/mydb\n")
        result = check_env_example(tmp_path)
        assert result["status"] == "pass"


# ---------------------------------------------------------------------------
# check_agent_boundary
# ---------------------------------------------------------------------------

class TestAgentBoundary:
    def test_no_boundary_returns_fail(self, tmp_path: Path) -> None:
        result = check_agent_boundary(tmp_path)
        assert result["status"] == "fail"

    def test_codeowners_returns_pass(self, tmp_path: Path) -> None:
        (tmp_path / "CODEOWNERS").write_text("* @owner\n")
        result = check_agent_boundary(tmp_path)
        assert result["status"] == "pass"

    def test_agentignore_returns_pass(self, tmp_path: Path) -> None:
        (tmp_path / ".agentignore").write_text("secrets/\ninfra/\n")
        result = check_agent_boundary(tmp_path)
        assert result["status"] == "pass"

    def test_agents_md_with_forbidden_returns_pass(self, tmp_path: Path) -> None:
        (tmp_path / "AGENTS.md").write_text(
            "# AGENTS.md\n\n## Forbidden Changes\nDo not touch production.\n"
        )
        result = check_agent_boundary(tmp_path)
        assert result["status"] == "pass"

    def test_agents_md_without_boundaries_returns_warn(self, tmp_path: Path) -> None:
        (tmp_path / "AGENTS.md").write_text("# AGENTS.md\n\nGeneral info only.\n")
        result = check_agent_boundary(tmp_path)
        assert result["status"] == "warn"


# ---------------------------------------------------------------------------
# check_run_command
# ---------------------------------------------------------------------------

class TestRunCommand:
    def test_no_commands_returns_fail(self, tmp_path: Path) -> None:
        result = check_run_command(tmp_path)
        assert result["status"] == "fail"

    def test_makefile_with_test_target_returns_pass(self, tmp_path: Path) -> None:
        (tmp_path / "Makefile").write_text("test:\n\tpytest -q\n\n.PHONY: test\n")
        result = check_run_command(tmp_path)
        assert result["status"] == "pass"

    def test_pyproject_with_pytest_returns_pass(self, tmp_path: Path) -> None:
        (tmp_path / "pyproject.toml").write_text(
            "[build-system]\n[tool.pytest.ini_options]\ntestpaths = ['tests']\n"
        )
        result = check_run_command(tmp_path)
        assert result["status"] == "pass"

    def test_readme_with_pytest_returns_pass(self, tmp_path: Path) -> None:
        (tmp_path / "README.md").write_text(
            "# Project\n\n## Usage\n\n```bash\npytest -q\n```\n" * 10
        )
        result = check_run_command(tmp_path)
        assert result["status"] == "pass"


# ---------------------------------------------------------------------------
# run_all_checks integration
# ---------------------------------------------------------------------------

class TestRunAllChecks:
    def test_returns_12_results(self, tmp_path: Path) -> None:
        results = run_all_checks(tmp_path)
        assert len(results) == 12

    def test_all_results_have_required_fields(self, tmp_path: Path) -> None:
        results = run_all_checks(tmp_path)
        required_fields = {"id", "name", "description", "weight", "status", "evidence", "recommendation"}
        for r in results:
            assert required_fields.issubset(r.keys()), f"Missing fields in: {r}"

    def test_all_statuses_are_valid(self, tmp_path: Path) -> None:
        results = run_all_checks(tmp_path)
        valid_statuses = {"pass", "fail", "warn"}
        for r in results:
            assert r["status"] in valid_statuses, f"Invalid status: {r['status']}"

    def test_empty_repo_produces_mostly_fails(self, tmp_path: Path) -> None:
        results = run_all_checks(tmp_path)
        fails = [r for r in results if r["status"] == "fail"]
        # An empty repo should fail most checks
        assert len(fails) >= 7
