"""Deterministic checks for AI agent readiness.

17 checks — no network calls, no LLM calls, no telemetry.
Each check inspects the file system only.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import TypedDict, Literal

Status = Literal["pass", "fail", "warn"]


class CheckResult(TypedDict):
    id: str
    name: str
    description: str
    weight: int
    status: Status
    evidence: str
    recommendation: str


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_SKIP_DIRS = {
    ".git", ".venv", "venv", "env", ".env",
    "node_modules", "__pycache__", ".pytest_cache",
    "dist", "build", ".tox", ".mypy_cache", ".ruff_cache",
}

_TEST_DIRS = {"tests", "test", "spec", "__tests__", "fixtures", "testdata"}

_BOUNDARY_KEYWORDS = re.compile(
    r"\b(scope|boundaries|boundary|allowed|forbidden|guardrails|off.limits"
    r"|restricted|do not|must not|never|prohibited)\b",
    re.IGNORECASE,
)

_SECRET_PATTERNS = [
    (re.compile(r"sk-[A-Za-z0-9_-]{20,}"), "OpenAI/Anthropic API key (sk-)"),
    (re.compile(r"ghp_[A-Za-z0-9]{36,}"), "GitHub Personal Access Token (ghp_)"),
    (re.compile(r"AKIA[A-Z0-9]{16}"), "AWS Access Key ID (AKIA)"),
    (re.compile(r"Bearer\s+[A-Za-z0-9\-._~+/]{20,}"), "Bearer token"),
]

_SCANNABLE_SUFFIXES = {
    "", ".py", ".js", ".ts", ".jsx", ".tsx", ".rb", ".go",
    ".java", ".cs", ".yml", ".yaml", ".env", ".cfg", ".ini",
    ".toml", ".sh", ".bash", ".zsh", ".fish",
}

_HANDOFF_DOC_CANDIDATES = [
    "CURRENT_STATE.md",
    "HANDOFF.md",
    "SESSION_NOTES.md",
    "RUNBOOK.md",
    "docs/CURRENT_STATE.md",
    "docs/HANDOFF.md",
]

_ENV_EXAMPLE_NAMES = {".env.example", ".env.sample", ".env.template", ".env.dist"}


def _find_env_like_files(root: Path) -> list[Path]:
    return [
        f
        for f in root.glob(".env*")
        if f.is_file() and f.name not in _ENV_EXAMPLE_NAMES
    ]


def _gitignore_has_env_pattern(root: Path) -> bool:
    gitignore = root / ".gitignore"
    if not gitignore.exists():
        return False

    content = gitignore.read_text(errors="replace")
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        if line in {".env", ".env.*", "*.env", "**/.env", "**/.env*"}:
            return True

        if line.startswith(".env") and line not in _ENV_EXAMPLE_NAMES:
            return True

        if "/.env" in line:
            return True

    return False


# ---------------------------------------------------------------------------
# Check 1 — AGENTS.md present
# ---------------------------------------------------------------------------

def check_agents_md(root: Path) -> CheckResult:
    path = root / "AGENTS.md"
    if path.exists():
        size = path.stat().st_size
        if size > 100:
            return CheckResult(
                id="agents_md",
                name="AGENTS.md present",
                description="AGENTS.md provides operational guidance for AI coding agents",
                weight=3,
                status="pass",
                evidence=f"Found AGENTS.md ({size} bytes)",
                recommendation="",
            )
        return CheckResult(
            id="agents_md",
            name="AGENTS.md present",
            description="AGENTS.md provides operational guidance for AI coding agents",
            weight=3,
            status="warn",
            evidence=f"Found AGENTS.md but it is nearly empty ({size} bytes)",
            recommendation="Expand AGENTS.md with project purpose, allowed/forbidden changes, and test commands.",
        )
    return CheckResult(
        id="agents_md",
        name="AGENTS.md present",
        description="AGENTS.md provides operational guidance for AI coding agents",
        weight=3,
        status="fail",
        evidence="AGENTS.md not found in repo root",
        recommendation="Run `agent-scan . --generate` to create a starter AGENTS.md.",
    )


# ---------------------------------------------------------------------------
# Check 2 — .github/copilot-instructions.md present
# ---------------------------------------------------------------------------

def check_copilot_instructions(root: Path) -> CheckResult:
    path = root / ".github" / "copilot-instructions.md"
    if path.exists():
        size = path.stat().st_size
        if size > 50:
            return CheckResult(
                id="copilot_instructions",
                name=".github/copilot-instructions.md present",
                description="Copilot instructions guide AI agents on code style and repo conventions",
                weight=2,
                status="pass",
                evidence=f"Found .github/copilot-instructions.md ({size} bytes)",
                recommendation="",
            )
        return CheckResult(
            id="copilot_instructions",
            name=".github/copilot-instructions.md present",
            description="Copilot instructions guide AI agents on code style and repo conventions",
            weight=2,
            status="warn",
            evidence="Found .github/copilot-instructions.md but it is nearly empty",
            recommendation="Expand copilot-instructions.md with concrete style and scope guidance.",
        )
    return CheckResult(
        id="copilot_instructions",
        name=".github/copilot-instructions.md present",
        description="Copilot instructions guide AI agents on code style and repo conventions",
        weight=2,
        status="fail",
        evidence=".github/copilot-instructions.md not found",
        recommendation="Run `agent-scan . --generate` to create a starter copilot-instructions.md.",
    )


# ---------------------------------------------------------------------------
# Check 3 — Pull request template present
# ---------------------------------------------------------------------------

def check_pr_template(root: Path) -> CheckResult:
    path = root / ".github" / "pull_request_template.md"
    if path.exists():
        return CheckResult(
            id="pr_template",
            name="PR template present",
            description="Pull request template ensures agents produce structured PRs",
            weight=2,
            status="pass",
            evidence="Found .github/pull_request_template.md",
            recommendation="",
        )
    return CheckResult(
        id="pr_template",
        name="PR template present",
        description="Pull request template ensures agents produce structured PRs",
        weight=2,
        status="fail",
        evidence=".github/pull_request_template.md not found",
        recommendation="Add .github/pull_request_template.md with a checklist for reviewers.",
    )


# ---------------------------------------------------------------------------
# Check 4 — Issue templates present
# ---------------------------------------------------------------------------

def check_issue_templates(root: Path) -> CheckResult:
    template_dir = root / ".github" / "ISSUE_TEMPLATE"
    if template_dir.exists():
        templates = (
            list(template_dir.glob("*.md"))
            + list(template_dir.glob("*.yml"))
            + list(template_dir.glob("*.yaml"))
        )
        if templates:
            return CheckResult(
                id="issue_templates",
                name="Issue templates present",
                description="Issue templates help agents and humans file structured reports",
                weight=1,
                status="pass",
                evidence=f"Found {len(templates)} template(s) in .github/ISSUE_TEMPLATE/",
                recommendation="",
            )
    return CheckResult(
        id="issue_templates",
        name="Issue templates present",
        description="Issue templates help agents and humans file structured reports",
        weight=1,
        status="fail",
        evidence=".github/ISSUE_TEMPLATE/ not found or empty",
        recommendation="Add issue templates at .github/ISSUE_TEMPLATE/bug_report.md.",
    )


# ---------------------------------------------------------------------------
# Check 5 — CI workflow present
# ---------------------------------------------------------------------------

def check_ci_workflow(root: Path) -> CheckResult:
    workflow_dir = root / ".github" / "workflows"
    if workflow_dir.exists():
        workflows = list(workflow_dir.glob("*.yml")) + list(workflow_dir.glob("*.yaml"))
        if workflows:
            names = ", ".join(w.name for w in workflows[:5])
            return CheckResult(
                id="ci_workflow",
                name="CI workflow present",
                description="CI workflow ensures agents can verify changes automatically",
                weight=3,
                status="pass",
                evidence=f"Found {len(workflows)} workflow(s): {names}",
                recommendation="",
            )
    return CheckResult(
        id="ci_workflow",
        name="CI workflow present",
        description="CI workflow ensures agents can verify changes automatically",
        weight=3,
        status="fail",
        evidence=".github/workflows/*.yml not found",
        recommendation="Add a GitHub Actions workflow that runs your test suite on push.",
    )


# ---------------------------------------------------------------------------
# Check 6 — Test directory present
# ---------------------------------------------------------------------------

def check_test_directory(root: Path) -> CheckResult:
    candidates = ["tests", "test", "spec", "__tests__"]
    for name in candidates:
        p = root / name
        if p.exists() and p.is_dir():
            files = (
                list(p.rglob("*.py"))
                + list(p.rglob("*.js"))
                + list(p.rglob("*.ts"))
                + list(p.rglob("*.rb"))
                + list(p.rglob("*.go"))
            )
            if files:
                return CheckResult(
                    id="test_directory",
                    name="Test directory present",
                    description="Agents need a test suite to verify their changes",
                    weight=3,
                    status="pass",
                    evidence=f"Found {p.name}/ with {len(files)} test file(s)",
                    recommendation="",
                )
            return CheckResult(
                id="test_directory",
                name="Test directory present",
                description="Agents need a test suite to verify their changes",
                weight=3,
                status="warn",
                evidence=f"Found {p.name}/ but it contains no test files",
                recommendation="Add test files to the test directory.",
            )
    return CheckResult(
        id="test_directory",
        name="Test directory present",
        description="Agents need a test suite to verify their changes",
        weight=3,
        status="fail",
        evidence="No test directory found (checked: tests/, test/, spec/, __tests__/)",
        recommendation="Create a tests/ directory with at least one test file.",
    )


# ---------------------------------------------------------------------------
# Check 7 — Run command documented
# ---------------------------------------------------------------------------

def check_run_command(root: Path) -> CheckResult:
    # Makefile with test target
    makefile = root / "Makefile"
    if makefile.exists():
        content = makefile.read_text(errors="replace")
        if re.search(r"^test\s*:", content, re.MULTILINE):
            return CheckResult(
                id="run_command",
                name="Run command documented",
                description="Agents need to know how to run tests and the project",
                weight=2,
                status="pass",
                evidence="Found Makefile with `test` target",
                recommendation="",
            )

    # justfile
    for jf in ("justfile", "Justfile"):
        if (root / jf).exists():
            return CheckResult(
                id="run_command",
                name="Run command documented",
                description="Agents need to know how to run tests and the project",
                weight=2,
                status="pass",
                evidence=f"Found {jf}",
                recommendation="",
            )

    # package.json scripts
    pkg = root / "package.json"
    if pkg.exists():
        try:
            data = json.loads(pkg.read_text(errors="replace"))
            scripts = data.get("scripts", {})
            if "test" in scripts or "start" in scripts:
                return CheckResult(
                    id="run_command",
                    name="Run command documented",
                    description="Agents need to know how to run tests and the project",
                    weight=2,
                    status="pass",
                    evidence="Found package.json with scripts.test or scripts.start",
                    recommendation="",
                )
        except (json.JSONDecodeError, Exception):
            pass

    # pyproject.toml with pytest or scripts
    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        content = pyproject.read_text(errors="replace")
        if any(k in content for k in ("[tool.pytest", "pytest", "[project.scripts]")):
            return CheckResult(
                id="run_command",
                name="Run command documented",
                description="Agents need to know how to run tests and the project",
                weight=2,
                status="pass",
                evidence="Found pyproject.toml with pytest or scripts configuration",
                recommendation="",
            )

    # README.md with run commands
    readme = root / "README.md"
    if readme.exists():
        content = readme.read_text(errors="replace").lower()
        run_keywords = ["pytest", "npm test", "make test", "python -m", "cargo test", "go test", "bundle exec rspec"]
        if any(kw in content for kw in run_keywords):
            return CheckResult(
                id="run_command",
                name="Run command documented",
                description="Agents need to know how to run tests and the project",
                weight=2,
                status="pass",
                evidence="README.md contains run/test command references",
                recommendation="",
            )

    return CheckResult(
        id="run_command",
        name="Run command documented",
        description="Agents need to know how to run tests and the project",
        weight=2,
        status="fail",
        evidence="No Makefile, justfile, package.json scripts, or pyproject.toml test config found",
        recommendation="Add a Makefile `test` target or document run commands in README.md.",
    )


# ---------------------------------------------------------------------------
# Check 8 — .env.example present if .env patterns detected
# ---------------------------------------------------------------------------

def check_env_example(root: Path) -> CheckResult:
    env_like = _find_env_like_files(root)

    if not env_like:
        return CheckResult(
            id="env_example",
            name=".env.example present (if needed)",
            description="If secrets are used, .env.example documents required variables",
            weight=2,
            status="pass",
            evidence="No .env-like files detected — check not applicable",
            recommendation="",
        )

    for name in _ENV_EXAMPLE_NAMES:
        if (root / name).exists():
            return CheckResult(
                id="env_example",
                name=".env.example present (if needed)",
                description="If secrets are used, .env.example documents required variables",
                weight=2,
                status="pass",
                evidence=f"Found example file alongside .env-like files",
                recommendation="",
            )

    names_str = ", ".join(f.name for f in env_like[:3])
    return CheckResult(
        id="env_example",
        name=".env.example present (if needed)",
        description="If secrets are used, .env.example documents required variables",
        weight=2,
        status="warn",
        evidence=f".env-like file(s) found ({names_str}) but no .env.example exists",
        recommendation="Add .env.example with placeholder values to document required variables.",
    )


# ---------------------------------------------------------------------------
# Check 9 — No .env file committed
# ---------------------------------------------------------------------------

def check_no_env_committed(root: Path) -> CheckResult:
    env_path = root / ".env"
    if env_path.exists():
        return CheckResult(
            id="no_env_committed",
            name="No .env file committed",
            description="A committed .env file exposes secrets to agents and version control",
            weight=3,
            status="fail",
            evidence=".env file found in repo root — may contain real secrets",
            recommendation="Remove .env from the repo immediately and add it to .gitignore.",
        )

    if _gitignore_has_env_pattern(root):
        return CheckResult(
            id="no_env_committed",
            name="No .env file committed",
            description="A committed .env file exposes secrets to agents and version control",
            weight=3,
            status="pass",
            evidence=".env not present; .gitignore includes .env pattern",
            recommendation="",
        )

    return CheckResult(
        id="no_env_committed",
        name="No .env file committed",
        description="A committed .env file exposes secrets to agents and version control",
        weight=3,
        status="pass",
        evidence=".env file not found in repo root",
        recommendation="",
    )


# ---------------------------------------------------------------------------
# Check 10 — Cursor rules present
# ---------------------------------------------------------------------------

def check_cursor_rules(root: Path) -> CheckResult:
    cursor_rules_file = root / ".cursorrules"
    if cursor_rules_file.exists():
        size = cursor_rules_file.stat().st_size
        if size > 50:
            return CheckResult(
                id="cursor_rules",
                name="Cursor rules present",
                description="Cursor rules define local AI-agent behavior and boundaries",
                weight=2,
                status="pass",
                evidence=f"Found .cursorrules ({size} bytes)",
                recommendation="",
            )
        return CheckResult(
            id="cursor_rules",
            name="Cursor rules present",
            description="Cursor rules define local AI-agent behavior and boundaries",
            weight=2,
            status="warn",
            evidence="Found .cursorrules but it is nearly empty",
            recommendation="Expand .cursorrules with concrete scope and safety guidance.",
        )

    rules_dir = root / ".cursor" / "rules"
    if rules_dir.exists() and rules_dir.is_dir():
        rule_files = (
            list(rules_dir.glob("*.mdc"))
            + list(rules_dir.glob("*.md"))
            + list(rules_dir.glob("*.txt"))
        )
        if rule_files:
            return CheckResult(
                id="cursor_rules",
                name="Cursor rules present",
                description="Cursor rules define local AI-agent behavior and boundaries",
                weight=2,
                status="pass",
                evidence=f"Found {len(rule_files)} file(s) in .cursor/rules/",
                recommendation="",
            )

    return CheckResult(
        id="cursor_rules",
        name="Cursor rules present",
        description="Cursor rules define local AI-agent behavior and boundaries",
        weight=2,
        status="fail",
        evidence="No .cursorrules or .cursor/rules/* file found",
        recommendation="Add .cursorrules or .cursor/rules/ with project-specific agent constraints.",
    )


# ---------------------------------------------------------------------------
# Check 11 — Workspace handoff doc present
# ---------------------------------------------------------------------------

def check_workspace_handoff_present(root: Path) -> CheckResult:
    found = [p for p in _HANDOFF_DOC_CANDIDATES if (root / p).exists()]
    if found:
        sample = ", ".join(found[:3])
        return CheckResult(
            id="workspace_handoff",
            name="Workspace handoff/current-state doc present",
            description="Handoff docs reduce re-discovery and drift across agent sessions",
            weight=2,
            status="pass",
            evidence=f"Found handoff/current-state doc(s): {sample}",
            recommendation="",
        )

    return CheckResult(
        id="workspace_handoff",
        name="Workspace handoff/current-state doc present",
        description="Handoff docs reduce re-discovery and drift across agent sessions",
        weight=2,
        status="fail",
        evidence="No CURRENT_STATE/HANDOFF/session notes doc found in root or docs/",
        recommendation="Add CURRENT_STATE.md or HANDOFF.md summarizing active state and next steps.",
    )


# ---------------------------------------------------------------------------
# Check 12 — Test command explicit
# ---------------------------------------------------------------------------

def check_test_command_explicit(root: Path) -> CheckResult:
    makefile = root / "Makefile"
    if makefile.exists():
        content = makefile.read_text(errors="replace")
        if re.search(r"^test\s*:", content, re.MULTILINE):
            return CheckResult(
                id="test_command_explicit",
                name="Test command explicit",
                description="Agent workspaces need an explicit test command that can be run safely",
                weight=2,
                status="pass",
                evidence="Found Makefile with explicit `test` target",
                recommendation="",
            )

    for jf in ("justfile", "Justfile"):
        p = root / jf
        if p.exists():
            content = p.read_text(errors="replace")
            if re.search(r"^test\s*:", content, re.MULTILINE):
                return CheckResult(
                    id="test_command_explicit",
                    name="Test command explicit",
                    description="Agent workspaces need an explicit test command that can be run safely",
                    weight=2,
                    status="pass",
                    evidence=f"Found {jf} with explicit `test` recipe",
                    recommendation="",
                )

    pkg = root / "package.json"
    if pkg.exists():
        try:
            data = json.loads(pkg.read_text(errors="replace"))
            scripts = data.get("scripts", {})
            if "test" in scripts and str(scripts["test"]).strip():
                return CheckResult(
                    id="test_command_explicit",
                    name="Test command explicit",
                    description="Agent workspaces need an explicit test command that can be run safely",
                    weight=2,
                    status="pass",
                    evidence="Found package.json scripts.test",
                    recommendation="",
                )
        except (json.JSONDecodeError, Exception):
            pass

    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        content = pyproject.read_text(errors="replace")
        if "[tool.pytest" in content:
            return CheckResult(
                id="test_command_explicit",
                name="Test command explicit",
                description="Agent workspaces need an explicit test command that can be run safely",
                weight=2,
                status="pass",
                evidence="Found pyproject.toml with pytest configuration",
                recommendation="",
            )

    return CheckResult(
        id="test_command_explicit",
        name="Test command explicit",
        description="Agent workspaces need an explicit test command that can be run safely",
        weight=2,
        status="fail",
        evidence="No explicit test command found in Makefile/justfile/package.json/pyproject.toml",
        recommendation="Add an explicit test command (for example `pytest -q` or `npm test`) in project config.",
    )


# ---------------------------------------------------------------------------
# Check 13 — Env contract pairing
# ---------------------------------------------------------------------------

def check_env_contract_pairing(root: Path) -> CheckResult:
    env_like = _find_env_like_files(root)
    if not env_like:
        return CheckResult(
            id="env_contract_pairing",
            name="Env contract pairing",
            description="If .env-like files exist, .gitignore and example templates must both be in place",
            weight=2,
            status="pass",
            evidence="No .env-like runtime files detected — check not applicable",
            recommendation="",
        )

    if not _gitignore_has_env_pattern(root):
        sample = ", ".join(f.name for f in env_like[:3])
        return CheckResult(
            id="env_contract_pairing",
            name="Env contract pairing",
            description="If .env-like files exist, .gitignore and example templates must both be in place",
            weight=2,
            status="fail",
            evidence=f".env-like file(s) found ({sample}) but .gitignore does not protect .env patterns",
            recommendation="Add `.env` (or `.env.*`) to .gitignore before agent edits continue.",
        )

    has_example = any((root / name).exists() for name in _ENV_EXAMPLE_NAMES)
    if not has_example:
        sample = ", ".join(f.name for f in env_like[:3])
        return CheckResult(
            id="env_contract_pairing",
            name="Env contract pairing",
            description="If .env-like files exist, .gitignore and example templates must both be in place",
            weight=2,
            status="warn",
            evidence=f".env-like file(s) found ({sample}) and .gitignore is correct, but no .env.example/.sample/.template/.dist found",
            recommendation="Add an env example/template file documenting required variables with placeholder values.",
        )

    return CheckResult(
        id="env_contract_pairing",
        name="Env contract pairing",
        description="If .env-like files exist, .gitignore and example templates must both be in place",
        weight=2,
        status="pass",
        evidence=".env-like files detected; .gitignore protects .env and example/template file is present",
        recommendation="",
    )


# ---------------------------------------------------------------------------
# Check 14 — Workspace handoff doc substantive
# ---------------------------------------------------------------------------

def check_workspace_handoff_substantive(root: Path) -> CheckResult:
    existing = [root / p for p in _HANDOFF_DOC_CANDIDATES if (root / p).exists()]
    if not existing:
        return CheckResult(
            id="workspace_handoff_substantive",
            name="Workspace handoff doc substantive",
            description="Handoff docs should contain enough context for the next agent session",
            weight=1,
            status="fail",
            evidence="No handoff/current-state doc available to assess substance",
            recommendation="Add a substantive CURRENT_STATE.md or HANDOFF.md with current state, blockers, and next actions.",
        )

    longest = max(existing, key=lambda p: p.stat().st_size)
    size = longest.stat().st_size
    rel = longest.relative_to(root)

    if size >= 120:
        return CheckResult(
            id="workspace_handoff_substantive",
            name="Workspace handoff doc substantive",
            description="Handoff docs should contain enough context for the next agent session",
            weight=1,
            status="pass",
            evidence=f"{rel} appears substantive ({size} bytes)",
            recommendation="",
        )

    return CheckResult(
        id="workspace_handoff_substantive",
        name="Workspace handoff doc substantive",
        description="Handoff docs should contain enough context for the next agent session",
        weight=1,
        status="warn",
        evidence=f"{rel} exists but is too brief ({size} bytes)",
        recommendation="Expand handoff/current-state doc with decisions made, current status, and concrete next steps.",
    )


# ---------------------------------------------------------------------------
# Check 15 — README.md present and substantive
# ---------------------------------------------------------------------------

def check_readme_quality(root: Path) -> CheckResult:
    readme = root / "README.md"
    if not readme.exists():
        return CheckResult(
            id="readme_quality",
            name="README.md present and substantive",
            description="Agents need README.md to understand the project purpose and usage",
            weight=2,
            status="fail",
            evidence="README.md not found in repo root",
            recommendation="Create README.md with project description, install, and usage sections.",
        )

    content = readme.read_text(errors="replace")
    size = len(content.strip())

    if size >= 500:
        return CheckResult(
            id="readme_quality",
            name="README.md present and substantive",
            description="Agents need README.md to understand the project purpose and usage",
            weight=2,
            status="pass",
            evidence=f"README.md found ({size:,} characters)",
            recommendation="",
        )
    if size >= 200:
        return CheckResult(
            id="readme_quality",
            name="README.md present and substantive",
            description="Agents need README.md to understand the project purpose and usage",
            weight=2,
            status="warn",
            evidence=f"README.md found but brief ({size} characters)",
            recommendation="Expand README.md with install instructions, usage, and examples.",
        )
    return CheckResult(
        id="readme_quality",
        name="README.md present and substantive",
        description="Agents need README.md to understand the project purpose and usage",
        weight=2,
        status="fail",
        evidence=f"README.md found but nearly empty ({size} characters)",
        recommendation="Expand README.md with meaningful content (minimum 200 characters).",
    )


# ---------------------------------------------------------------------------
# Check 16 — No hardcoded secret patterns
# ---------------------------------------------------------------------------

def check_no_secrets(root: Path) -> CheckResult:
    findings: list[str] = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        rel_parts = path.relative_to(root).parts

        # Skip vendor and build directories
        if any(part in _SKIP_DIRS for part in rel_parts):
            continue

        # Skip test fixtures (mocked values are expected there)
        if any(part in _TEST_DIRS for part in rel_parts):
            continue

        # Only scan text-like files
        if path.suffix not in _SCANNABLE_SUFFIXES:
            continue

        try:
            content = path.read_text(errors="replace")
        except (OSError, PermissionError):
            continue

        for pattern, label in _SECRET_PATTERNS:
            if pattern.search(content):
                rel = str(path.relative_to(root))
                findings.append(f"{rel}: {label}")
                break  # one finding per file

        if len(findings) >= 10:
            break  # stop scanning after 10 hits

    if not findings:
        return CheckResult(
            id="no_secrets",
            name="No hardcoded secret patterns",
            description="Hardcoded secrets in source files are dangerous for agents and humans",
            weight=3,
            status="pass",
            evidence="No obvious secret patterns detected in non-test source files",
            recommendation="",
        )

    sample = "; ".join(findings[:3])
    return CheckResult(
        id="no_secrets",
        name="No hardcoded secret patterns",
        description="Hardcoded secrets in source files are dangerous for agents and humans",
        weight=3,
        status="fail",
        evidence=f"Potential secrets in {len(findings)} file(s): {sample}",
        recommendation="Remove hardcoded secrets and use environment variables or a secrets manager.",
    )


# ---------------------------------------------------------------------------
# Check 17 — Agent boundary file present or inferable
# ---------------------------------------------------------------------------

def check_agent_boundary(root: Path) -> CheckResult:
    # CODEOWNERS — standard GitHub path
    codeowners_paths = [
        root / "CODEOWNERS",
        root / ".github" / "CODEOWNERS",
        root / "docs" / "CODEOWNERS",
    ]
    for p in codeowners_paths:
        if p.exists():
            return CheckResult(
                id="agent_boundary",
                name="Agent boundary file present",
                description="Agent boundaries prevent AI agents from modifying protected paths",
                weight=2,
                status="pass",
                evidence=f"Found CODEOWNERS at {p.relative_to(root)}",
                recommendation="",
            )

    # .agentignore — explicit agent exclusion file
    if (root / ".agentignore").exists():
        return CheckResult(
            id="agent_boundary",
            name="Agent boundary file present",
            description="Agent boundaries prevent AI agents from modifying protected paths",
            weight=2,
            status="pass",
            evidence="Found .agentignore",
            recommendation="",
        )

    # AGENTS.md with boundary keywords
    agents_md = root / "AGENTS.md"
    if agents_md.exists():
        content = agents_md.read_text(errors="replace")
        if _BOUNDARY_KEYWORDS.search(content):
            return CheckResult(
                id="agent_boundary",
                name="Agent boundary file present",
                description="Agent boundaries prevent AI agents from modifying protected paths",
                weight=2,
                status="pass",
                evidence="AGENTS.md contains boundary/scope keywords",
                recommendation="",
            )
        return CheckResult(
            id="agent_boundary",
            name="Agent boundary file present",
            description="Agent boundaries prevent AI agents from modifying protected paths",
            weight=2,
            status="warn",
            evidence="AGENTS.md present but no boundary/scope/forbidden keywords found",
            recommendation="Add a 'Forbidden Changes' or 'Boundaries' section to AGENTS.md.",
        )

    return CheckResult(
        id="agent_boundary",
        name="Agent boundary file present",
        description="Agent boundaries prevent AI agents from modifying protected paths",
        weight=2,
        status="fail",
        evidence="No CODEOWNERS, .agentignore, or AGENTS.md with boundary section found",
        recommendation="Add CODEOWNERS or a 'Forbidden Changes' section to AGENTS.md.",
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

_ALL_CHECKS = [
    check_agents_md,
    check_copilot_instructions,
    check_pr_template,
    check_issue_templates,
    check_ci_workflow,
    check_test_directory,
    check_run_command,
    check_env_example,
    check_no_env_committed,
    check_cursor_rules,
    check_workspace_handoff_present,
    check_test_command_explicit,
    check_env_contract_pairing,
    check_workspace_handoff_substantive,
    check_readme_quality,
    check_no_secrets,
    check_agent_boundary,
]


def run_all_checks(repo_path: Path) -> list[CheckResult]:
    """Run all 17 checks against the given repo path."""
    return [check(repo_path) for check in _ALL_CHECKS]
