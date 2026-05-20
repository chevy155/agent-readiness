"""Template generation for missing governance files.

Rules:
- Never overwrites existing files (unless force=True).
- Uses static templates with variable substitution only.
- No LLM calls. No network calls. No telemetry.
"""

from __future__ import annotations

import re
from pathlib import Path

_TEMPLATE_DIR = Path(__file__).parent.parent / "templates"


# ---------------------------------------------------------------------------
# Repo introspection helpers
# ---------------------------------------------------------------------------

def _detect_repo_name(root: Path) -> str:
    return root.resolve().name


_LANG_EXTENSIONS: dict[str, str] = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".go": "Go",
    ".rs": "Rust",
    ".rb": "Ruby",
    ".java": "Java",
    ".cs": "C#",
    ".cpp": "C++",
    ".c": "C",
}


def _detect_language(root: Path) -> str:
    """Return the dominant language by file count."""
    counts: dict[str, int] = {}
    skip = {".git", ".venv", "venv", "node_modules", "__pycache__", "dist", "build"}

    for path in root.rglob("*"):
        if path.is_file() and not any(s in path.parts for s in skip):
            lang = _LANG_EXTENSIONS.get(path.suffix)
            if lang:
                counts[lang] = counts.get(lang, 0) + 1

    if not counts:
        return "Unknown"
    return max(counts, key=lambda k: counts[k])


# ---------------------------------------------------------------------------
# Template rendering
# ---------------------------------------------------------------------------

def _render_template(template_path: Path, subs: dict[str, str]) -> str:
    content = template_path.read_text(encoding="utf-8")
    for key, value in subs.items():
        content = content.replace(f"{{{{{key}}}}}", value)
    return content


# ---------------------------------------------------------------------------
# Public generators
# ---------------------------------------------------------------------------

def generate_agents_md(root: Path) -> tuple[Path, str]:
    """Generate AGENTS.md content. Returns (target_path, content)."""
    template_path = _TEMPLATE_DIR / "AGENTS.md.template"
    target = root / "AGENTS.md"
    subs = {
        "REPO_NAME": _detect_repo_name(root),
        "LANGUAGE": _detect_language(root),
    }
    content = _render_template(template_path, subs)
    return target, content


def generate_copilot_instructions(root: Path) -> tuple[Path, str]:
    """Generate .github/copilot-instructions.md content."""
    template_path = _TEMPLATE_DIR / "copilot-instructions.md.template"
    target = root / ".github" / "copilot-instructions.md"
    subs = {
        "REPO_NAME": _detect_repo_name(root),
        "LANGUAGE": _detect_language(root),
    }
    content = _render_template(template_path, subs)
    return target, content


def write_generated_file(
    path: Path,
    content: str,
    overwrite: bool = False,
) -> tuple[bool, str]:
    """Write a generated file safely.

    Returns (written: bool, message: str).
    Will NOT overwrite existing files unless overwrite=True.
    Creates parent directories as needed.
    """
    if path.exists() and not overwrite:
        return False, f"Skipped (already exists): {path}"

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True, f"Created: {path}"
