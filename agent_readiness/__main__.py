"""Allow `python -m agent_readiness` as an entry point."""

import sys

from .cli import main

sys.exit(main())
