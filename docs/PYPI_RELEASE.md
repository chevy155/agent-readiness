# PyPI Release Guide — Agent Readiness Scanner

This is the canonical step-by-step guide for publishing `agent-readiness` to PyPI.

---

## Prerequisites

```bash
pip install build twine
```

You need:
- A PyPI account at https://pypi.org/
- A PyPI API token (not username/password — token auth is required)
- The `dist/` directory to be clean or nonexistent before each release

---

## Confirming Package Name

The name `agent-readiness` was reserved/registered under the `chevy155` PyPI account.
Confirm the name is yours before uploading:

```
https://pypi.org/project/agent-readiness/
```

If someone has already claimed it under a different account, you will get an error on first upload.
You do **not** need to pre-register the name — uploading for the first time claims it.

---

## Release Checklist

Before running `twine upload`:

- [ ] `pyproject.toml` version matches the release tag (e.g. `0.2.0`)
- [ ] `agent_readiness/__init__.py` `__version__` matches
- [ ] `CHANGELOG.md` has an entry for this version
- [ ] All tests pass: `python -m pytest -q`
- [ ] `dist/` is clean (delete and rebuild)
- [ ] `python -m build` completes with no errors
- [ ] `python -m twine check dist/*` shows `PASSED` for both artifacts
- [ ] Clean-venv install works (see validation steps below)

---

## Build

```bash
# Clean previous build artifacts
Remove-Item -Recurse -Force dist      # PowerShell
# or: rm -rf dist                     # bash

# Build sdist and wheel
python -m build
```

Expected output ends with:
```
Successfully built agent_readiness-0.2.0.tar.gz and agent_readiness-0.2.0-py3-none-any.whl
```

---

## Validate Before Upload

```bash
# Check PyPI metadata rendering
python -m twine check dist/*
```

Expected:
```
Checking dist/agent_readiness-0.2.0-py3-none-any.whl: PASSED
Checking dist/agent_readiness-0.2.0.tar.gz: PASSED
```

### Clean-venv test (optional but recommended)

```bash
python -m venv .venv-test
.venv-test/bin/pip install dist/agent_readiness-0.2.0-py3-none-any.whl

# Verify entry point
.venv-test/bin/agent-scan --version
.venv-test/bin/agent-scan . --output terminal --no-color

# Clean up
rm -rf .venv-test
```

Expected: `agent-scan 0.2.0` and a `100/100 GREEN` self-scan.

---

## Upload to PyPI

### Test PyPI first (recommended for first release)

```bash
python -m twine upload --repository testpypi dist/*
```

Confirm the package renders correctly at:
```
https://test.pypi.org/project/agent-readiness/
```

Then test install from TestPyPI:
```bash
pip install --index-url https://test.pypi.org/simple/ agent-readiness
agent-scan --version
```

### Live PyPI upload

```bash
python -m twine upload dist/*
```

Twine will prompt for:
- Username: `__token__`
- Password: your PyPI API token (starts with `pypi-`)

Or use environment variables to avoid the prompt:
```bash
$env:TWINE_USERNAME = "__token__"
$env:TWINE_PASSWORD = "pypi-YOUR_TOKEN_HERE"
python -m twine upload dist/*
```

---

## After Upload

Confirm the live page:
```
https://pypi.org/project/agent-readiness/
```

Test the live install:
```bash
pip install agent-readiness
agent-scan --version
agent-scan . --output terminal --no-color
```

---

## GitHub Release

Create a GitHub release matching the PyPI version:

```bash
gh release create v0.3.0 \
  --repo chevy155/agent-readiness \
  --title "v0.3.0 — <title>" \
  --notes "..."
```

---

## Update Install Instructions After First PyPI Publish

After successful PyPI publish:

- `README.md` hero install block already shows `pip install agent-readiness` (no changes needed)
- `docs/LAUNCH_POSTS.md` — update any remaining `git clone` install blocks
- `CHANGELOG.md` — add entry noting PyPI availability

---

## Security Notes

- Never commit your PyPI token to the repo
- Use a scoped PyPI API token (project-specific, not account-wide)
- Rotate the token if it is ever accidentally exposed

---

## CI Automation (optional future)

To publish automatically on tagged releases, add `.github/workflows/publish.yml`:

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    environment: pypi
    permissions:
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install build
      - run: python -m build
      - uses: pypa/gh-action-pypi-publish@release/v1
```

This uses OIDC trusted publishing — no API token needed in secrets.

---

## Current Status

| Item | Status |
|---|---|
| `pyproject.toml` metadata | Complete |
| `README.md` renders on PyPI | Verified (twine check PASSED) |
| `dist/` artifacts built | `agent_readiness-0.2.0.tar.gz` + `.whl` |
| `twine check` | PASSED |
| Clean-venv install | PASSED — `100/100 GREEN` |
| PyPI upload | Pending — awaiting operator decision |
