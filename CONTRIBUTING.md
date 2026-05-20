# Contributing to Agent Readiness Scanner

Thank you for considering a contribution. This document explains how to get set up,
what the scope rules are, and what a good contribution looks like.

---

## Scope Rules (Read First)

Before contributing, understand what is **in scope** for this project:

**In scope:**
- New or improved check functions in `agent_readiness/checks.py`
- Improved check accuracy (fewer false positives, fewer false negatives)
- Better terminal output formatting
- Documentation improvements (README, AGENTS.md, CONTRIBUTING.md)
- Test coverage improvements
- Bug fixes

**Out of scope (do not propose):**
- SaaS features, dashboards, or web UI
- Billing, Stripe, or payment integration
- GitHub App or OAuth flows
- LLM or AI model calls of any kind
- External API calls or network requests
- Telemetry or analytics
- New runtime dependencies (the package must remain zero-dependency)
- Token Burn Firewall module (planned separately)
- Repo Red Cell Bot module (planned separately)

If you are unsure whether your idea is in scope, open an issue to discuss it before writing code.

---

## Getting Set Up

```bash
git clone https://github.com/yourusername/agent-readiness
cd agent-readiness
pip install -e .
python -m pytest -q
```

The test suite should pass in under 1 second. If it doesn't, something is broken.

```bash
# Verify the CLI works
agent-scan . --output terminal
agent-scan . --no-color
agent-scan . --version
```

---

## Adding a New Check

If you want to add a new check:

1. **Open an issue first.** Describe what the check detects, what the pass/fail/warn criteria are,
   and what the weight should be. Get feedback before writing code.

2. **Add the check function to `agent_readiness/checks.py`:**

```python
def check_my_new_check(root: Path) -> CheckResult:
    """One-line docstring describing what this checks."""
    # ... detection logic ...
    return CheckResult(
        id="my_new_check",
        name="Human-readable check name",
        description="Why this matters for AI agents",
        weight=2,        # 1 = minor, 2 = moderate, 3 = critical
        status="pass",   # or "fail" or "warn"
        evidence="What was found or not found",
        recommendation="What to do if this fails (empty string if pass)",
    )
```

3. **Add the check to `_ALL_CHECKS`** at the bottom of `checks.py`.

4. **Write tests** in `tests/test_checks.py`. Use `tmp_path` fixture. Cover:
   - The fail case (file missing)
   - The pass case (file present and correct)
   - The warn case if applicable
   - At least one edge case

5. **Update the README** check table if the check is user-facing.

6. **Run the full test suite:**

```bash
python -m pytest -q
```

---

## Test Requirements

- All tests use `tmp_path` (pytest built-in fixture) to create isolated repos
- No network calls in tests — ever
- No LLM calls in tests — ever
- Each check function must have at least one test covering the failure path
- Tests must pass on Python 3.9, 3.10, 3.11, and 3.12
- Do not use `unittest.mock` to mock file system operations — create real temp files instead

---

## Running Tests

```bash
# Full suite, quiet
python -m pytest -q

# Full suite, verbose
python -m pytest -v

# Single test file
python -m pytest tests/test_checks.py -v

# Single test class
python -m pytest tests/test_checks.py::TestAgentsMd -v

# With coverage (if pytest-cov installed)
python -m pytest --cov=agent_readiness --cov-report=term-missing
```

---

## Code Style

- Python ≥ 3.9 with `from __future__ import annotations` at the top of every file
- No runtime dependencies — standard library only
- `TypedDict` for structured return values
- No `print()` in library modules (`checks.py`, `scoring.py`, `report.py`, `templates.py`)
- Functions over classes where possible
- Docstrings on all public functions
- Keep functions under 50 lines; split if longer

---

## Pull Request Checklist

Before opening a PR, confirm:

- [ ] `python -m pytest -q` passes
- [ ] `agent-scan . --output terminal` runs successfully
- [ ] No new runtime dependencies added to `pyproject.toml`
- [ ] No network calls added
- [ ] No LLM calls added
- [ ] README updated if any user-facing behavior changed
- [ ] New check added to the README check table
- [ ] Tests cover the new or modified behavior

---

## Commit Messages

Keep commit messages concise and descriptive. Examples:

```
Add check for .editorconfig presence
Fix false positive in secret detection for test fixture paths
Improve README score tier table formatting
```

---

## Licensing

By contributing, you agree that your contributions are licensed under the MIT License.
