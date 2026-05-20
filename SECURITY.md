# Security Policy

## What This Tool Is

Agent Readiness Scanner is a governance and readiness checker. It scans repository structure
to determine whether a repo is configured for safe AI agent use.

## What This Tool Is NOT

**This is not a security scanner.**

Check 11 ("No hardcoded secret patterns") performs basic heuristic detection using four regex
patterns:

| Pattern | Matches |
|---|---|
| `sk-[A-Za-z0-9]{20,}` | OpenAI and Anthropic API key prefixes |
| `ghp_[A-Za-z0-9]{36,}` | GitHub Personal Access Tokens |
| `AKIA[A-Z0-9]{16}` | AWS Access Key IDs |
| `Bearer [token]{20,}` | Bearer auth tokens in source files |

**This detection is deliberately shallow.** It will miss:
- Secrets stored in config files with unusual formats
- Base64-encoded secrets
- Secrets in binary files
- Secrets added to git history but not in the current working tree
- Secrets in environment-specific configs
- Custom API key formats

**For real secret scanning, use:**
- [truffleHog](https://github.com/trufflesecurity/trufflehog) — scans git history, not just current files
- [gitleaks](https://github.com/gitleaks/gitleaks) — fast secret detection in git repos
- [detect-secrets](https://github.com/Yelp/detect-secrets) — pre-commit hook friendly

A passing score on check 11 does **not** mean your repository is free of secrets.

## Reporting Security Issues

If you discover a security vulnerability in Agent Readiness Scanner itself (not in repos it scans),
please open a GitHub issue with the label `security`. Do not include exploit details in the title.

There is no bounty program. This is an open source tool.

## False Positives and False Negatives

Check 11 skips files in test directories (`tests/`, `test/`, `spec/`, `__tests__/`) to reduce
false positives from mock values and test fixtures. This is a deliberate trade-off.

If a scan incorrectly flags a legitimate value, file a bug report with the file type and pattern
that triggered it. We will add it to the exclusion list if it is a genuine false positive.
