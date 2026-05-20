## Summary

<!-- One sentence: what does this PR do? -->

## Type of Change

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New check (adds a new agent readiness check)
- [ ] Enhancement (improves existing check accuracy or output)
- [ ] Documentation update
- [ ] Refactor (no functional change)

## Checklist

- [ ] Tests pass: `python -m pytest -q`
- [ ] Scanner runs on this repo: `agent-scan . --output terminal`
- [ ] No new runtime dependencies added
- [ ] No network calls added
- [ ] No LLM calls added
- [ ] No telemetry added
- [ ] README updated if user-facing behavior changed
- [ ] AGENTS.md is still accurate after this change

## Test Coverage

<!-- Which test files cover this change? -->

## Scope Check

This PR does NOT add:
- [ ] SaaS, auth, or dashboard features
- [ ] External API calls
- [ ] LLM or AI model calls
- [ ] Billing or payment code
- [ ] GitHub App or OAuth flows
