"""Agent Readiness Scanner CLI.

Usage:
    agent-scan [path] [options]
    python -m agent_readiness.cli [path] [options]

No network calls. No LLM calls. No telemetry.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .checks import run_all_checks
from .report import render_json, render_terminal, write_markdown_report
from .scoring import compute_score, get_tier
from .templates import (
    generate_agents_md,
    generate_copilot_instructions,
    write_generated_file,
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agent-scan",
        description=(
            "Agent Readiness Scanner — check whether a repo is ready for AI coding agents.\n"
            "Scans repo structure, governance files, CI, tests, and safety signals.\n"
            "No network calls. No LLM calls."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  agent-scan .
  agent-scan /path/to/repo --output json
  agent-scan . --output markdown
  agent-scan . --generate
  agent-scan . --fail-under 70 --verbose
""",
    )

    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to the repository root (default: current directory)",
    )
    parser.add_argument(
        "--output",
        choices=["terminal", "json", "markdown"],
        default="terminal",
        help="Output format: terminal (default), json, or markdown",
    )
    parser.add_argument(
        "--generate",
        action="store_true",
        help="Generate missing AGENTS.md and .github/copilot-instructions.md (will not overwrite)",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=70,
        metavar="N",
        help="Score threshold considered acceptable (default: 70, display only)",
    )
    parser.add_argument(
        "--fail-under",
        type=int,
        default=None,
        dest="fail_under",
        metavar="N",
        help="Exit with code 1 if score is below N (useful in CI)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show evidence and recommendations for every check",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    # Ensure UTF-8 output on Windows terminals that default to cp1252
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    parser = _build_parser()
    args = parser.parse_args(argv)

    repo_path = Path(args.path).resolve()

    if not repo_path.exists():
        print(f"error: path does not exist: {repo_path}", file=sys.stderr)
        return 2

    if not repo_path.is_dir():
        print(f"error: path is not a directory: {repo_path}", file=sys.stderr)
        return 2

    results = run_all_checks(repo_path)
    score = compute_score(results)
    scan_path = str(repo_path)

    # --- Output ---
    if args.output == "json":
        print(render_json(results, scan_path))

    elif args.output == "markdown":
        output_file = repo_path / "AGENT_READINESS.md"
        print(render_terminal(results, scan_path, verbose=args.verbose))
        write_markdown_report(results, scan_path, output_file)
        print(f"\n  Markdown report written to: {output_file}\n")

    else:  # terminal
        print(render_terminal(results, scan_path, verbose=args.verbose))

    # --- Generate mode ---
    if args.generate:
        print("  Generating missing governance files...")
        generators = [generate_agents_md, generate_copilot_instructions]
        for gen_fn in generators:
            try:
                target, content = gen_fn(repo_path)
                written, msg = write_generated_file(target, content)
                icon = "  ✓" if written else "  –"
                print(f"{icon} {msg}")
            except Exception as exc:
                print(f"  ✗ Error: {exc}", file=sys.stderr)
        print()

    # --- Exit code ---
    if args.fail_under is not None and score < args.fail_under:
        tier = get_tier(score)
        print(
            f"  FAIL: score {score:.0f} is below --fail-under {args.fail_under}",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
