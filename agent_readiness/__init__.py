"""Agent Readiness Scanner — deterministic AI-agent governance checker.

No network calls. No LLM calls. No telemetry.
"""

__version__ = "0.2.0"
__all__ = ["run_all_checks", "compute_score", "get_tier"]

from .checks import run_all_checks
from .scoring import compute_score, get_tier
